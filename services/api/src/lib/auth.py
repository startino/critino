import logging
from fastapi import HTTPException
from supabase import PostgrestAPIError
from supabase._sync.client import SyncClient

from src.lib import keys


def authenticate_team(supabase: SyncClient, team_name: str, key: str):
    try:
        team = (
            supabase.table("teams")
            .select("key")
            .eq("name", team_name)
            .single()
            .execute()
        )
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    if team.data["key"] != keys.encrypt_key(key):
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid key.")


def authenticate_team_or_environment(
    supabase: SyncClient, team_name: str, environment_name: str, key: str
):
    try:
        team_key = (
            supabase.table("teams")
            .select("key")
            .eq("name", team_name)
            .single()
            .execute()
        ).data["key"]

        environment_key = (
            supabase.table("environments")
            .select("key")
            .eq("team_name", team_name)
            .eq("name", environment_name)
            .single()
            .execute()
        ).data["key"]
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    if team_key != keys.encrypt_key(key) and environment_key != keys.encrypt_key(key):
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid key.")
