from pydantic import BaseModel
from src.interfaces import db
from src.lib.few_shot import few_shot_example_messages, ContextItem, Critique

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


@router.get("/get_examples")
def get_examples() -> str:
    examples = [
        Critique(
            optimal="This is the optimal output 1",
            context=[
                ContextItem(name="user", content="This is the context 1", index=0),
                ContextItem(
                    name="facilitator", content="This is the context 2", index=1
                ),
            ],
        ),
    ]

    query = "This is the query"

    return few_shot_example_messages(examples, query)
    # supabase = db.client()
    # response = (
    #     supabase.table("critiques")
    #     .select("*")
    #     .eq("team_name", team)
    #     .eq("project_name", project)
    #     .eq("workflow_name", workflow)
    #     .eq("agent_name", agent)
    #     .execute()
    # )
    # return {
    #     "examples": "<examples></examples>",
    #     "critiques": [
    #         {
    #             "optimal": critique["optimal"],
    #             "query": critique["query"],
    #             "context": critique["context"],
    #         }
    #         for critique in response.data
    #     ],
    # }
