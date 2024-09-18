from pydantic import BaseModel
from src.interfaces import db
from src.lib.few_shot import (
    few_shot_example_messages,
    StrippedCritique,
)

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
def get_examples() -> dict:
    supabase = db.client()
    response = supabase.table("critiques").select("*").execute()
    critiques = [
        StrippedCritique(
            optimal=critique["optimal"],
            query=critique["query"],
            context=critique["context"],
        )
        for critique in response.data
    ]

    query = "This is the query"

    return few_shot_example_messages(critiques, query, k=4)
