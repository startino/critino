from src.interfaces import db

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.get("/critique-ids")
def get_critique_ids() -> list[str]:
    supabase = db.client()
    response = supabase.table("critiques").select("id").execute()
    return [critique["id"] for critique in response.data]


@router.get("/{team}/{project}/{workflow}/{agent}")
def get_examples(team: str, project: str, workflow: str, agent: str) -> dict:
    supabase = db.client()
    response = (
        supabase.table("critiques")
        .select("*")
        .eq("team_name", team)
        .eq("project_name", project)
        .eq("workflow_name", workflow)
        .eq("agent_name", agent)
        .execute()
    )
    return {
        "examples": "<examples></examples>",
        "critiques": [
            {
                "optimal": critique["optimal"],
                "query": critique["query"],
                "context": critique["context"],
            }
            for critique in response.data
        ],
    }
