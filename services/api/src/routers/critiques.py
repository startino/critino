import traceback
import logfire
import asyncio
from functools import wraps
from typing import Annotated
import urllib.parse
import uuid
from langchain_core.messages import HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from pydantic import BaseModel, AfterValidator
from src.interfaces import db, llm
from src.lib.url_utils import get_url, sluggify
from src.lib.critiques_utils import CritiqueGenerator
from src.lib.types import GenerateCritiqueInput
from supabase import PostgrestAPIError
from sse_starlette import EventSourceResponse

from fastapi import APIRouter, Depends, HTTPException, Header, Query
from src.lib import auth, validators as vd


from src.lib.few_shot import SimilarityKey, keyword_search
from src.models.critique import Critique, CritiqueWithSituation

router = APIRouter(prefix="/critiques")

supabase = db.client()


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
            logfire.error(f"Error in {func.__name__}: {e}\n{tb_str}")
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
            logfire.error(f"Error in {func.__name__}: {e}\n{tb_str}")
            raise HTTPException(
                status_code=500, detail={"message": str(e), "traceback": tb_str}
            )

    return wrapper


def generate_situation(model: ChatOpenAI, query: str) -> str:
    logfire.info(f"generate_fields: query: {query}")
    query = truncate_query(query)

    prompt = [
        HumanMessage(
            content=f"""
<context>
{query}
</context>

Please deduce the situation from the context provided.

Provide a ~10 word description of the situation from the query and query. The situation should be generic such that it's similarly worded to others since it's used for similarity search. Do not mention specifics like names.
                """.strip()
        ),
    ]

    situation = model.invoke(prompt)

    logfire.info(f"critiques: generate_situation: {situation.content}")

    return situation.content


@router.post("/generate")
@ahandle_error
async def generate(
    x_openrouter_api_key: Annotated[str | None, Header()], body: GenerateCritiqueInput
):
    if not x_openrouter_api_key:
        raise HTTPException(
            status_code=400,
            detail="OpenRouter API key is required to generate critiques.",
        )
    critique_generator = CritiqueGenerator(body.instructions, x_openrouter_api_key)
    event = critique_generator.process_request(body)
    return EventSourceResponse(event, media_type="text/event-stream")


@router.get("/ids")
def get_critique_ids() -> list[str]:
    supabase = db.client()
    response = supabase.table("critiques").select("id").execute()
    return [critique["id"] for critique in response.data]


class GetCritiquesQuery(BaseModel):
    team_name: str
    environment_name: str
    query: str | None = None
    k: int | None = None
    similarity_key: SimilarityKey = "query"


class GetCritiquesResult(BaseModel):
    situation: str | None = None
    data: list[Critique]
    count: int


@router.get("")
@ahandle_error
async def list_critiques(
    x_critino_key: Annotated[str, Header()],
    query: Annotated[GetCritiquesQuery, Depends(GetCritiquesQuery)],
    x_openrouter_api_key: Annotated[str | None, Header()],
    tags: Annotated[list[str] | None, Query()] = None,
) -> GetCritiquesResult:
    logfire.info(f"list_critiques: x_critino_key: {x_critino_key} - params: {query}")

    query.team_name = urllib.parse.unquote(query.team_name).strip()
    query.environment_name = urllib.parse.unquote(query.environment_name).strip()

    if (query.query is None and query.k is not None) or (
        query.k is None and query.query is not None
    ):
        raise HTTPException(
            status_code=400,
            detail="Both 'query' and 'k' must be either set if you want relevant critiques or None if you want all critiques.",
        )

    async def authenticate():
        return auth.authenticate_team_or_environment(
            supabase, query.team_name, query.environment_name, x_critino_key
        )

    async def get_critiques(supabase, query):
        with logfire.span(
            f"fetching critiques for {query.team_name}/{query.environment_name}"
        ):
            request = (
                supabase.table("critiques")
                .select("*")
                .eq("team_name", query.team_name)
                .eq("environment_name", query.environment_name)
            )
            if tags:
                request = request.contains("tags", tags)

            return request.execute()

    auth_task = asyncio.create_task(authenticate())
    critiques_task = asyncio.create_task(get_critiques(supabase, query))

    authenticated, response = await asyncio.gather(auth_task, critiques_task)

    if not authenticated:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized.",
        )

    if query.query is None or query.k is None:
        return GetCritiquesResult(
            data=[
                Critique(
                    query=critique["query"],
                    feedback=critique["feedback"],
                    response=critique["response"],
                )
                for critique in response.data
            ],
            count=len(response.data),
        )

    critiques = [
        CritiqueWithSituation(
            query=critique["query"],
            feedback=critique["feedback"],
            response=critique["response"],
            situation=critique["situation"],
        )
        for critique in response.data
    ]

    situation = None
    if query.similarity_key == "situation":
        with logfire.span("generating situation"):
            model = (
                llm.chat_open_router(
                    model="google/gemini-2.0-flash-001",
                    api_key=x_openrouter_api_key,
                    temperature=0,
                )
                if x_openrouter_api_key
                else None
            )

            if not model:
                raise HTTPException(
                    status_code=400,
                    detail="'similarity_key' is set to 'situation' but no model is available to generate the situation.",
                )

            situation = generate_situation(model, query.query)

    relevant_critiques = keyword_search(
        critiques,
        situation if situation else query.query,
        k=query.k,
        similarity_key=query.similarity_key,
    )

    return GetCritiquesResult(data=relevant_critiques, count=len(relevant_critiques))


class PostCritiquesQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    environment_name: Annotated[str, AfterValidator(vd.str_empty)]


class Feedback(BaseModel):
    response: str
    correction: str


class PostCritiquesResponse(BaseModel):
    url: str
    data: dict


def truncate_query(query: str, limit: int = 1500) -> str:
    if len(query) > limit:
        return "..." + query[-limit:]
    return query


@router.post("/{id}")
@ahandle_error
async def upsert(
    id: str,
    body: Critique,
    query: Annotated[PostCritiquesQuery, Depends(PostCritiquesQuery)],
    x_critino_key: Annotated[str, Header()],
    x_openrouter_api_key: Annotated[str, Header()],
    tags: Annotated[list[str] | None, Query()] = None,
) -> PostCritiquesResponse:
    logfire.info(
        f"upsert: id: {id}, body: {body}, query: {query}, x_critino_key: {x_critino_key}, x_openrouter_api_key: {x_openrouter_api_key}"
    )
    query.team_name = urllib.parse.unquote(query.team_name).strip()
    query.environment_name = urllib.parse.unquote(query.environment_name).strip()

    model = llm.chat_open_router(
        model="google/gemini-2.0-flash-001",
        api_key=x_openrouter_api_key,
        temperature=0,
    )

    situation = generate_situation(model, body.query)

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
                    "query": body.query,
                    "feedback": (
                        [f.model_dump() for f in body.feedback] if body.feedback else []
                    ),
                    "response": body.response if body.response else "",
                    "situation": situation,
                }
            )
            .execute()
            .data[0]
        )
    except PostgrestAPIError as e:
        logfire.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logfire.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    return PostCritiquesResponse(
        url=f"{get_url()}{sluggify(query.team_name)}/{sluggify(query.environment_name)}/critiques",
        data=critique,
    )


class PostManyCritique(Critique):
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
    x_openrouter_api_key: Annotated[str, Header()],
    tags: Annotated[list[str] | None, Query()] = None,
) -> PostManyCritiquesResponse:
    logfire.info(
        f"upsert: id: {id}, body: {body}, query: {query}, x_critino_key: {x_critino_key}, x_openrouter_api_key: {x_openrouter_api_key}"
    )
    query.team_name = urllib.parse.unquote(query.team_name).strip()
    query.environment_name = urllib.parse.unquote(query.environment_name).strip()

    data = []
    for critique in body.critiques:
        model = llm.chat_open_router(
            model="google/gemini-2.0-flash-001",
            api_key=x_openrouter_api_key,
            temperature=0,
        )

        situation = generate_situation(model, critique.query)

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
                        "query": critique.query,
                        "feedback": critique.feedback if critique.feedback else [],
                        "response": critique.response if critique.response else "",
                        "situation": situation,
                    }
                )
                .execute()
                .data[0]
            )
        except PostgrestAPIError as e:
            logfire.error(f"PostgrestAPIError: {e}")
            raise HTTPException(status_code=500, detail={**e.json()})
        except Exception as e:
            logfire.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail={**e.__dict__})

        data.append(critique)

    return PostManyCritiquesResponse(
        url=f"{get_url()}{sluggify(query.team_name)}/{sluggify(query.environment_name)}/critiques",
        data=data,
    )
