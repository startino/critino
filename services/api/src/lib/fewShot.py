import logging
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from pydantic import BaseModel
import os
import markdown

from src.lib import xml_utils


class ContextItem(BaseModel):
    name: str
    content: str
    index: int


class Critique(BaseModel):
    optimal: str
    context: list[ContextItem]


def format_one(critique: Critique) -> dict:
    output = markdown.markdown(critique.optimal)
    query_item = critique.context[-1]
    query = f"<{query_item.name}>{markdown.markdown(query_item.content)}</{query_item.name}>"
    context = [
        f"<{context_item.name}>{markdown.markdown(context_item.content)}</{context_item.name}>"
        for context_item in critique.context[:-1]
    ]
    return {
        "output": output,
        "query": query,
        "context": "\n".join(context),
    }


def format_critiques(critiques: list[Critique]) -> list[dict]:
    return [format_one(critique) for critique in critiques]


def few_shot_example_messages(critiques: list[Critique], query: str) -> str:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        logging.error("OPENAI_API_KEY is not set")
        raise ValueError("OPENAI_API_KEY is not set")

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    examples = format_critiques(critiques)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples=examples,
        embeddings=embeddings,
        vectorstore_cls=InMemoryVectorStore,
        k=2,
        input_keys=["query"],
    )

    examples = example_selector.select_examples({"query": query})

    example_prompt = PromptTemplate.from_template(
        "<example><context>{context}</context><query>{query}</query><output>{output}</output></example>"
    )
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        example_separator="",
        prefix="<examples>",
        suffix="</examples>",
    )
    formatval = few_shot_prompt.format()
    print("xml input:\n", formatval)
    print("xml output:\n", xml_utils.format_xml(formatval))
    return xml_utils.format_xml(formatval)


if __name__ == "__main__":
    examples = [
        Critique(
            optimal="This is the optimal output 1",
            context=[
                ContextItem(name="user", content="This is the context 1", index=0),
                ContextItem(
                    name="facilitator", content="This is the context 2", index=1
                ),
            ],
        ),
        Critique(
            optimal="This is the optimal output 2",
            context=[
                ContextItem(name="user", content="This is the context 1", index=0),
                ContextItem(
                    name="facilitator", content="This is the context 2", index=1
                ),
            ],
        ),
    ]

    query = "This is the query"

    few_shot_example_messages(examples, query)
