from google.cloud import bigquery
import logging


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
