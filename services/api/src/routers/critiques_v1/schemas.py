from pydantic import BaseModel
from typing import List

class CritiqueComponents(BaseModel):
    context: str 
    query: str     
    optimal: str   

class CritiqueRequest(BaseModel):
    file_url: str
    definitions: CritiqueComponents

class CritiqueResponse(CritiqueComponents):
    pass