from clients.big_query_client import BigQueryClient


def execute_query(sql_query: str, bq_client: BigQueryClient):
    return bq_client.query(sql_query)
