from app.clients.big_query_client import BigQueryClient
from app.env import env
from app.transform import format_sql


def execute_query(sql_query: str, bq_client: BigQueryClient):
    return bq_client.query(sql_query)


def page_query(page: int, page_size: int):
    return f"LIMIT {page_size} OFFSET {page_size * (page - 1)}"


def get_data_for_command_code(
    command_code: str,
    page: int,
    page_size: int,
    bq_client: BigQueryClient,
):
    query = format_sql(
        f"""
        SELECT *
        FROM `{env['BIG_QUERY_PROJECT']}.{env['BIG_QUERY_DATASET']}.inventory_adjustment`
        WHERE COMMAND_CD = '{command_code.strip().upper()}'
        {page_query(page, page_size)}
        """,
    )
    return execute_query(query, bq_client)
