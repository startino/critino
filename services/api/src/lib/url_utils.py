import urllib.parse


def sluggify(s: str) -> str:
    return urllib.parse.quote(s.lower().replace(" ", "-"))
