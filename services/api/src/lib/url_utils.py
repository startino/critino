import os
import urllib.parse

PUBLIC_SITE_URL = os.getenv("PUBLIC_SITE_URL", "http://0.0.0.0:5173")


def get_url(url=None):
    url = url or PUBLIC_SITE_URL
    url = url if "http" in url else f"https://{url}"
    url = url if url.endswith("/") else f"{url}/"
    return url


def sluggify(s: str) -> str:
    return urllib.parse.quote(s.lower().replace(" ", "-"))
