from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, Query, Response
from google.api_core.exceptions import BadRequest

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
    try:
        return query_service.execute_query(
            execute_query_generate(action, gen_ai),
            bq_client,
        )
    except BadRequest as e:
        return Response(
            content=f"Error: {e.message}. Try rephrasing or simplifying your query.",
            status_code=e.code,
        )


@query_router.get("/all")
def get_data_for_command_code(
    bq_client: BigQueryClient = Depends(get_big_query_client),
    page: int = 1,
    page_size: int = 25,
    command_code_include: List[str] = Query(None),
    site_id_include: List[int] = Query(None),
    adjustment_category_include: List[str] = Query(None),
    description_include: List[str] = Query(None),
    division_include: List[str] = Query(None),
    lob_description_include: List[str] = Query(None),
    department_description_include: List[str] = Query(None),
    class_include: List[str] = Query(None),
    subclass_include: List[str] = Query(None),
    merchandising_year_include: List[int] = Query(None),
    merchandising_period_include: List[int] = Query(None),
    period_include: List[str] = Query(None),
):
    return query_service.get_all_data(
        page,
        page_size,
        command_code_include,
        site_id_include,
        adjustment_category_include,
        description_include,
        division_include,
        lob_description_include,
        department_description_include,
        class_include,
        subclass_include,
        merchandising_year_include,
        merchandising_period_include,
        period_include,
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
