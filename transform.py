import sqlparse


def remove_markdown_code_formatting(markdown: str) -> str:
    """
    Given:
    ```sql
    [code here]
    ```

    Returns:
    [code here]
    """
    return markdown.replace("```sql", "").replace("```", "").strip()


def format_sql(query: str) -> str:
    """Given a SQL query, return a formatted version of the query."""
    return sqlparse.format(
        query,
        reindent=True,
        keyword_case="upper",
        strip_comments=True,
    )
