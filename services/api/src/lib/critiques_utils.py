import json
import os
import logging
import requests
from tempfile import NamedTemporaryFile
from langgraph.graph import StateGraph, END
from sse_starlette import ServerSentEvent
from langchain_core.messages import (
    AIMessageChunk,
    AIMessage,
    BaseMessage,
    BaseMessageChunk,
    ToolMessage,
    message_to_dict,
)
from langchain_community.document_loaders import (
    YoutubeLoader,
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from src.interfaces import llm
from typing import cast, TypedDict, List, Literal, Optional
from pydantic import BaseModel, Field
from urllib.parse import urlparse
from src.lib.types import GenerateCritiqueInput, GenerateCritiqueOutput
from src.lib.constants import LANGUAGE_CODES


# Define the state schema
class GraphState(BaseModel):
    document_or_youtube_text: str | None
    chunk_size: int
    chunk_overlap: int
    chunks: List[str] | None
    user_input: GenerateCritiqueInput
    critiques: List[GenerateCritiqueOutput] | None


class CritiqueGenerator:
    def __init__(self, instructions, openrouter_api_key: str):
        self.openrouter_api_key = openrouter_api_key
        self.instructions = instructions
        self.url = None
        self.loader = None
        self.temp_file = None
        self.critiques = []
        self.model = llm.chat_open_router(
            model="google/gemini-2.0-flash-001",
            api_key=self.openrouter_api_key,
            temperature=0,
        )

    def chunk_text(self, state: GraphState):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=state.chunk_size, chunk_overlap=state.chunk_overlap
        )
        if state.document_or_youtube_text is None:
            return {"chunks": None}

        return {"chunks": self.splitter.split_text(state.document_or_youtube_text)}

    # Function to generate critiques
    def generate_critiques(self, state: GraphState):
        if state.chunks is None:
            return {"critiques": None}

        class CritiqueResponse(BaseModel):
            query: str = Field(
                ...,
                description=state.user_input.definitions.query,
            )
            optimal: str = Field(
                ...,
                description=state.user_input.definitions.optimal,
            )
            situation: str = Field(
                ...,
                description="A ~10 word description of the situation from the query. The situation should be "
                "generic such that it's similarly worded to others since it's used for similarity search. Do not mention specifics like names.",
            )

        for chunk in state.chunks:
            prompt = ChatPromptTemplate(
                [
                    SystemMessage(content=self.instructions),
                    HumanMessage(
                        content=f"""
**Follow this defined structure for the critiques:**
- **Query**: {state.user_input.definitions.query}
- **Optimal Response**: {state.user_input.definitions.optimal}
- **Situation**: A ~10 word description of the situation from the query. The situation should be generic such that it's similarly worded to others since it's used for similarity search. Do not mention specifics like names.

**Text Chunk:**"
{chunk}
                        """.strip()
                    ),
                ]
            )
            model_with_structured_output = self.model.with_structured_output(
                CritiqueResponse
            )

            response = cast(
                CritiqueResponse, model_with_structured_output.invoke(prompt.invoke({}))
            )
            critique = response.model_dump_json(indent=4)
            logging.info(f"critique: \n\n\n{critique}\n\n\n")
            self.critiques.append(critique)

        return {"critiques": self.critiques}

    def classify_url(self) -> Literal["youtube", "pdf", "docx", "txt", "unknown"]:
        parsed_url = urlparse(self.url)
        youtube_domains = ["www.youtube.com", "youtube.com", "youtu.be"]
        if parsed_url.netloc in youtube_domains:
            return "youtube"

        ext = os.path.splitext(parsed_url.path)[-1].lower()
        if ext in [".pdf", ".txt", ".docx"]:
            return ext[1:]  # remove dot
        return "unknown"

    def download_file(self):
        """Downloads a file from the given URL and saves it temporarily."""
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()  # Raise error for bad status codes

            ext = os.path.splitext(urlparse(self.url).path)[-1].lower()
            if ext in [".pdf", ".txt", ".docx"]:
                self.temp_file = NamedTemporaryFile(delete=False, suffix=ext)
                with open(self.temp_file.name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

        except requests.RequestException as e:
            logging.error(f"Failed to download file: {e}")

    def process_url(self, state: GraphState):
        self.url = state.user_input.file_url

        if not self.url:
            return {}

        file_type = self.classify_url()

        if file_type == "unknown":
            return {}

        try:
            if file_type == "youtube":
                self.loader = YoutubeLoader.from_youtube_url(
                    self.url,
                    add_video_info=False,
                    language=LANGUAGE_CODES,
                    translation="en",
                )
            else:
                self.download_file()
                logging.info(f"temp_file: {self.temp_file.name}")
                if not self.temp_file.name:
                    return {}
                if file_type == "pdf":
                    self.loader = PyPDFLoader(self.temp_file.name)
                elif file_type == "docx":
                    self.loader = Docx2txtLoader(self.temp_file.name)
                elif file_type == "txt":
                    self.loader = TextLoader(self.temp_file.name)

                if self.loader is None:
                    return {}

            documents = self.loader.load()
            extracted_text = "\n".join([doc.page_content for doc in documents])

            return {"document_or_youtube_text": extracted_text}

        except Exception as e:
            logging.error(f"Error processing URL: {e}")
            return {}

    async def process_request(self, input_data: GenerateCritiqueInput):
        # Initialize workflow with state schema
        workflow = StateGraph(GraphState)

        # Add nodes
        workflow.add_node("process_url", self.process_url)
        workflow.add_node("create_chunks", self.chunk_text)
        workflow.add_node("generate_critiques", self.generate_critiques)

        # Set entry point and edges
        workflow.set_entry_point("process_url")
        workflow.add_edge("process_url", "create_chunks")
        workflow.add_edge("create_chunks", "generate_critiques")
        workflow.add_edge("generate_critiques", END)

        # Compile and run
        graph = workflow.compile()

        # Initialize with required state
        initial_state = GraphState(
            user_input=input_data,
            document_or_youtube_text=None,
            chunks=None,
            critiques=None,
            chunk_size=input_data.config.chunk_size,
            chunk_overlap=input_data.config.chunk_overlap,
        )

        critiques_list = []

        async for event in graph.astream_events(
            initial_state.model_dump(), version="v2"
        ):
            kind, data = event["event"], event["data"]

            metadata = event.get("metadata", {})
            node = metadata.get("langgraph_node", None)

            input = data.get("input", None)

            match kind:
                case "on_parser_end":
                    if not node:
                        logging.error(f"workshop: no node found for event {kind}")
                        continue

                    logging.info(f"workshop: {node}: {kind}: parser end: {data}")
                    input = data.get("input", None)
                    output = data.get("output", None)

                    if isinstance(output, BaseModel):
                        output_string = output.model_dump_json()
                    elif isinstance(output, list):
                        output_string = json.dumps(output[0].get("args", None))
                        if not output_string:
                            logging.error(
                                f"workshop: output is list but missing args: output: {output}"
                            )
                            continue
                    else:
                        logging.error(
                            f"workshop: output is not a BaseModel or a list: output: {output}"
                        )
                        continue

                    if not isinstance(input, AIMessage):
                        logging.error(
                            f"workshop: input is not an AIMessage: input: {input}"
                        )
                        continue

                    yield ServerSentEvent(
                        data=output_string,
                        event="on_critique_end",
                    )

                    critiques_list.append(json.loads(output_string))

        # Yield the accumulated critiques in a final event
        yield ServerSentEvent(
            data=json.dumps(critiques_list),
            event="on_critiques_end",
        )
