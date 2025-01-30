from pydantic import BaseModel


class Definitions(BaseModel):
    context: str
    query: str
    optimal: str


class GenerateCritiqueInput(BaseModel):
    file_url: str
    definitions: Definitions


class GenerateCritiqueOutput(BaseModel):
    context: str
    query: str
    optimal: str
    situation: str
