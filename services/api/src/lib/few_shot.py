import logging
from langchain_core import vectorstores
from langchain_core.documents import Document
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from pydantic import BaseModel, SecretStr
import os
import markdown

from src.lib import xml_utils


class StrippedCritique(BaseModel):
    context: str
    query: str
    optimal: str


def format_critiques(critiques: list[StrippedCritique]) -> list[dict]:
    return [
        {
            "context": critique.context,
            "query": critique.query,
            "optimal": critique.optimal,
        }
        for critique in critiques
    ]


def few_shot_example_messages(
    critiques: list[StrippedCritique], query: str, k: int = 4
) -> dict:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        logging.error("OPENAI_API_KEY is not set")
        raise ValueError("OPENAI_API_KEY is not set")
    OPENAI_API_KEY = SecretStr(OPENAI_API_KEY)

    examples = format_critiques(critiques)
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        InMemoryVectorStore,
        k=k,
        input_keys=["query"],
    )

    examples = example_selector.select_examples({"query": query})

    example_prompt = PromptTemplate.from_template(
        "<example><context>{context}</context><query>{query}</query><output>{optimal}</output></example>"
    )

    few_shot = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        example_separator="",
        prefix="<examples>",
        suffix="</examples>",
    ).format()

    return {"string": few_shot, "examples": examples}
