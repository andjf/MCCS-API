from functools import reduce
from json import dumps as to_json
from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, Query, Response
from google.api_core.exceptions import BadRequest

import app.query.service as query_service
from app.clients.big_query_client import BigQueryClient, get_big_query_client
from app.clients.gen_ai_client import GenAIClient, get_gen_ai_client
from app.llm.service import execute_query_generate
from app.logging import create_logger

query_router = APIRouter(prefix="/query", tags=["Query"])
data_router = APIRouter(prefix="/query/data", tags=["Data Query"])

logger = create_logger(__name__)


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
        result = query_service.execute_query(
            execute_query_generate(action, gen_ai),
            bq_client,
        )
        if type(result) == list:
            if len(result) == 1:
                return result[0]
            elif all(type(data) == dict for data in result):
                dictionary_keys = [list(data.keys()) for data in result]
                if all(len(keys) == 1 for keys in dictionary_keys):
                    single_key: str | None = reduce(
                        lambda x, y: x if x == y else None,
                        [keys[0] for keys in dictionary_keys],
                    )
                    if single_key:
                        logger.info(
                            "All rows returned have a single column: %s", single_key
                        )
                        formatted_single_key = single_key.replace("_", " ").title()
                        comma_sep_values = ", ".join(
                            [data[single_key] for data in result]
                        )
                        return f"{formatted_single_key} Values: {comma_sep_values}"
        return result
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
