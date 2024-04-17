import logging

from google.cloud import bigquery

from app.env import env


class BigQueryClient:
    def __init__(self, project: str):
        self.client = bigquery.Client(project=project)
        self.logger = logging.getLogger(__name__)

    def query(self, query: str):
        self.logger.info(f"Executing query: {query}")
        raw_result = self.client.query(query).result()
        self.logger.info("Query executed successfully")
        result = [dict(row) for row in raw_result]
        self.logger.info(f"Respond with {len(result)} rows")
        return result


def get_big_query_client() -> BigQueryClient:
    return BigQueryClient(project=env["BIG_QUERY_PROJECT"])
