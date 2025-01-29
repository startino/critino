import logging
from typing import Literal
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from pydantic import BaseModel, SecretStr
import os

from src.lib import xml_utils


class StrippedCritique(BaseModel):
    context: str
    query: str
    optimal: str
    instructions: str
    situation: str


SimilarityKey = Literal["query", "situation", "context"]

embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


def find_relevant_critiques(
    critiques: list[StrippedCritique],
    similarity: str,
    k: int = 4,
    similarity_key: SimilarityKey = "query",
) -> list[StrippedCritique]:
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        [critique.model_dump() for critique in critiques],
        embeddings,
        InMemoryVectorStore,
        k=k,
        input_keys=[similarity_key],
    )

    return [
        StrippedCritique(**critique)
        for critique in example_selector.select_examples({similarity_key: similarity})
    ]
