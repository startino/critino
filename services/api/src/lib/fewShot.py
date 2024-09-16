from langchain.core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.core.example_selectors import SemanticSimilarityExampleSelector
from langchain.openai import OpenAIEmbeddings
from langchain.vectorstores.memory import MemoryVectorStore
from pydantic import BaseModel
from typing import List, Optional
import os
import markdown

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)


class ContextItem(BaseModel):
    name: str
    content: str
    index: int


class Critique(BaseModel):
    optimal: str
    context: List[ContextItem]


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


def format_critiques(critiques: List[Critique]) -> List[dict]:
    return [format_one(critique) for critique in critiques]


async def few_shot_example_messages(critiques: List[Critique], query: str) -> str:
    examples = format_critiques(critiques)
    print("examples", examples)
    example_selector = await SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        MemoryVectorStore,
        {
            "k": 2,
        },
    )
    print("test1")
    example_prompt = PromptTemplate.from_template(
        "<example><context>{context}</context><query>{query}</query><output>{output}</output></example>"
    )
    print("test2")
    few_shot_prompt = FewShotPromptTemplate(
        {
            "example_selector": example_selector,
            "example_prompt": example_prompt,
            "example_separator": "",
            "prefix": "<examples>",
            "suffix": "</examples>",
            "input_variables": ["query"],
        }
    )
    print("test3")
    formatval = await few_shot_prompt.format({"query": query})
    print("test4")
    print("xml input:\n", formatval)
    return formatval
