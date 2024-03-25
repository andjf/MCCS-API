import google.generativeai as genai
from typing import Callable
from transform import remove_markdown_code_formatting, single_line
import logging
from functools import reduce


class GenAI:

    TRANSFORMERS: list[Callable[[str], str]] = [
        remove_markdown_code_formatting,
        single_line,
    ]

    def __init__(self, api_key: str, model_name: str, path_to_prompt: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        with open(path_to_prompt, "r") as f:
            self.raw_prompt = f.read()
        self.logger = logging.getLogger(__name__)

    def generate_content(self, **kwargs: dict) -> str:
        self.logger.info(f"Generating prompt with arguments: {kwargs}")
        prompt = self.raw_prompt.format(**kwargs)
        self.logger.info(f"Generating content with prompt: {prompt}")
        response = self.model.generate_content(prompt).text
        self.logger.info(f"Generated content: {response}")
        return response

    def generate_query(self, **kwargs: dict) -> str:
        self.logger.info("Generating query")
        response = self.generate_content(**kwargs)
        return reduce(lambda a, t: t(a), self.TRANSFORMERS, response)
