import vertexai
from vertexai.language_models import TextGenerationModel

from app.env import env
from app.logging import create_logger

PARAMS = {
    "max_output_tokens": 2048,
    "temperature": 0.25,
    "top_p": 1,
}

SEP = "=" * 80


class GenAIClient:
    def __init__(
        self,
        project: str,
        region: str = "us-east4",
        model_name: str = "text-bison",
    ):
        self.logger = create_logger(__name__)
        vertexai.init(project=project, location=region)
        self.model = TextGenerationModel.from_pretrained(model_name)
        self.logger.info(
            "Initialized LLM ('%s') in Google Cloud project '%s' in region '%s'",
            model_name,
            project,
            region,
        )

    def generate(self, prompt: str) -> str:
        self.logger.info(
            "Generating content from prompt:\n%s\n%s\n%s\nand params\n%s\n%s\n%s",
            SEP,
            prompt,
            SEP,
            SEP,
            PARAMS,
            SEP,
        )
        response = self.model.predict(prompt, **PARAMS).text
        self.logger.info("Responded with:\n%s\n%s\n%s", SEP, response, SEP)
        return response


def get_gen_ai_client() -> GenAIClient:
    return GenAIClient(project=env["BIG_QUERY_PROJECT"])
