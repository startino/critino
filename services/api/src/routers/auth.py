import os
from typing import Annotated
from pydantic import AfterValidator, BaseModel
from src.interfaces import db

from fastapi import APIRouter, Depends, Header
from src.lib import auth
from src.lib import validators as vd

router = APIRouter(prefix="/auth")


class GetAuthResponse(BaseModel):
    status: int
    detail: str


@router.get("/team/{name}")
async def authenticate_team(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    x_critino_key: Annotated[str, Header()],
) -> GetAuthResponse:
    supabase = db.client()

    auth.authenticate_team(supabase, name, x_critino_key)
    return GetAuthResponse(status=200, detail="Authorized.")


class GetEnvironmentQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


@router.get("/environment/{name}")
async def authenticate_environment(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    query: Annotated[GetEnvironmentQuery, Depends(GetEnvironmentQuery)],
    x_critino_key: Annotated[str, Header()],
) -> GetAuthResponse:
    if query.parent_name:
        if query.parent_name not in name:
            name = f"{query.parent_name}/{name}"

    supabase = db.client()

    auth.authenticate_team_or_environment(
        supabase, query.team_name, name, x_critino_key
    )
    return GetAuthResponse(status=200, detail="Authorized.")
