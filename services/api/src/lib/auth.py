import logging
from fastapi import HTTPException
from supabase import PostgrestAPIError
from supabase._sync.client import SyncClient

from src.lib import keys


def authenticate_team(supabase: SyncClient, team_name: str, key: str):
    logging.info(f"Authenticating team: {team_name}")
    try:
        team_key = (
            supabase.table("teams")
            .select("key")
            .eq("name", team_name)
            .single()
            .execute()
        ).data["key"]
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    logging.info(f"Valid crypts: {[team_key]}")
    logging.info(f"Provided crypt: {keys.encrypt_key(key)}")
    logging.info(f"Provided key: {key}")
    if team_key != keys.encrypt_key(key):
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid key.")


def authenticate_team_or_environment(
    supabase: SyncClient, team_name: str, environment_name: str, key: str
):
    if team_name == "":
        raise HTTPException(status_code=401, detail="Unauthorized. Team Empty.")
    if environment_name == "":
        raise HTTPException(status_code=401, detail="Unauthorized. Environment Empty.")
    if key == "":
        raise HTTPException(status_code=401, detail="Unauthorized. Key Empty.")

    logging.info(f"Authenticating team: {team_name} or environment: {environment_name}")
    try:
        valid_keys = [
            (
                supabase.table("teams")
                .select("key")
                .eq("name", team_name)
                .single()
                .execute()
            ).data["key"]
        ]

        # Split the environment_name by '/'
        parts = environment_name.split("/")

        # Generate all possible prefixes
        prefixes = ["/".join(parts[: i + 1]) for i in range(len(parts))]

        # Query the database for all prefixes in a single call
        result = (
            supabase.table("environments")
            .select("key")
            .eq("team_name", team_name)
            .in_("name", prefixes)
            .execute()
        )

        # Extract the keys from the result
        valid_keys += [item["key"] for item in result.data]
    except PostgrestAPIError as e:
        logging.error(f"PostgrestAPIError: {e}")
        raise HTTPException(status_code=500, detail={**e.json()})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={**e.__dict__})

    logging.info(f"Valid crypts: {valid_keys}")
    logging.info(f"Provided crypt: {keys.encrypt_key(key)}")
    logging.info(f"Provided key: {key}")
    if keys.encrypt_key(key) not in valid_keys:
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid key.")
