from typing import Annotated

from fastapi import APIRouter, Body, Depends

from clients.big_query_client import BigQueryClient, get_big_query_client
from clients.gen_ai_client import GenAIClient, get_gen_ai_client
from llm.service import execute_query_generate

import query.service as query_service

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/")
def query(
    sql_query: str,
    bq_client: BigQueryClient = Depends(get_big_query_client),
):
    return query_service.execute_query(sql_query, bq_client)


@router.post("/english")
def query(
    action: Annotated[str, Body()],
    gen_ai: GenAIClient = Depends(get_gen_ai_client),
    bq_client: BigQueryClient = Depends(get_big_query_client),
):
    return query_service.execute_query(
        execute_query_generate(action, gen_ai),
        bq_client,
    )
