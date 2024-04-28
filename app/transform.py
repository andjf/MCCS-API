import sqlparse

from app.logging import create_logger

logger = create_logger(__name__)


def remove_markdown_code_formatting(markdown: str) -> str:
    """
    Given:
    ```sql
    [code here]
    ```

    Returns:
    [code here]
    """
    result = markdown.replace("```sql", "").replace("```", "").strip()
    logger.info("remove_markdown_code_formatting: [%s] => [%s]", markdown, result)
    return result


def format_sql(query: str) -> str:
    """Given a SQL query, return a formatted version of the query."""
    result = sqlparse.format(
        query,
        reindent=True,
        keyword_case="upper",
        strip_comments=True,
    )
    logger.info("format_sql: [%s] => [%s]", query, result)
    return result
