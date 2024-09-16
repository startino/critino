import logging
import os
from dotenv import load_dotenv
from supabase import create_client, Client


def client() -> Client:
    logging.debug("Creating Supabase client")
    load_dotenv()
    url: str | None = os.environ.get("PUBLIC_SUPABASE_URL")
    key: str | None = os.environ.get("PUBLIC_SUPABASE_ANON_KEY")

    if url is None or key is None:
        logging.error("PUBLIC_SUPABASE_URL and PUBLIC_SUPABASE_ANON_KEY must be set")
        raise ValueError("PUBLIC_SUPABASE_URL and PUBLIC_SUPABASE_ANON_KEY must be set")

    return create_client(url, key)
