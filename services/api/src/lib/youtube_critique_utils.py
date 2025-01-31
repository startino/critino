import os
from typing import List, Optional

import requests
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi

# Set up environment variable for Grok API key
os.environ["GROQ_API_KEY"] = "groq_api_key"
os.environ["GOOGLE_API_KEY"] = "gemini_api_key"


# Load Google Generative AI model
chat_model = ChatGroq(model="gemma2-9b-it", groq_api_key=os.environ["GROQ_API_KEY"])
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


class CritiqueRequest(BaseModel):
    context: str
    query: str
    optimal_response: str
    youtube_url: Optional[str] = None
    # document: Optional[str] = None  # Base64-encoded string or text conten


class CritiqueResponse(BaseModel):
    context: str
    query: str
    optimal_response: str
    situation: str
    critiques: List[str]


def fetch_youtube_transcript(url):
    url = url.split("v=")
    if "&" in url[1]:
        url = url[1].split("&")
        url = url[0]

    else:
        url = url[1]

    trans = YouTubeTranscriptApi.get_transcript(url)
    sa = []
    for i in range(len(trans)):
        sa.append(trans[i]["text"])

    sa = "".join(sa)
    text = sa.replace("\xa0", " ").replace("\n", " ").strip()
    return text


def split_text(text: str) -> List[str]:
    """Splits text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_text(text)


def generate_critiques(
    chunks: List[str], context: str, query: str, optimal_response: str
) -> List[str]:
    """Generates critiques for text chunks using LangChain Google Generative AI."""
    critiques = []
    for chunk in chunks:
        prompt = f"""
        Context: {context}\n
        Query: {query}\n
        Optimal Response: {optimal_response}\n
        Situation: {chunk}\n
        Generate a structured critique based on the provided information.
        """
        response = chat_model.invoke(prompt)
        critiques.append(response.content)
    return critiques


def generate_critique(request: CritiqueRequest):
    print(request)
    text = ""
    if request.youtube_url:
        text = fetch_youtube_transcript(request.youtube_url)
    elif request.document:
        text = request.document

    chunks = split_text(text)
    print(chunks)
    critiques = generate_critiques(
        chunks, request.context, request.query, request.optimal_response
    )

    return CritiqueResponse(
        context=request.context,
        query=request.query,
        optimal_response=request.optimal_response,
        situation="Generated critiques based on input text.",
        critiques=critiques,
    )
