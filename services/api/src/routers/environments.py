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


class PostEnvironmentsQuery(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


class PostEnvironmentsBody(BaseModel):
    description: str = ""
    gen_key: bool = False


class PostEnvironmentsResponse(BaseModel):
    data: dict
    key: str | None


@router.post("/{name}")
@ahandle_error
async def create_environment(
    name: str,
    body: PostEnvironmentsBody,
    query: Annotated[PostEnvironmentsQuery, Depends(PostEnvironmentsQuery)],
    x_critino_key: Annotated[str, Header()],
) -> PostEnvironmentsResponse:
    supabase = db.client()

    auth.authenticate_team(supabase, query.team_name, x_critino_key)

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
                    "name": f"{query.parent_name + '/' if query.parent_name else ''}{name}",
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

    return PostEnvironmentsResponse(
        key=key,
        data=environment,
    )


class DeleteEnvironmentsParams(BaseModel):
    team_name: Annotated[str, AfterValidator(vd.str_empty)]
    parent_name: Annotated[str, AfterValidator(vd.str_empty)] | None = None


@router.delete("/{name}")
@ahandle_error
async def delete_environment(
    name: str,
    params: Annotated[DeleteEnvironmentsParams, Depends(DeleteEnvironmentsParams)],
    x_critino_key: Annotated[str, Header()],
) -> None:
    supabase = db.client()

    if not params.parent_name:
        auth.authenticate_team(supabase, params.team_name, x_critino_key)
    else:
        auth.authenticate_team_or_environment(
            supabase, params.team_name, params.parent_name, x_critino_key
        )

    try:
        (
            supabase.table("environments")
            .delete()
            .eq("team_name", params.team_name)
            .eq("parent_name", params.parent_name)
            .eq("name", name)
            .execute()
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})
