import logging

import vertexai
from vertexai.language_models import TextGenerationModel

from env import env

PARAMS = {
    "max_output_tokens": 2048,
    "temperature": 0.25,
    "top_p": 1,
}


class GenAIClient:
    def __init__(
        self,
        project: str,
        location: str = "us-east4",
        model_name: str = "text-bison",
    ):
        vertexai.init(project=project, location=location)
        self.model = TextGenerationModel.from_pretrained(model_name)
        self.logger = logging.getLogger(__name__)

    def generate(self, prompt: str) -> str:
        return self.model.predict(prompt, **PARAMS).text


def get_gen_ai_client() -> GenAIClient:
    return GenAIClient(project=env["BIG_QUERY_PROJECT"])
