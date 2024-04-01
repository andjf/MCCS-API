import logging
from functools import reduce
from typing import Callable

import vertexai
from vertexai.language_models import TextGenerationModel

from transform import remove_markdown_code_formatting, format_sql

TRANSFORMERS: list[Callable[[str], str]] = [
    remove_markdown_code_formatting,
    format_sql,
]

PARAMS = {
    "max_output_tokens": 2048,
    "temperature": 0.25,
    "top_p": 1,
}


class GenAI:
    def __init__(
        self,
        project: str,
        location: str = "us-east4",
        model_name: str = "text-bison",
        path_to_prompt: str = "./prompt.txt",
    ):
        vertexai.init(project=project, location=location)
        self.model = TextGenerationModel.from_pretrained(model_name)
        with open(path_to_prompt, "r") as f:
            self.raw_prompt = f.read()
        self.logger = logging.getLogger(__name__)

    def generate_content(self, **kwargs: dict) -> str:
        self.logger.info(f"Generating prompt with arguments: {kwargs}")
        prompt = self.raw_prompt.format(**kwargs)
        self.logger.info(f"Generating content with prompt: {prompt}")
        response = self.model.predict(prompt, **PARAMS).text
        self.logger.info(f"Generated content: {response}")
        return response

    def generate_query(self, **kwargs: dict) -> str:
        self.logger.info("Generating query")
        response = self.generate_content(**kwargs)
        return reduce(lambda a, t: t(a), TRANSFORMERS, response)
