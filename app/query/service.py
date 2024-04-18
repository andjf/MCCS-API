from typing import List

from app.clients.big_query_client import BigQueryClient
from app.env import env
from app.transform import format_sql


def execute_query(sql_query: str, bq_client: BigQueryClient):
    return bq_client.query(sql_query)


def page_query(page: int, page_size: int):
    return f"""
    ORDER BY ID ASC
    LIMIT {page_size}
    OFFSET {page_size * (page - 1)}
    """


def select_from(table_name: str):
    return f"""
    SELECT *
    FROM `{env['BIG_QUERY_DATASET']}.{table_name}`
    """


def filter_where(col: str, vals: List[str] | List[int]) -> str | None:
    if vals is None:
        return None
    if all(type(x) == str for x in vals):
        options = ", ".join(map(lambda val: f"'{val}'", vals))
        return f"{col} IN ({options})"
    return "(" + " OR ".join(map(lambda x: f"{col} = {x}", vals)) + ")"


def get_all_data(
    page: int,
    page_size: int,
    command_code_include: list[str] | None,
    site_id_include: list[int] | None,
    adjustment_category_include: list[str] | None,
    description_include: list[str] | None,
    division_include: list[str] | None,
    lob_description_include: list[str] | None,
    department_description_include: list[str] | None,
    class_include: list[str] | None,
    subclass_include: list[str] | None,
    merchandising_year_include: list[int] | None,
    merchandising_period_include: list[int] | None,
    period_include: list[str] | None,
    bq_client: BigQueryClient,
):
    filters = " AND ".join(
        filter(
            bool,
            map(
                lambda pair: filter_where(*pair),
                [
                    ("COMMAND_CD", command_code_include),
                    ("SITE_ID", site_id_include),
                    ("ADJUSTMENT_CATEGORY", adjustment_category_include),
                    ("DESCRIPTION", description_include),
                    ("DIVISION", division_include),
                    ("LOB_DESC", lob_description_include),
                    ("DEPT_DESC", department_description_include),
                    ("CLASS", class_include),
                    ("SUB_CLASS", subclass_include),
                    ("MERCHANDISING_YEAR", merchandising_year_include),
                    ("MERCHANDISING_PERIOD", merchandising_period_include),
                    ("PERIOD", period_include),
                ],
            ),
        )
    )

    query = format_sql(
        " ".join(
            [
                select_from("inventory_adjustment"),
                f"WHERE {filters}" if filters else "",
                page_query(page, page_size),
            ]
        ),
    )

    return execute_query(query, bq_client)


def get_data_for_command_code(
    command_code: str,
    page: int,
    page_size: int,
    bq_client: BigQueryClient,
):
    query = format_sql(
        f"""
        {select_from('inventory_adjustment')}
        WHERE COMMAND_CD = '{command_code.strip().upper()}'
        {page_query(page, page_size)}
        """,
    )
    return execute_query(query, bq_client)
