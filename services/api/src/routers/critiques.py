import traceback
import logging
from functools import wraps
import os
from typing import Annotated
import urllib.parse
from pydantic import BaseModel, AfterValidator
from src.interfaces import db
from src.lib.url_utils import get_url, sluggify
from supabase import PostgrestAPIError

from fastapi import APIRouter, Depends, HTTPException, Header
from src.lib import auth, keys, validators as vd

from src.lib.few_shot import (
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


@router.get("/ids")
def get_critique_ids() -> list[str]:
    supabase = db.client()
    response = supabase.table("critiques").select("id").execute()
    return [critique["id"] for critique in response.data]


class GetCritiquesQuery(BaseModel):
    team_name: str
    environment_name: str
    workflow_name: str | None = None
    agent_name: str | None = None
    query: str | None = None
    k: int | None = None


class GetCritiquesResult(BaseModel):
    data: list[StrippedCritique]
    count: int


@router.get("")
@ahandle_error
async def list_critiques(
    x_critino_key: Annotated[str, Header()],
    query: Annotated[GetCritiquesQuery, Depends(GetCritiquesQuery)],
) -> GetCritiquesResult:
    logging.info(f"list_critiques: x_critino_key: {x_critino_key} - params: {query}")

    query.team_name = urllib.parse.unquote(query.team_name)
    query.environment_name = urllib.parse.unquote(query.environment_name)
    if query.workflow_name:
        query.workflow_name = urllib.parse.unquote(query.workflow_name)
    if query.agent_name:
        query.agent_name = urllib.parse.unquote(query.agent_name)

    if (query.agent_name is not None) and (query.workflow_name is None):
        raise HTTPException(
            status_code=400,
            detail="If you provide an agent_name, you must also provide a workflow_name",
        )

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

    if query.workflow_name is not None:
        request.eq("workflow_name", query.workflow_name)

    if query.agent_name is not None:
        request.eq("agent_name", query.agent_name)

    response = request.execute()

    if query.query is None or query.k is None:
        return GetCritiquesResult(
            data=[
                StrippedCritique(
                    optimal=critique["optimal"],
                    query=critique["query"],
                    context=critique["context"],
                )
                for critique in response.data
            ],
            count=len(response.data),
        )

    critiques = [
        StrippedCritique(
            optimal=critique["optimal"],
            query=critique["query"],
            context=critique["context"],
        )
        for critique in response.data
    ]

    relevant_critiques = find_relevant_critiques(critiques, query.query, k=query.k)

    return GetCritiquesResult(data=relevant_critiques, count=len(relevant_critiques))


class PostCritiquesQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    environment_name: Annotated[str, AfterValidator(vd.str_empty)]
    workflow_name: Annotated[str, AfterValidator(vd.str_empty)]
    agent_name: Annotated[str, AfterValidator(vd.str_empty)]


class PostCritiquesBody(BaseModel):
    context: str | None = None
    query: str | None = None
    optimal: str | None = None
    response: str | None = None


class PostCritiquesResponse(BaseModel):
    url: str
    data: dict


@router.post("/{id}")
@ahandle_error
async def upsert(
    id: str,
    body: PostCritiquesBody,
    query: Annotated[PostCritiquesQuery, Depends(PostCritiquesQuery)],
    x_critino_key: Annotated[str, Header()],
) -> PostCritiquesResponse:
    supabase = db.client()

    auth.authenticate_team_or_environment(
        supabase, query.team_name, query.environment_name, x_critino_key
    )

    query.team_name = urllib.parse.unquote(query.team_name)
    query.environment_name = urllib.parse.unquote(query.environment_name)
    query.workflow_name = urllib.parse.unquote(query.workflow_name)
    query.agent_name = urllib.parse.unquote(query.agent_name)

    try:
        (
            supabase.table("workflows")
            .upsert(
                {
                    "team_name": query.team_name,
                    "environment_name": query.environment_name,
                    "name": query.workflow_name,
                }
            )
            .execute()
        )

        (
            supabase.table("agents")
            .upsert(
                {
                    "team_name": query.team_name,
                    "environment_name": query.environment_name,
                    "workflow_name": query.workflow_name,
                    "name": query.agent_name,
                }
            )
            .execute()
        )
        critique = (
            supabase.table("critiques")
            .upsert(
                {
                    "team_name": query.team_name,
                    "environment_name": query.environment_name,
                    "workflow_name": query.workflow_name,
                    "agent_name": query.agent_name,
                    "id": id,
                    **body.model_dump(),
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
        url=f"{get_url()}{sluggify(query.team_name)}/{sluggify(query.environment_name)}/workflows/{sluggify(query.workflow_name)}/{id}",
        data=critique,
    )
