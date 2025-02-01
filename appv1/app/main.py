from fastapi import FastAPI, HTTPException
from typing import List
from app.schemas import CritiqueRequest, CritiqueResponse
from app.services.critique_generator import generate_critiques


app = FastAPI()

@app.post("/critiques/", response_model=List[CritiqueResponse])
async def create_critiques(request: CritiqueRequest, use_streaming: bool = False): # Add use_streaming parameter
    try:
        return await generate_critiques(request, use_streaming)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")