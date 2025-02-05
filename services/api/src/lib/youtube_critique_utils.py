import os
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from urllib.parse import urlparse
from docx import Document
import re

os.environ['GROQ_API_KEY'] = "groq_api_key" 

# Load AI model
chat_model = ChatGroq(model="gemma2-9b-it", groq_api_key=os.environ.get('GROQ_API_KEY'))

class CritiqueRequest(BaseModel):
    file_url: str
    definitions: Dict[str, str]

class CritiqueResponse(BaseModel):
    context: str
    query: str
    optimal: str
    situation: str

def clean_text(text: str) -> str:
    """Remove unwanted newlines and clean up the text."""
    # Replace multiple newlines with a single space
    text = re.sub(r'\n+', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fetch_text_from_url(url: str) -> str:
    """Fetches and processes text from various file types."""
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()

    try:
        response = requests.get(url)
        response.raise_for_status()

        if path.endswith(".txt"):
            return clean_text(response.text)
        elif "youtube.com" in url or "youtu.be" in url:
            video_id = parsed_url.query.split("v=")[-1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return clean_text(" ".join([entry["text"] for entry in transcript]))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

def split_text(text: str) -> List[str]:
    """Splits text into chunks while preserving XML tags."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ". ", " "],
        keep_separator=True
    )
    return [clean_text(chunk) for chunk in splitter.split_text(text)]

def generate_critiques(chunks: List[str], definitions: Dict[str, str]) -> List[Dict[str, str]]:
    """Generates critiques maintaining XML format in context."""
    critiques = []
    
    for chunk in chunks:
        prompt = f"""
        Given the following definitions and content:
        
        Definitions:
        - Context format: {definitions['context']}
        - Query format: {definitions['query']}
        - Optimal response format: {definitions['optimal']}
        
        Content to analyze: {chunk}
        
        Generate a critique with:
        1. Context: Use XML tags to separate speakers as specified
        2. Query: Include the last statement with speaker XML tags
        3. Optimal: Format as specified for Francis' response
        4. Situation: Provide a generic description for similarity searches
        """

        response = chat_model.invoke(prompt)
        
        # Clean and process the response
        critique = {
            "context": clean_text(definitions["context"]),
            "query": clean_text(definitions["query"]),
            "optimal": clean_text(definitions["optimal"]),
            "situation": clean_text("Team meeting with market research and marketing professionals")
        }
        critiques.append(critique)

    return critiques

async def generate_critique(request: CritiqueRequest):
    """Generates critiques from input file while maintaining XML formatting."""
    # Validate required fields in definitions
    required_fields = ["context", "query", "optimal"]
    if not all(field in request.definitions for field in required_fields):
        raise HTTPException(
            status_code=400,
            detail="Missing required fields in definitions"
        )

    # Process the input file
    text = fetch_text_from_url(request.file_url)
    if not text:
        raise HTTPException(
            status_code=400,
            detail="No text extracted from the provided file"
        )

    # Generate critiques
    chunks = split_text(text)
    critiques = generate_critiques(chunks, request.definitions)

    return critiques


