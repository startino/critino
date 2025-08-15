import logfire
from typing import Literal
from rapidfuzz import process, fuzz

# from langchain_core.example_selectors import SemanticSimilarityExampleSelector
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_core.vectorstores import InMemoryVectorStore

from src.models.critique import Critique, CritiqueWithSituation

SimilarityKey = Literal["query", "situation"]

# embeddings = HuggingFaceBgeEmbeddings(
#     model_name="BAAI/bge-small-en-v1.5",
#     model_kwargs={"device": "cpu"},
#     encode_kwargs={"normalize_embeddings": True},
# )


@logfire.instrument(
    "keyword_search: query: {query} - k: {k} - similarity_key: {similarity_key}"
)
def keyword_search(
    critiques: list[CritiqueWithSituation],
    query: str,
    k: int = 4,
    similarity_key: SimilarityKey = "query",
) -> list[Critique]:
    """
    Search using keyword search for the most similar 'situation' strings in CritiqueWithSituation.

    Args:
        critiques (list[CritiqueWithSituation]): List of Critiques potentially with `situation` key.
        query (str): The search query (situation-style wording).
        k (int): Max number of results to return.
        similarity_key (SimilarityKey): The key to use for similarity search.

    Returns:
        list[Critique]: List of Critique objects.
    """

    match similarity_key:
        case "query":
            data = [item.query for item in critiques]
        case "situation":
            logfire.info(
                f"keyword_search: query: {query} - k: {k} - similarity_key: {similarity_key}"
            )
            data = [item.situation for item in critiques]

    # Use rapidfuzz for partial/fuzzy match
    results = process.extract(
        query,
        data,
        scorer=fuzz.token_sort_ratio,  # You can try fuzz.ratio or fuzz.partial_ratio
        limit=k,
    )

    # Map results back to original dicts
    return [Critique(**critiques[idx].model_dump()) for _, _, idx in results]


# @logfire.instrument(
#     "similarity_search: query: {query} - k: {k} - similarity_key: {similarity_key}"
# )
# def similarity_search(
#     critiques: list[CritiqueWithSituation],
#     query: str,
#     k: int = 4,
#     similarity_key: SimilarityKey = "query",
# ) -> list[Critique]:
#     """
#     Search using similarity search for the most similar 'situation' strings in CritiqueWithSituation.
#
#     Args:
#         critiques (list[CritiqueWithSituation]): List of Critiques potentially with `situation` key.
#         query (str): The search query (situation-style wording).
#         k (int): Max number of results to return.
#         similarity_key (SimilarityKey): The key to use for similarity search.
#
#     Returns:
#         list[Critique]: List of Critique objects.
#     """
#
#     example_selector = SemanticSimilarityExampleSelector.from_examples(
#         [critique.model_dump() for critique in critiques],
#         embeddings,
#         InMemoryVectorStore,
#         k=k,
#         input_keys=[similarity_key],
#     )
#
#     return [
#         Critique(**critique)
#         for critique in example_selector.select_examples({similarity_key: query})
#     ]
