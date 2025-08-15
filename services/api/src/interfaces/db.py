import logfire
import os
from dotenv import load_dotenv
from supabase import create_client, Client


def client() -> Client:
    logfire.debug("Creating Supabase client")
    load_dotenv()
    url: str | None = os.environ.get("PUBLIC_SUPABASE_URL")
    key: str | None = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

    if url is None or key is None:
        logfire.error("PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        raise ValueError("PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")

    return create_client(url, key)
