from fastapi import APIRouter, HTTPException
from src.routers.critiques_v1.schemas import CritiqueRequest
from src.routers.critiques_v1.services.critique_generator import generate_critiques


router = APIRouter(prefix="/critiquesv1")

@router.post("/")
async def create_critiques(request: CritiqueRequest, use_streaming: bool = False): 
    try:
        return await generate_critiques(request, use_streaming)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")