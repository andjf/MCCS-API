from google.cloud import bigquery

from app.env import env
from app.logging import create_logger


class BigQueryClient:
    def __init__(self, project: str):
        self.logger = create_logger(__name__)
        self.client = bigquery.Client(project=project)
        self.logger.info(
            "Initialized BigQuery Client in Google Cloud project '%s'", project
        )

    def query(self, query: str):
        self.logger.info("Executing query:\n%s\n%s\n%s", "=" * 80, query, "=" * 80)
        raw_result = self.client.query(query).result()
        self.logger.info("Query executed successfully")
        result = [dict(row) for row in raw_result]
        self.logger.info("Respond with %d rows", len(result))
        return result


def get_big_query_client() -> BigQueryClient:
    return BigQueryClient(project=env["BIG_QUERY_PROJECT"])
