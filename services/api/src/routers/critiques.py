import json
import traceback
import logging
from functools import wraps
from typing import Annotated, cast
import urllib.parse
import uuid
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, AfterValidator, Field
from src.interfaces import db, llm
from src.lib.url_utils import get_url, sluggify
from src.lib.critiques_utils import CritiqueGenerator
from src.lib.types import GenerateCritiqueInput
from supabase import PostgrestAPIError

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from src.lib import auth, validators as vd


from src.lib.few_shot import (
    SimilarityKey,
    find_relevant_critiques,
    StrippedCritique,
)

router = APIRouter(prefix="/critiques")


def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            tb_str = "".join(traceback.format_exception(e))
            logging.error(f"Error in {func.__name__}: {e}\n{tb_str}")
            raise HTTPException(
                status_code=500, detail={"message": str(e), "traceback": tb_str}
            )

    return wrapper


def ahandle_error(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            return response
        except HTTPException as e:
            raise e
        except Exception as e:
            tb_str = "".join(traceback.format_exception(e))
            logging.error(f"Error in {func.__name__}: {e}\n{tb_str}")
            raise HTTPException(
                status_code=500, detail={"message": str(e), "traceback": tb_str}
            )

    return wrapper


def generate_situation(model: ChatOpenAI, context: str) -> str:
    class Situation(BaseModel):
        situation: str = Field(
            description="A ~10 word description of the situation from the context and query. The situation should be generic such that it's similarly worded to others since it's used for similarity search."
        )

    context = truncate_context(context)

    prompt = ChatPromptTemplate(
        [
            HumanMessage(
                content=f"""
<context>
{context}
</context>

Please deduce the situation from the context provided.
                """.strip()
            ),
        ]
    )

    agent = model.with_structured_output(Situation)

    situation = cast(
        Situation,
        agent.invoke(prompt.invoke({})),
    ).situation

    logging.info(f"critiques: generate_situation: {situation}")

    return situation


@router.post("/generate")
@ahandle_error
async def generate(
    body: GenerateCritiqueInput
) -> list[dict]:
    critique_generator = CritiqueGenerator()
    response = critique_generator.process_request(body)
    logging.info(f"generate: response: {response}")
    return [json.loads(r) for r in response] if response is not None else []


@router.get("/ids")
def get_critique_ids() -> list[str]:
    supabase = db.client()
    response = supabase.table("critiques").select("id").execute()
    return [critique["id"] for critique in response.data]


class GetCritiquesQuery(BaseModel):
    team_name: str
    environment_name: str
    context: str | None = None
    query: str | None = None
    k: int | None = None
    similarity_key: SimilarityKey = "query"


class GetCritiquesResult(BaseModel):
    situation: str | None = None
    data: list[StrippedCritique]
    count: int


@router.get("")
@ahandle_error
async def list_critiques(
    x_critino_key: Annotated[str, Header()],
    query: Annotated[GetCritiquesQuery, Depends(GetCritiquesQuery)],
    x_openrouter_api_key: Annotated[str | None, Header()],
    tags: Annotated[list[str] | None, Query()] = None,
) -> GetCritiquesResult:
    logging.info(f"list_critiques: x_critino_key: {x_critino_key} - params: {query}")

    query.team_name = urllib.parse.unquote(query.team_name).strip()
    query.environment_name = urllib.parse.unquote(query.environment_name).strip()

    if (query.query is None and query.k is not None) or (
        query.k is None and query.query is not None
    ):
        raise HTTPException(
            status_code=400,
            detail="Both 'query' and 'k' must be either set if you want relevant critiques or None if you want all critiques.",
        )

    supabase = db.client()

    auth.authenticate_team_or_environment(
        supabase, query.team_name, query.environment_name, x_critino_key
    )

    request = (
        supabase.table("critiques")
        .select("*")
        .eq("team_name", query.team_name)
        .eq("environment_name", query.environment_name)
    )
    if tags:
        request = request.contains("tags", tags)

    response = request.execute()

    if query.query is None or query.k is None:
        return GetCritiquesResult(
            data=[
                StrippedCritique(
                    optimal=critique["optimal"] if not None else "",
                    instructions=critique["instructions"] if not None else "",
                    query=critique["query"],
                    context=critique["context"],
                    situation=critique["situation"],
                )
                for critique in response.data
            ],
            count=len(response.data),
        )

    critiques = [
        StrippedCritique(
            optimal=critique["optimal"] if not None else "",
            instructions=critique["instructions"] if not None else "",
            query=critique["query"],
            context=critique["context"],
            situation=critique["situation"],
        )
        for critique in response.data
    ]

    if query.similarity_key == "situation":
        model = (
            llm.chat_open_router(
                model="anthropic/claude-3-5-haiku-20241022:beta",
                api_key=x_openrouter_api_key,
                temperature=0.1,
            )
            if x_openrouter_api_key
            else None
        )

        if not model:
            raise HTTPException(
                status_code=400,
                detail="'similarity_key' is set to 'situation' but no model is available to generate the situation.",
            )

        context = query.context + "\n" if query.context else "" + query.query
        logging.info(f"generate_fields: Generated context: {context}")
        situation = generate_situation(model, context)
        logging.info(f"generate_fields: Generated situation: {situation}")

        relevant_critiques = find_relevant_critiques(
            critiques, situation, k=query.k, similarity_key=query.similarity_key
        )

        return GetCritiquesResult(
            situation=situation, data=relevant_critiques, count=len(relevant_critiques)
        )

    relevant_critiques = find_relevant_critiques(
        critiques, query.query, k=query.k, similarity_key=query.similarity_key
    )

    return GetCritiquesResult(data=relevant_critiques, count=len(relevant_critiques))


class PostCritiquesQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    environment_name: Annotated[str, AfterValidator(vd.str_empty)]
    populate_missing: bool = False


class PostCritiquesBody(BaseModel):
    query: Annotated[str, AfterValidator(vd.str_empty)] | None = None
    response: str | None = None
    context: str | None = None
    optimal: str | None = None
    instructions: str | None = None


class PostCritiquesResponse(BaseModel):
    url: str
    data: dict


class FilledBody(PostCritiquesBody):
    situation: str = ""


def truncate_context(context: str, limit: int = 1500) -> str:
    if len(context) > limit:
        return "..." + context[-limit:]
    return context


def generate_fields(
    query: PostCritiquesQuery,
    body: PostCritiquesBody,
    model: ChatOpenAI,
    attempts: int = 3,
    messages: list[BaseMessage] = [],
) -> FilledBody:
    logging.info(
        f"generate_fields: Starting to generate fields for query: {query}, body: {body}"
    )
    context = (body.context + "\n" if body.context else "") + (
        body.query if body.query else ""
    )
    situation = generate_situation(model, context)
    filled_body = FilledBody(
        query=body.query,
        context=body.context,
        response=body.response if body.response else "",
        optimal=body.optimal,
        instructions=body.instructions,
        situation=situation,
    )

    logging.info(f"generate_fields: Created filled_body: {filled_body}")

    if not query.populate_missing:
        logging.info("critiques: generate_fields: did not populate fields")
        return filled_body

    class Populate(BaseModel):
        chain_of_thought: str = Field(
            description="This is your reasoning, use it to evaluate the current information given. Especially the context and original response 'response'. Evaluate how the response was optimized 'optimal'. Then make sure to evaluate how to create instructions on how to achieve the 'optimal' answer. Always start this field with `Let's think step by step. `"
        )
        optimal: str = Field(
            description="DO NOT LEAVE EMPTY. The pure optimal response."
        )
        instructions: str = Field(
            description="DO NOT LEAVE EMPTY. The pure tailored instructions for achieving a response similar or like the same as the optimal response, only provide instructions on how to achive the optimal response, don't provide your own instructions."
        )

    prompt = ChatPromptTemplate(
        [
            SystemMessage(
                content="""
You revise critiques and populate the missing properties inferring them from the current.
Please populate the missing fields.
DO NOT REPLACE FIELDS ALREADY FILLED IN, THOSE ARE SET IN STONE AS OPTIMAL, USE THOSE TO INSPIRE AND INFER THE MISSING FIELDS.
        """
            ),
            HumanMessage(
                content=f"""
Fields and context:
{filled_body.model_dump_json(indent=4)}

Please deduce the missing fields.
Do NOT change the fields already present.
If optimal is present, that is the **optimal** you're aiming for.
        """
            ),
            MessagesPlaceholder("msgs"),
        ]
    )

    agent = model.with_structured_output(Populate)

    logging.info("generate_fields: Starting attempts to populate fields")
    for attempt in range(attempts):
        logging.info(f"generate_fields: Attempt {attempt + 1}")
        result = cast(
            Populate,
            agent.invoke(prompt.invoke({"msgs": messages})),
        )
        logging.info(f"generate_fields: Result from agent: {result}")
        if (
            filled_body.instructions != ""
            and result.instructions != filled_body.instructions
        ) or (filled_body.optimal != "" and result.optimal != filled_body.optimal):
            logging.info(
                f"generate_fields: Instructions or optimal field not populated, adding messages to correct"
            )
            messages.append(
                AIMessage(name="populator", content=result.model_dump_json(indent=4))
            )
            messages.append(
                HumanMessage(
                    content="You did not properly populate the missing fields. You changed an existing field. DO NOT CHANGE EXISTING FIELDS, THOSE ARE ALREADY PERFECT."
                )
            )
            continue

        filled_body.instructions = (
            result.instructions if result.instructions else filled_body.instructions
        )
        filled_body.optimal = (
            result.optimal if result.optimal else filled_body.instructions
        )

        if filled_body.instructions == "" or filled_body.optimal == "":
            messages.append(
                AIMessage(name="populator", content=result.model_dump_json(indent=4))
            )
            messages.append(
                HumanMessage(
                    content="You did not properly populate the missing fields. You did not populate a missing field. DO NOT CHANGE EXISTING FIELDS, THOSE ARE ALREADY PERFECT."
                )
            )
            continue

        filled_body = FilledBody(
            query=filled_body.query,
            context=filled_body.context,
            response=filled_body.response,
            optimal=filled_body.optimal,
            instructions=filled_body.instructions,
            situation=filled_body.situation,
        )

        logging.info(
            f"critiques: generate_fields: attempt {attempt + 1}: (instructions: {result.instructions}, optimal: {result.optimal})"
        )

        logging.info(
            f"generate_fields: Successfully populated fields on attempt {attempt + 1}"
        )
        logging.info(f"generate_fields: Returning filled_body: {filled_body}")
        return filled_body

    logging.error("generate_fields: all attempts at populating missing failed")
    return filled_body


@router.post("/{id}")
@ahandle_error
async def upsert(
    id: str,
    body: PostCritiquesBody,
    query: Annotated[PostCritiquesQuery, Depends(PostCritiquesQuery)],
    x_critino_key: Annotated[str, Header()],
    x_openrouter_api_key: Annotated[str | None, Header()],
    tags: Annotated[list[str] | None, Query()] = None,
) -> PostCritiquesResponse:
    logging.info(
        f"upsert: id: {id}, body: {body}, query: {query}, x_critino_key: {x_critino_key}, x_openrouter_api_key: {x_openrouter_api_key}"
    )
    query.team_name = urllib.parse.unquote(query.team_name).strip()
    query.environment_name = urllib.parse.unquote(query.environment_name).strip()
    query.populate_missing = False

    if body.instructions is None:
        body.instructions = ""
    if body.optimal is None:
        body.optimal = ""

    model = (
        llm.chat_open_router(
            model="anthropic/claude-3-5-haiku-20241022:beta",
            api_key=x_openrouter_api_key,
            temperature=0.1,
        )
        if x_openrouter_api_key
        else None
    )

    if body.optimal == "" and body.instructions == "" and query.populate_missing:
        raise HTTPException(
            status_code=400,
            detail="both 'optimal' and 'instructions' cannot be empty when 'populate_missing' is true.",
        )
    if query.populate_missing and model is None:
        raise HTTPException(
            status_code=400,
            detail="'populate_missing' is true but no model is available to populate the fields.",
        )

    filled_body = generate_fields(query, body, model) if model else None

    supabase = db.client()

    auth.authenticate_team_or_environment(
        supabase, query.team_name, query.environment_name, x_critino_key
    )

    try:
        (
            supabase.table("environments")
            .upsert(
                {
                    "team_name": query.team_name.strip(),
                    "parent_name": query.environment_name.rsplit("/", 1)[0].strip(),
                    "name": query.environment_name.strip(),
                }
            )
            .execute()
        )
        critique = (
            supabase.table("critiques")
            .upsert(
                {
                    "id": id,
                    "team_name": query.team_name.strip(),
                    "environment_name": query.environment_name.strip(),
                    "tags": tags if tags else [],
                    **(filled_body.model_dump() if filled_body else body.model_dump()),
                }
            )
            .execute()
            .data[0]
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    return PostCritiquesResponse(
        url=f"{get_url()}{sluggify(query.team_name)}/{sluggify(query.environment_name)}/critiques",
        data=critique,
    )


class PostManyCritique(PostCritiquesBody):
    id: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class PostManyCritiquesBody(BaseModel):
    critiques: list[PostManyCritique]


class PostManyCritiquesResponse(BaseModel):
    url: str
    data: list[dict]


@router.post("")
@ahandle_error
async def upsert_many(
    body: PostManyCritiquesBody,
    query: Annotated[PostCritiquesQuery, Depends(PostCritiquesQuery)],
    x_critino_key: Annotated[str, Header()],
    x_openrouter_api_key: Annotated[str | None, Header()],
    tags: Annotated[list[str] | None, Query()] = None,
) -> PostManyCritiquesResponse:
    logging.info(
        f"upsert: id: {id}, body: {body}, query: {query}, x_critino_key: {x_critino_key}, x_openrouter_api_key: {x_openrouter_api_key}"
    )
    query.team_name = urllib.parse.unquote(query.team_name).strip()
    query.environment_name = urllib.parse.unquote(query.environment_name).strip()
    query.populate_missing = False

    data = []
    for critique in body.critiques:
        if critique.instructions is None:
            critique.instructions = ""
        if critique.optimal is None:
            critique.optimal = ""

        model = (
            llm.chat_open_router(
                model="anthropic/claude-3-5-haiku-20241022:beta",
                api_key=x_openrouter_api_key,
                temperature=0.1,
            )
            if x_openrouter_api_key
            else None
        )

        if (
            critique.optimal == ""
            and critique.instructions == ""
            and query.populate_missing
        ):
            raise HTTPException(
                status_code=400,
                detail="both 'optimal' and 'instructions' cannot be empty when 'populate_missing' is true.",
            )
        if query.populate_missing and model is None:
            raise HTTPException(
                status_code=400,
                detail="'populate_missing' is true but no model is available to populate the fields.",
            )

        filled_critique = generate_fields(query, critique, model) if model else None

        supabase = db.client()

        auth.authenticate_team_or_environment(
            supabase, query.team_name, query.environment_name, x_critino_key
        )

        try:
            (
                supabase.table("environments")
                .upsert(
                    {
                        "team_name": query.team_name.strip(),
                        "parent_name": query.environment_name.rsplit("/", 1)[0].strip(),
                        "name": query.environment_name.strip(),
                    }
                )
                .execute()
            )
            critique = (
                supabase.table("critiques")
                .upsert(
                    {
                        "id": critique.id if critique.id else str(uuid.uuid4()),
                        "team_name": query.team_name.strip(),
                        "environment_name": query.environment_name.strip(),
                        "tags": tags if tags else [],
                        **(
                            filled_critique.model_dump()
                            if filled_critique
                            else critique.model_dump()
                        ),
                    }
                )
                .execute()
                .data[0]
            )
        except PostgrestAPIError as e:
            logging.error(f"PostgrestAPIError: {e}")
            raise HTTPException(status_code=500, detail={**e.json()})
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail={**e.__dict__})

        data.append(critique)

    return PostManyCritiquesResponse(
        url=f"{get_url()}{sluggify(query.team_name)}/{sluggify(query.environment_name)}/critiques",
        data=data,
    )
