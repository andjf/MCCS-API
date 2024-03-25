from fastapi import FastAPI, APIRouter, Body, Depends
from datetime import datetime
from typing import Annotated

import logging
import warnings

from dotenv import dotenv_values

from big_query_client import BigQueryClient
from gen_ai import GenAI

logging.basicConfig(level=logging.INFO)

# Load environment variables into a dictionary
env = dotenv_values(".env")

def gen_ai_model() -> GenAI:
    return GenAI(
        api_key=env["GOOGLE_GEN_AI_API_KEY"],
        model_name=env["GOOGLE_GEN_AI_MODEL_NAME"],
        path_to_prompt=env["GEN_AI_PROMPT_PATH"],
    )

def big_query_client() -> BigQueryClient:
    return BigQueryClient(project=env["BIG_QUERY_PROJECT"])

# Ignore warnings about using end user credentials
warnings.filterwarnings("ignore", "authenticated using end user credentials")

app = FastAPI()

@app.get("/ping")
def ping():
    return {
        "message": "pong",
        "timestamp": datetime.now(),
    }

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/")
def query(
    action: Annotated[str, Body()],
    gen_ai: GenAI = Depends(gen_ai_model),
    big_query: BigQueryClient = Depends(big_query_client)
):
    model_generated_query = gen_ai.generate_query(
        PROJECT=env["BIG_QUERY_PROJECT"],
        DATASET=env["BIG_QUERY_DATASET"],
        ACTION=action,
    )
    return big_query.query(model_generated_query)

app.include_router(router)
