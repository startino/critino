from pydantic import BaseModel


class Definitions(BaseModel):
    context: str
    query: str
    optimal: str


class GenerateCritiqueConfig(BaseModel):
    chunk_size: int
    chunk_overlap: int


class GenerateCritiqueInput(BaseModel):
    file_url: str
    config: GenerateCritiqueConfig
    definitions: Definitions


class GenerateCritiqueOutput(BaseModel):
    context: str
    query: str
    optimal: str
    situation: str
