import time
import logging
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests import Request

from src.routers import auth, critiques, index, environments
from src.routers.critiques_v1 import critiquesv1

load_dotenv()



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%M:%S",
)


def create_app() -> FastAPI:
    app = FastAPI()

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(end_time)
        return response

    app.include_router(index.router)
    app.include_router(auth.router)
    app.include_router(environments.router)
    app.include_router(critiques.router)
    app.include_router(critiquesv1.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()
