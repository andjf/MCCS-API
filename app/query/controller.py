from typing import Annotated

from fastapi import APIRouter, Body, Depends

import app.query.service as query_service
from app.clients.big_query_client import BigQueryClient, get_big_query_client
from app.clients.gen_ai_client import GenAIClient, get_gen_ai_client
from app.llm.service import execute_query_generate

query_router = APIRouter(prefix="/query", tags=["Query"])
data_router = APIRouter(prefix="/query/data", tags=["Data Query"])


@query_router.post("/")
def query(
    query: Annotated[
        str,
        Body(
            description="The query to execute.",
            media_type="text/plain",
        ),
    ],
    bq_client: BigQueryClient = Depends(get_big_query_client),
):
    return query_service.execute_query(query, bq_client)


@query_router.post("/english")
def query(
    action: Annotated[
        str,
        Body(
            description="The action to execute.",
            media_type="text/plain",
        ),
    ],
    gen_ai: GenAIClient = Depends(get_gen_ai_client),
    bq_client: BigQueryClient = Depends(get_big_query_client),
):
    return query_service.execute_query(
        execute_query_generate(action, gen_ai),
        bq_client,
    )


@query_router.get("/command-code/{command_code}")
def get_data_for_command_code(
    command_code: str,
    bq_client: BigQueryClient = Depends(get_big_query_client),
    page: int = 1,
    page_size: int = 25,
):
    return query_service.get_data_for_command_code(
        command_code,
        page,
        page_size,
        bq_client,
    )
