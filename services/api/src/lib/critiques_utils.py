import os
import logging
from langgraph.graph import StateGraph, END
from langchain_community.document_loaders import YoutubeLoader, PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from src.interfaces import llm
from typing import cast, TypedDict, List, Literal, Optional
from pydantic import BaseModel, Field
from urllib.parse import urlparse
from src.lib.types import GenerateCritiqueInput, GenerateCritiqueOutput


# Define the state schema
class GraphState(TypedDict):
    document_or_youtube_text: str | None
    chunks: List[str] | None
    user_input: GenerateCritiqueInput
    critiques: List[GenerateCritiqueOutput] | None


class CritiqueResponse(BaseModel):
    context: str = Field(
        ...,
        description="A detailed background of the conversation or content leading up to the query. This provides "
                    "necessary context to understand the nature of the discussion."
    )
    query: str = Field(
        ...,
        description="The specific statement, question, or input that triggered a response. It represents the direct "
                    "prompt to which an optimal reply should be formulated."
    )
    optimal: str = Field(
        ...,
        description="The ideal, most accurate, and contextually appropriate response to the given query. This is the "
                    "benchmark against which other responses are evaluated."
    )
    situation: str = Field(
        ...,
        description="A ~10 word description of the situation from the context and query. The situation should be "
                    "generic such that it's similarly worded to others since it's used for similarity search."
    )


def chunk_text(state: GraphState) -> GraphState:
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)

    if state["document_or_youtube_text"] is None:
        return {"chunks": None}

    return {"chunks": splitter.split_text(state["document_or_youtube_text"])}


# Function to generate critiques
def generate_critiques(state: GraphState) -> GraphState:
    if state["chunks"] is None:
        return {"critiques": None}

    critiques : List[str] = []
    for chunk in state["chunks"]:
        prompt = ChatPromptTemplate(
            [
                SystemMessage(
                    content="""" You are an advanced AI critique generator trained to analyze media content and
                    provide structured feedback based on user-defined criteria. Your task is to process the given
                    text chunk and generate multiple critiques adhering to the Critino format. Each critique should
                    be precise, actionable, and well-structured, ensuring clarity and relevance.

                    Follow this structured output:
                    - **Context**: Briefly summarize the surrounding information relevant to the critique.
                    - **Query**: The specific aspect being evaluated.
                    - **Optimal Response**: A well-crafted answer or correction based on best practices.
                    - **Situation**: A generalized version of the critique to enable similarity searches.

                    Ensure the critiques are objective, relevant, and maintain professional standards.
                    """
                ),
                HumanMessage(
                    content=f"""Analyze the following text chunk and generate structured critiques based on the Critino format.

                    **User-Defined Definitions:**
                    - **Context**: {state["user_input"].definitions.context}
                    - **Query**: {state["user_input"].definitions.query}
                    - **Optimal Response**: {state["user_input"].definitions.optimal}

                    **Text Chunk:**"
                    {chunk}
                    """
                )
            ]
        )
        model = llm.chat_open_router(model="gpt-4o", api_key="api-key")
        model_with_structured_output = model.with_structured_output(CritiqueResponse)

        response = cast(
            CritiqueResponse,
            model_with_structured_output.invoke(prompt.invoke({}))
        )
        critique = response.model_dump_json(indent=4)
        critiques.append(critique)

    return {"critiques": critiques}


def classify_url(url) -> Literal["youtube", "pdf", "docx", "txt", "unknown"]:
    parsed_url = urlparse(url)
    youtube_domains = ["www.youtube.com", "youtube.com", "youtu.be"]
    if parsed_url.netloc in youtube_domains:
        return "youtube"

    ext = os.path.splitext(parsed_url.path)[-1].lower()
    if ext in [".pdf", ".txt", ".docx"]:
        return ext[1:]  # remove dot
    return "unknown"


def process_url(state: GraphState) -> GraphState:
    file_url: Optional[str] = state.get("user_input", {}).file_url

    if not file_url:
        return {"document_or_youtube_text": None}

    file_type = classify_url(file_url)

    if file_type == "unknown":
        return {"document_or_youtube_text": None}

    try:
        loader = None
        if file_type == "youtube":
            loader = YoutubeLoader.from_youtube_url(
                file_url, add_video_info=False, language=["en", "id"], translation="en"
            )
        elif file_type == "pdf":
            loader = PyPDFLoader(file_url)
        elif file_type == "docx":
            loader = Docx2txtLoader(file_url)
        elif file_type == "txt":
            loader = TextLoader(file_url)

        if loader is None:
            return {"document_or_youtube_text": None}

        documents = loader.load()
        extracted_text = "\n".join([doc.page_content for doc in documents])

        return {"document_or_youtube_text": extracted_text}

    except Exception as e:
        logging.error(f"Error processing URL: {e}")
        return {"document_or_youtube_text": None}


def process_request(input_data: GenerateCritiqueInput) -> List[GenerateCritiqueOutput]:
    # Initialize workflow with state schema
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("process_url", process_url)
    workflow.add_node("create_chunks", chunk_text)
    workflow.add_node("generate_critiques", generate_critiques)

    # Set entry point and edges
    workflow.set_entry_point("process_url")
    workflow.add_edge("process_url", "create_chunks")
    workflow.add_edge("create_chunks", "generate_critiques")
    workflow.add_edge("generate_critiques", END)

    # Compile and run
    graph = workflow.compile()

    # Initialize with required state
    initial_state = {
        "user_input": input_data,
        "document_or_youtube_text": None,
        "chunks": None,
        "critiques": None
    }

    result = graph.invoke(initial_state)
    return result["critiques"]
