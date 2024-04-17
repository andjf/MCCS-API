from typing import Callable
from clients.gen_ai_client import GenAIClient


from llm.transform import format_sql, remove_markdown_code_formatting
from functools import reduce

from env import env

TRANSFORMERS: list[Callable[[str], str]] = [
    remove_markdown_code_formatting,
    format_sql,
]

PROMPT_PATH = "prompts"


def execute_generate(prompt: str, gen_ai_client: GenAIClient):
    return gen_ai_client.generate(prompt).strip()


def execute_assistant_generate(question: str, gen_ai_client: GenAIClient):
    with open(f"{PROMPT_PATH}/assistant.txt", "r") as f:
        return execute_generate(f.read().format(question=question), gen_ai_client)


def execute_query_generate(plain_english_query: str, gen_ai_client: GenAIClient):
    with open(f"{PROMPT_PATH}/query.txt", "r") as f:
        return reduce(
            lambda x, f: f(x),
            TRANSFORMERS,
            execute_generate(
                f.read().format(
                    query=plain_english_query,
                    DATASET=env["BIG_QUERY_DATASET"],
                    PROJECT=env["BIG_QUERY_PROJECT"],
                ),
                gen_ai_client,
            ),
        )