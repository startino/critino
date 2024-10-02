import traceback
import logging
from functools import wraps
import os
from typing import Annotated
from pydantic import BaseModel, AfterValidator
from src.interfaces import db
from supabase import PostgrestAPIError

from fastapi import APIRouter, Depends, HTTPException
from src.lib import auth, keys, validators as vd

from src.lib.few_shot import (
    find_relevant_critiques,
    StrippedCritique,
)

router = APIRouter(prefix="/critiques")

PUBLIC_SITE_URL = os.getenv("PUBLIC_SITE_URL", "http://0.0.0.0:5173")


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


class GetCritiquesParams(BaseModel):
    team_name: str
    environment_name: str
    key: Annotated[str, AfterValidator(vd.str_empty)]
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
    params: GetCritiquesParams = Depends(),
) -> GetCritiquesResult:

    if (params.agent_name is not None) and (params.workflow_name is None):
        raise HTTPException(
            status_code=400,
            detail="If you provide an agent_name, you must also provide a workflow_name",
        )

    if (params.query is None and params.k is not None) or (
        params.k is None and params.query is not None
    ):
        raise HTTPException(
            status_code=400,
            detail="Both 'query' and 'k' must be either set if you want relevant critiques or None if you want all critiques.",
        )

    supabase = db.client()

    auth.authenticate_team_or_environment(
        supabase, params.team_name, params.environment_name, params.key
    )

    request = (
        supabase.table("critiques")
        .select("*")
        .eq("team_name", params.team_name)
        .eq("environment_name", params.environment_name)
    )

    if params.workflow_name is not None:
        request.eq("workflow_name", params.workflow_name)

    if params.agent_name is not None:
        request.eq("agent_name", params.agent_name)

    response = request.execute()

    if params.query is None or params.k is None:
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

    relevant_critiques = find_relevant_critiques(critiques, params.query, k=params.k)

    return GetCritiquesResult(data=relevant_critiques, count=len(relevant_critiques))


class PostCritiquesParams(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    environment_name: Annotated[str, AfterValidator(vd.str_empty)]
    workflow_name: Annotated[str, AfterValidator(vd.str_empty)]
    agent_name: Annotated[str, AfterValidator(vd.str_empty)]
    key: Annotated[str, AfterValidator(vd.str_empty)]


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
    id: str, body: PostCritiquesBody, params: PostCritiquesParams = Depends()
) -> PostCritiquesResponse:
    supabase = db.client()

    auth.authenticate_team_or_environment(
        supabase, params.team_name, params.environment_name, params.key
    )

    try:
        (
            supabase.table("workflows")
            .upsert(
                {
                    "team_name": params.team_name,
                    "environment_name": params.environment_name,
                    "name": params.workflow_name,
                }
            )
            .execute()
        )

        (
            supabase.table("agents")
            .upsert(
                {
                    "team_name": params.team_name,
                    "environment_name": params.environment_name,
                    "workflow_name": params.workflow_name,
                    "name": params.agent_name,
                }
            )
            .execute()
        )
        critique = (
            supabase.table("critiques")
            .upsert(
                {
                    "team_name": params.team_name,
                    "environment_name": params.environment_name,
                    "workflow_name": params.workflow_name,
                    "agent_name": params.agent_name,
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
        url=f"{PUBLIC_SITE_URL}/{params.team_name}/environments/{params.environment_name}/workflows/{params.workflow_name}/critiques/{id}",
        data=critique,
    )
