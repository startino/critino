import traceback
import logging
from functools import wraps
import os
from typing import Annotated
from pydantic import AfterValidator, BaseModel
from src.interfaces import db
from supabase import PostgrestAPIError

from fastapi import APIRouter, Depends, HTTPException, Header
from src.lib import auth, keys
from src.lib import validators as vd

router = APIRouter(prefix="/environments")

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
                status_code=500, detail={**e.__dict__, "traceback": tb_str}
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
                status_code=500, detail={**e.__dict__, "traceback": tb_str}
            )

    return wrapper


class GetEnvironmentsQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class GetEnvironmentsResponse(BaseModel):
    data: list
    count: int


@router.get("")
@ahandle_error
async def list_environments(
    query: Annotated[GetEnvironmentsQuery, Depends(GetEnvironmentsQuery)],
    x_critino_key: Annotated[str, Header()],
) -> GetEnvironmentsResponse:
    supabase = db.client()

    auth.authenticate_team(supabase, query.team_name, x_critino_key)

    try:
        environments = (
            supabase.table("environments")
            .select("*")
            .eq("team_name", query.team_name)
            .eq("parent_name", query.parent_name)
            .execute()
            .data
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    return GetEnvironmentsResponse(
        data=environments,
        count=len(environments),
    )


class PostEnvironmentQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class PostEnvironmentBody(BaseModel):
    description: str = ""
    gen_key: bool = False


class PostEnvironmentResponse(BaseModel):
    data: dict
    key: str | None


@router.post("/{name}")
@ahandle_error
async def create_environment(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    body: PostEnvironmentBody,
    query: Annotated[PostEnvironmentQuery, Depends(PostEnvironmentQuery)],
    x_critino_key: Annotated[Annotated[str, AfterValidator(vd.str_empty)], Header()],
) -> PostEnvironmentResponse:
    supabase = db.client()

    if query.parent_name:
        if query.parent_name not in name:
            name = f"{query.parent_name}/{name}"

    if not query.parent_name:
        auth.authenticate_team(supabase, query.team_name, x_critino_key)
    else:
        auth.authenticate_team_or_environment(
            supabase, query.team_name, query.parent_name, x_critino_key
        )

    key: str | None = None
    encrypted: str | None = None
    if body.gen_key:
        key_response = keys.gen_key("env")
        key = key_response.key
        encrypted = key_response.encrypted

    try:
        environment = (
            supabase.table("environments")
            .insert(
                {
                    "team_name": query.team_name,
                    "parent_name": query.parent_name,
                    "name": name,
                    "description": body.description,
                    "key": encrypted,
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

    return PostEnvironmentResponse(
        key=key,
        data=environment,
    )


class PatchEnvironmentQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class PatchEnvironmentBody(BaseModel):
    description: str = ""


class PatchEnvironmentResponse(BaseModel):
    data: dict


@router.patch("/{name}")
@ahandle_error
async def update_environment(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    body: PostEnvironmentBody,
    query: Annotated[PostEnvironmentQuery, Depends(PostEnvironmentQuery)],
    x_critino_key: Annotated[Annotated[str, AfterValidator(vd.str_empty)], Header()],
) -> PatchEnvironmentResponse:
    supabase = db.client()

    if query.parent_name:
        if query.parent_name not in name:
            name = f"{query.parent_name}/{name}"

    if not query.parent_name:
        auth.authenticate_team(supabase, query.team_name, x_critino_key)
    else:
        auth.authenticate_team_or_environment(
            supabase, query.team_name, query.parent_name, x_critino_key
        )

    try:
        environment = (
            supabase.table("environments")
            .update(
                {
                    "description": body.description,
                }
            )
            .eq("team_name", query.team_name)
            .eq("parent_name", query.parent_name)
            .eq("name", name)
            .execute()
            .data[0]
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    return PatchEnvironmentResponse(
        data=environment,
    )


class PatchEnvironmentKeyQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class PatchEnvironmentKeyResponse(BaseModel):
    data: dict
    key: str | None


@router.patch("/{name}/key")
@ahandle_error
async def update_environment_key(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    query: Annotated[PatchEnvironmentKeyQuery, Depends(PatchEnvironmentKeyQuery)],
    x_critino_key: Annotated[Annotated[str, AfterValidator(vd.str_empty)], Header()],
) -> PatchEnvironmentKeyResponse:
    supabase = db.client()

    if query.parent_name:
        if query.parent_name not in name:
            name = f"{query.parent_name}/{name}"

    if not query.parent_name:
        auth.authenticate_team(supabase, query.team_name, x_critino_key)
    else:
        auth.authenticate_team_or_environment(
            supabase, query.team_name, query.parent_name, x_critino_key
        )

    key_response = keys.gen_key("env")
    key = key_response.key
    encrypted = key_response.encrypted

    try:
        environment = (
            supabase.table("environments")
            .update(
                {
                    "key": encrypted,
                }
            )
            .eq("team_name", query.team_name)
            .eq("parent_name", query.parent_name)
            .eq("name", name)
            .execute()
            .data[0]
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    return PatchEnvironmentKeyResponse(
        key=key,
        data=environment,
    )


class DeleteEnvironmentKeyResponse(BaseModel):
    data: dict
    key: str | None


@router.delete("/{name}/key")
@ahandle_error
async def delete_environment_key(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    query: Annotated[PatchEnvironmentKeyQuery, Depends(PatchEnvironmentKeyQuery)],
    x_critino_key: Annotated[Annotated[str, AfterValidator(vd.str_empty)], Header()],
) -> DeleteEnvironmentKeyResponse:
    supabase = db.client()

    if query.parent_name:
        if query.parent_name not in name:
            name = f"{query.parent_name}/{name}"

    if not query.parent_name:
        auth.authenticate_team(supabase, query.team_name, x_critino_key)
    else:
        auth.authenticate_team_or_environment(
            supabase, query.team_name, query.parent_name, x_critino_key
        )

    try:
        environment = (
            supabase.table("environments")
            .update(
                {
                    "key": None,
                }
            )
            .eq("team_name", query.team_name)
            .eq("parent_name", query.parent_name)
            .eq("name", name)
            .execute()
            .data[0]
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    return DeleteEnvironmentKeyResponse(data=environment, key=None)


class GetEnvironmentQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class GetEnvironmentResponse(BaseModel):
    data: list[dict]


@router.get("/{name}")
@ahandle_error
async def read_environment(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    query: Annotated[GetEnvironmentQuery, Depends(GetEnvironmentQuery)],
    x_critino_key: Annotated[Annotated[str, AfterValidator(vd.str_empty)], Header()],
) -> GetEnvironmentResponse:
    supabase = db.client()

    if query.parent_name:
        if query.parent_name not in name:
            name = f"{query.parent_name}/{name}"

    auth.authenticate_team_or_environment(
        supabase, query.team_name, name, x_critino_key
    )

    try:
        environment = (
            supabase.table("environments")
            .select("*")
            .eq("team_name", query.team_name)
            .eq("parent_name", query.parent_name)
            .eq("name", name)
            .single()
            .execute()
            .data
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    return GetEnvironmentResponse(
        data=environment,
    )


class DeleteEnvironmentQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


@router.delete("/{name}")
@ahandle_error
async def delete_environment(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    query: Annotated[DeleteEnvironmentQuery, Depends(DeleteEnvironmentQuery)],
    x_critino_key: Annotated[str, Header()],
) -> None:
    supabase = db.client()

    if query.parent_name:
        if query.parent_name not in name:
            name = f"{query.parent_name}/{name}"

    if not query.parent_name:
        auth.authenticate_team(supabase, query.team_name, x_critino_key)
    else:
        auth.authenticate_team_or_environment(
            supabase, query.team_name, query.parent_name, x_critino_key
        )

    try:
        (
            supabase.table("environments")
            .delete()
            .eq("team_name", query.team_name)
            .eq("parent_name", query.parent_name)
            .eq("name", name)
            .execute()
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})
