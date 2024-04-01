import logging
from datetime import datetime
from typing import Annotated

from dotenv import dotenv_values
from fastapi import APIRouter, Body, Depends, FastAPI
from fastapi.responses import FileResponse
import uvicorn

from big_query_client import BigQueryClient
from gen_ai import GenAI

logging.basicConfig(level=logging.INFO)

# Load environment variables into a dictionary
env = dotenv_values(".env")


def gen_ai_model() -> GenAI:
    return GenAI(project=env["BIG_QUERY_PROJECT"])


def big_query_client() -> BigQueryClient:
    return BigQueryClient(project=env["BIG_QUERY_PROJECT"])


app = FastAPI()


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
def home():
    return {
        "status": "up",
        "timestamp": datetime.now(),
    }


router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/")
def query(
    action: Annotated[str, Body()],
    gen_ai: GenAI = Depends(gen_ai_model),
    big_query: BigQueryClient = Depends(big_query_client),
):
    model_generated_query = gen_ai.generate_query(
        PROJECT=env["BIG_QUERY_PROJECT"],
        DATASET=env["BIG_QUERY_DATASET"],
        ACTION=action,
    )
    return big_query.query(model_generated_query)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
