import logging
from typing import Literal
from langchain_core.example_selectors import SemanticSimilarityExampleSelector

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from src.models.critique import Critique, CrtitiqueWithSituation

SimilarityKey = Literal["query", "situation"]

embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


def find_relevant_critiques(
    critiques: list[CrtitiqueWithSituation],
    similarity: str,
    k: int = 4,
    similarity_key: SimilarityKey = "query",
) -> list[Critique]:
    logging.info(
        f"find_relevant_critiques: similarity: {similarity} - k: {k} - similarity_key: {similarity_key}"
    )
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        [critique.model_dump() for critique in critiques],
        embeddings,
        InMemoryVectorStore,
        k=k,
        input_keys=[similarity_key],
    )

    return [
        Critique(**critique)
        for critique in example_selector.select_examples({similarity_key: similarity})
    ]
