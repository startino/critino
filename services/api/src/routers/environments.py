from datetime import datetime
import traceback
import logging
from functools import wraps
import os
from typing import Annotated
import urllib.parse
import uuid
from pydantic import AfterValidator, BaseModel
from src.interfaces import db
from supabase import PostgrestAPIError

from fastapi import APIRouter, Depends, HTTPException, Header
from src.lib import auth, keys
from src.lib import validators as vd

router = APIRouter(prefix="/environments")


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

    query.team_name = urllib.parse.unquote(query.team_name)
    # "/" is used for parent hirearchy, don't allow in the passed name
    if "/" in name:
        raise HTTPException(400, detail={"name": "Name cannot contain '/'"})
    if query.parent_name:
        query.parent_name = urllib.parse.unquote(query.parent_name)
        name = f"{query.parent_name}/{name}"

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

    query.team_name = urllib.parse.unquote(query.team_name)
    # "/" is used for parent hirearchy, don't allow in the passed name
    if "/" in name:
        raise HTTPException(400, detail={"name": "Name cannot contain '/'"})
    if query.parent_name:
        query.parent_name = urllib.parse.unquote(query.parent_name)
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


class DuplicateEnvironmentQuery(BaseModel):
    from_team_name: Annotated[str, AfterValidator(vd.str_empty)]
    from_parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class DuplicateEnvironmentResponse(BaseModel):
    data: dict


class DuplicateEnvironmentBody(BaseModel):
    # Until echoAI clients need their own team, the team name is the same as the from_team_name
    to_team_name: Annotated[str, AfterValidator(vd.str_empty)]
    to_parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None
    new_name: Annotated[str, AfterValidator(vd.str_empty)]
    gen_key: bool = False


@router.post("/{name}/duplicate")
@ahandle_error
async def duplicate_environment(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    body: DuplicateEnvironmentBody,
    query: Annotated[DuplicateEnvironmentQuery, Depends(DuplicateEnvironmentQuery)],
    x_critino_key: Annotated[Annotated[str, AfterValidator(vd.str_empty)], Header()],
) -> DuplicateEnvironmentResponse:
    """
    Duplicate an environment.

    This endpoint duplicates an environment and all its critiques.

    Currently, this endpoint is only safe for duplicating environments in the same team.

    Returns:
        The duplicated environment.
    """

    supabase = db.client()

    query.from_team_name = urllib.parse.unquote(query.from_team_name)
    # "/" is used for parent hirearchy, don't allow in the passed name
    if "/" in name:
        raise HTTPException(400, detail={"name": "Name cannot contain '/'"})
    if "/" in body.new_name:
        raise HTTPException(400, detail={"new_name": "New name cannot contain '/'"})
    
    if query.from_parent_name:
        query.from_parent_name = urllib.parse.unquote(query.from_parent_name)
        # At this point, name went from being just the last segment of the environment name to parent_name/name
        full_from_name = f"{query.from_parent_name}/{name}"

    if body.to_parent_name:
        body.to_parent_name = urllib.parse.unquote(body.to_parent_name)
        full_to_name = f"{body.to_parent_name}/{body.new_name}"

    # If echoAI clients need their own team, we'll need to handle the auth and checking of existing environments.
    if not query.from_parent_name:
        auth.authenticate_team(supabase, query.from_team_name, x_critino_key)
    else:
        auth.authenticate_team_or_environment(
            supabase, query.from_team_name, query.from_parent_name, x_critino_key,
        )

    try:
        environment = (
            supabase.table("environments")
            .select("*")
            .eq("team_name", query.from_team_name)
            .eq("parent_name", query.from_parent_name)
            .eq("name", full_from_name)
            .execute()
            .data[0]
        )
        critiques = (
            supabase.table("critiques")
            .select("*")
            .eq("team_name", query.from_team_name)
            .eq("environment_name", full_from_name)
            .execute()
            .data
        )

    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    if not environment:
        raise HTTPException(404, detail={"name": "Environment not found"})


    try:
        new_environment = (
            supabase.table("environments")
            .insert(
                {
                    "team_name": body.to_team_name,
                    "parent_name": body.to_parent_name,
                    "name": full_to_name,
                    "description": environment["description"],
                    "key": environment["key"],
                }
            )
            .execute()
            .data[0]
        )
        new_critiques = (
            supabase.table("critiques")
            .insert(
                [
                    {**critique, "id": str(uuid.uuid4()), "created_at": datetime.now().isoformat(), "team_name": body.to_team_name, "environment_name": full_to_name}
                    for critique in critiques
                ]
            )
            .execute()
            .data
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    return DuplicateEnvironmentResponse(
        data={
            "new_environment": new_environment,
            "new_critiques": new_critiques,
        },
    )


class PatchEnvironmentQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class PatchEnvironmentBody(BaseModel):
    data: dict = {}


class PatchEnvironmentResponse(BaseModel):
    data: dict


@router.patch("/{name}")
@ahandle_error
async def update_environment(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    body: PatchEnvironmentBody,
    query: Annotated[PatchEnvironmentQuery, Depends(PatchEnvironmentQuery)],
    x_critino_key: Annotated[Annotated[str, AfterValidator(vd.str_empty)], Header()],
) -> PatchEnvironmentResponse:
    supabase = db.client()

    query.team_name = urllib.parse.unquote(query.team_name)

    # "/" is used for parent hirearchy, don't allow in the passed name
    if "/" in name:
        raise HTTPException(400, detail={"name": "Name cannot contain '/'"})
    if query.parent_name:
        query.parent_name = urllib.parse.unquote(query.parent_name)
        name = f"{query.parent_name}/{name}"

    if not query.parent_name:
        auth.authenticate_team(supabase, query.team_name, x_critino_key)
    else:
        auth.authenticate_team_or_environment(
            supabase, query.team_name, query.parent_name, x_critino_key
        )

    # "/" is used for parent hirearchy, don't allow in the passed name
    if body.data["name"]:
        if "/" in body.data["name"]:
            raise HTTPException(400, detail={"name": "Name cannot contain '/'"})

        body.data["name"] = f"{query.parent_name}/{body.data['name']}"

    try:
        environment = (
            supabase.table("environments")
            .update(body.data)
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

    query.team_name = urllib.parse.unquote(query.team_name)

    # "/" is used for parent hirearchy, don't allow in the passed name
    if "/" in name:
        raise HTTPException(400, detail={"name": "Name cannot contain '/'"})
    if query.parent_name:
        query.parent_name = urllib.parse.unquote(query.parent_name)
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

    query.team_name = urllib.parse.unquote(query.team_name)
    # "/" is used for parent hirearchy, don't allow in the passed name
    if "/" in name:
        raise HTTPException(400, detail={"name": "Name cannot contain '/'"})
    if query.parent_name:
        query.parent_name = urllib.parse.unquote(query.parent_name)
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
    data: dict


@router.get("/{name}")
@ahandle_error
async def read_environment(
    name: Annotated[str, AfterValidator(vd.str_empty)],
    query: Annotated[GetEnvironmentQuery, Depends(GetEnvironmentQuery)],
    x_critino_key: Annotated[Annotated[str, AfterValidator(vd.str_empty)], Header()],
) -> GetEnvironmentResponse:
    supabase = db.client()

    query.team_name = urllib.parse.unquote(query.team_name)
    # "/" is used for parent hirearchy, don't allow in the passed name
    if "/" in name:
        raise HTTPException(400, detail={"name": "Name cannot contain '/'"})
    if query.parent_name:
        query.parent_name = urllib.parse.unquote(query.parent_name)
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

    query.team_name = urllib.parse.unquote(query.team_name)
    # "/" is used for parent hirearchy, don't allow in the passed name
    if "/" in name:
        raise HTTPException(400, detail={"name": "Name cannot contain '/'"})
    if query.parent_name:
        query.parent_name = urllib.parse.unquote(query.parent_name)
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
