import traceback
import logging
from functools import wraps
import os
from typing import Annotated
from pydantic import AfterValidator, BaseModel
from src.interfaces import db
from src.lib.few_shot import (
    format_example_string,
    find_relevant_critiques,
    StrippedCritique,
)

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()

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


@router.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.get("/critiques/ids")
def get_critique_ids() -> list[str]:
    supabase = db.client()
    response = supabase.table("critiques").select("id").execute()
    return [critique["id"] for critique in response.data]


class PostCritiquesRelevantRequest(BaseModel):
    query: str
    k: int = 4
    team_name: str
    project_name: str
    workflow_name: str | None = None
    agent_name: str | None = None


class PostCritiquesRelevantResult(BaseModel):
    critiques: list[StrippedCritique]
    examples: str


@router.post("/critiques/relevant")
@ahandle_error
async def post_relevant_critiques(
    q: PostCritiquesRelevantRequest,
) -> PostCritiquesRelevantResult:
    if (q.agent_name is not None) and (q.workflow_name is None):
        raise HTTPException(
            status_code=400,
            detail="If you provide an agent_name, you must also provide a workflow_name",
        )

    supabase = db.client()
    request = (
        supabase.table("critiques")
        .select("*")
        .eq("team_name", q.team_name)
        .eq("project_name", q.project_name)
    )

    if q.workflow_name is not None:
        request.eq("workflow_name", q.workflow_name)

    if q.agent_name is not None:
        request.eq("agent_name", q.agent_name)

    response = request.execute()

    critiques = [
        StrippedCritique(
            optimal=critique["optimal"],
            query=critique["query"],
            context=critique["context"],
        )
        for critique in response.data
    ]

    relevant_critiques = find_relevant_critiques(critiques, q.query, k=q.k)

    return PostCritiquesRelevantResult(
        critiques=relevant_critiques, examples=format_example_string(relevant_critiques)
    )


def check_empty(v: str):
    assert v != "", "must not be an empty string"
    return v


class PostCritiquesRequest(BaseModel):
    id: str
    context: str | None = None
    query: str | None = None
    optimal: str | None = None
    response: str | None = None
    team_name: Annotated[str, AfterValidator(check_empty)]
    project_name: Annotated[str, AfterValidator(check_empty)]
    workflow_name: Annotated[str, AfterValidator(check_empty)]
    agent_name: Annotated[str, AfterValidator(check_empty)]


@router.post("/critiques")
@ahandle_error
async def upsert_a_critique(q: PostCritiquesRequest) -> str:
    supabase = db.client()

    (
        supabase.table("projects")
        .upsert(
            {
                "team_name": q.team_name,
                "name": q.project_name,
            }
        )
        .execute()
    )

    (
        supabase.table("workflows")
        .upsert(
            {
                "team_name": q.team_name,
                "project_name": q.project_name,
                "name": q.workflow_name,
            }
        )
        .execute()
    )

    (
        supabase.table("agents")
        .upsert(
            {
                "team_name": q.team_name,
                "project_name": q.project_name,
                "workflow_name": q.workflow_name,
                "name": q.agent_name,
            }
        )
        .execute()
    )

    supabase.table("critiques").upsert(q.model_dump()).execute()

    return f"{PUBLIC_SITE_URL}/{q.team_name}/projects/{q.project_name}/workflows/{q.workflow_name}/critiques/{q.id}"
