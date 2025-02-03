import os
import logging
from pydantic import BaseModel
from typing import List,cast
from fastapi import HTTPException
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

os.environ["OPENAI_API_KEY"] = "your-api-key"

class CritiqueGeneratorRequest(BaseModel):
    input_type: str  
    input_source: str  
    context: str 
    query: str
    optimal_response: str

class CritiqueGeneratorResponse(BaseModel):
    context: str
    query: str
    optimal_response: str
    situation: str

class ContentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def process_youtube(self, url: str) -> List[str]:
        try:
            yt_loader = YoutubeLoader.from_youtube_url(
                url, add_video_info=False, language=["en", "en-US", "en-GB", "en-CA", "en-AU"]
            )
            transcript = yt_loader.load()
            return self.text_splitter.split_text(transcript[0].page_content)
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": "Error Processing YouTube Video", "error": str(e)})

    def process_documents(self, source: str) -> List[str]:
        try:
            loader = UnstructuredURLLoader(urls=[source])
            docs = loader.load()
            return self.text_splitter.split_text("\n".join([doc.page_content for doc in docs]))
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": "Error Processing Documents", "error": str(e)})

    def process_input(self, input_type: str, input_source: str) -> List[str]:
        if input_type == "youtube":
            return self.process_youtube(input_source)
        elif input_type in ["txt", "pdf", "docx"]:
            return self.process_documents(input_source)
        else:
            raise HTTPException(status_code=400, detail="Invalid input type or missing source")


class CritiqueProcessor:
    def __init__(self):
        self.model = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
        )
        self.content_processor = ContentProcessor()

    def generate_critique(self, request: CritiqueGeneratorRequest) -> List[CritiqueGeneratorResponse]:
        text_chunks = self.content_processor.process_input(request.input_type, request.input_source)
        critiques = []

        model_with_structured_output = self.model.with_structured_output(CritiqueGeneratorResponse)

        for chunk in text_chunks:
            prompt = ChatPromptTemplate([
                SystemMessage(content=f"""
                You are an expert AI critique assistant. Your task is to analyze the given content and provide detailed and constructive critiques in the specified Critino Format.
                You need to analyze the content and populate the fields/attributes in JSON according to the User-Defined Definations.

                ## User-Defined Definitions ##
                - context: {request.context}
                - query: {request.query}
                - optimal_response: {request.optimal_response}

                Each Critique output should follow this structured format as a valid JSON object:
                - context
                - query
                - optimal_response
                - situation: A brief (10 words max) summary describing the core theme of the critique.

                Only include these attributes in the JSON response.
                """),
                HumanMessage(content=f"Text Chunk: {chunk}\nAnalyze the text chunk and provide a structured critique.")
            ])

            try:
                response = cast(
                    CritiqueGeneratorResponse,
                    model_with_structured_output.invoke(prompt.invoke({}))
                )
                critique = response.model_dump_json(indent=4)
                critiques.append(critique)
            except Exception as e:
                logging.error(f"Failed to process critique: {e}")
                raise HTTPException(status_code=500, detail="LLM response error")

        return critiques
