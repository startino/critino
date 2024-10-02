import uuid
import hashlib
from pydantic import BaseModel


class GenKeyReturn(BaseModel):
    key: str
    encrypted: str


def encrypt_key(key: str) -> str:
    # Create SHA-256 hash
    sha256 = hashlib.sha256()
    sha256.update(key.encode("utf-8"))

    # Convert hash to hexadecimal string
    return sha256.hexdigest()


def gen_key(name: str) -> GenKeyReturn:

    # Generate two UUIDs and remove hyphens
    uuid1 = uuid.uuid4().hex
    uuid2 = uuid.uuid4().hex

    # Concatenate the UUIDs
    concatenated_uuids = uuid1 + uuid2

    # Create SHA-256 hash
    sha256 = hashlib.sha256()
    sha256.update(concatenated_uuids.encode("utf-8"))

    # Convert hash to hexadecimal string
    hex_digest = sha256.hexdigest()

    key = "sp-critino-" + name + "-" + hex_digest

    return GenKeyReturn(key=key, encrypted=encrypt_key(key))
