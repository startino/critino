import logging
import os
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

workers = {}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def redirect_to_docts():
    return RedirectResponse(url="/docs")


def run():
    try:
        PORT = os.environ.get("PORT")
        if not PORT:
            logging.info(
                "PORT not found in environment variables. Using default PORT=8000"
            )
            PORT = 8000

        PORT = int(PORT)
    except Exception:
        raise ValueError("PORT is not an integer")

    uvicorn.run(app, host="0.0.0.0", port=PORT, log_config="logging.yaml")


if __name__ == "__main__":
    run()
