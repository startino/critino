import os
from pydantic import UUID4, BaseModel
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


@router.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.get("/critiques/ids")
def get_critique_ids() -> list[str]:
    supabase = db.client()
    response = supabase.table("critiques").select("id").execute()
    return [critique["id"] for critique in response.data]


class GetCritiquesRelevantRequest(BaseModel):
    query: str
    k: int = 4
    team_name: str
    project_name: str
    workflow_name: str | None = None
    agent_name: str | None = None


class GetCritiquesRelevantResult(BaseModel):
    critiques: list[StrippedCritique]
    examples: str


@router.get("/critiques/relevant")
def get_relevant_critiques(
    q: GetCritiquesRelevantRequest = Depends(),
) -> GetCritiquesRelevantResult:
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

    return GetCritiquesRelevantResult(
        critiques=relevant_critiques, examples=format_example_string(relevant_critiques)
    )


class PostCritiquesRequest(BaseModel):
    id: str
    context: str | None = None
    query: str | None = None
    optimal: str | None = None
    response: str | None = None
    team_name: str
    project_name: str
    workflow_name: str
    agent_name: str


@router.post("/critiques")
def upsert_a_critique(q: PostCritiquesRequest) -> str:
    supabase = db.client()

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

    return f"{PUBLIC_SITE_URL}/{q.team_name}/projects/{q.project_name}/workflows/{q.workflow_name}/{q.agent_name}/critiques/{q.id}"
