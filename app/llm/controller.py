from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.clients.gen_ai_client import GenAIClient, get_gen_ai_client

from .service import execute_assistant_generate, execute_query_generate

router = APIRouter(prefix="/generate", tags=["LLM"])


@router.post("/assistant")
def generate(
    question: Annotated[str, Body(description="The text to generate from.")],
    gen_ai_client: GenAIClient = Depends(get_gen_ai_client),
):
    return execute_assistant_generate(question, gen_ai_client)


@router.post("/query")
def generate(
    plaintext_query: Annotated[str, Body(description="The text to generate from.")],
    gen_ai_client: GenAIClient = Depends(get_gen_ai_client),
):
    return execute_query_generate(plaintext_query, gen_ai_client)
