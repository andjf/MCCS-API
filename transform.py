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


def single_line(query: str) -> str:
    """
    Given:
    SELECT *
    FROM table
    WHERE condition

    Returns:
    SELECT * FROM table WHERE condition
    """
    return " ".join(map(str.strip, query.split("\n"))).strip()
