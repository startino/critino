from pydantic import BaseModel
from typing import List

class CritiqueComponents(BaseModel):
    context: str  # Full conversation history with XML speaker tags
    query: str     # Specific question/statement with XML speaker tag
    optimal: str   # Ideal response with XML speaker tag

class CritiqueRequest(BaseModel):
    file_url: str
    definitions: CritiqueComponents

class CritiqueResponse(CritiqueComponents):
    pass