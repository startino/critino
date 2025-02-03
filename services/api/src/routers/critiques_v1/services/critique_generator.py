import os
import json
import requests
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from src.routers.critiques_v1.utils.youtube import get_transcript

from src.routers.critiques_v1.services.content_processor import chunk_content,chunk_content_streaming,chunk_content_string,chunk_content_streaming_string

from src.routers.critiques_v1.schemas import CritiqueRequest,CritiqueResponse
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logging.basicConfig(level=logging.DEBUG)

logging.basicConfig(level=logging.DEBUG)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=dict(os.environ)["GOOGLE_API_KEY"]
)

PROMPT_TEMPLATE = """You are a precise dialogue formatter. Format the given transcript chunk into a structured dialogue following these EXACT requirements:

<Transcript>
{chunk}
</Transcript>

FORMATTING RULES:

1. DIALOGUE STRUCTURE
   - Every piece of dialogue MUST be a complete, grammatical sentence
   - NO fragments, stutters, or run-on sentences
   - Format: <Speaker>One complete sentence.</Speaker>
   - Multiple sentences need separate tags: <Speaker>First sentence.</Speaker> <Speaker>Second sentence.</Speaker>

2. SPEAKER IDENTIFICATION
   - Use exact names when mentioned (e.g., "Mr. Sterling", "Dr. Goodrich")
   - Use clear roles when names aren't available (e.g., "Judge", "Attorney", "Defendant")
   - Use "Speaker 1" format for unidentified speakers
   - NEVER change a speaker's identifier within the same chunk

3. REQUIRED OUTPUT FORMAT
{{
    "context": "2-3 complete exchanges that set up the situation",
    "query": "Single complete statement/question requiring response",
    "optimal": "Professional 2-3 sentence response addressing the query"
}}

EXACT EXAMPLES:

CORRECT:
{{
    "context": "<Judge>The court has reviewed the psychiatric evaluation in detail.</Judge> <Mr. Sterling>Your Honor, I have crucial evidence to present.</Mr. Sterling> <Judge>The evidence must conform to court procedures.</Judge>",
    "query": "<Mr. Sterling>I request permission to call Francis as a witness to these events.</Mr. Sterling>",
    "optimal": "<Judge>The court cannot accept testimony from non-human entities as evidence.</Judge> <Judge>We must proceed based on admissible evidence and expert testimony only.</Judge>"
}}

INCORRECT FORMATS (DO NOT USE):
- Unclosed tags: <Judge>Text
- Missing periods: <Judge>This is a sentence</Judge>
- Fragments: <Judge>Well maybe if</Judge>
- Mixed speakers: <Judge>Text</Attorney>
- Run-on sentences: <Judge>And then he said and then I said and</Judge>

REQUIREMENTS CHECK:
1. Each tag pair must match exactly
2. Every sentence must end with a period
3. Each dialogue must be a complete thought
4. Optimal response must be 2-3 full sentences
5. All speakers must be consistently identified
6. No sentence fragments or run-ons allowed"""


parser = JsonOutputParser(pydantic_object=CritiqueResponse)
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
chain = prompt | llm | parser

def validate_tags(response: dict) -> bool:
    """Validate that all speaker tags are properly closed"""
    for field in ['context', 'query', 'optimal']:
        content = response.get(field, '')
        opening_tags = content.count('<')
        closing_tags = content.count('</') * 2  
        if opening_tags != closing_tags:
            return False
    return True

def download_file(url: str, filepath: str):
    """Downloads a file from a URL and saves it to the given filepath."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
        return False


@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def generate_critiques(request: CritiqueRequest, use_streaming=False) -> List[CritiqueResponse]:
    """Generate structured critiques, supporting both YouTube and online text files."""
    try:
        file_url = request.file_url
        transcript_file = None

        if file_url.startswith("http"):
            if file_url.endswith(".txt"):
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w+t', suffix='.txt', delete=False) as temp_file:
                    transcript_file = temp_file.name
                if not download_file(file_url, transcript_file):
                    raise ValueError("Failed to download transcript from URL.")

                with open(transcript_file, 'r', encoding='utf-8') as f:
                    transcript_content = f.read()

                if use_streaming:
                    chunks = chunk_content_streaming_string(transcript_content)
                else:
                    chunks = chunk_content_string(transcript_content)

            else:  # YouTube URL
                transcript = get_transcript(file_url)
                if transcript is None:
                    raise ValueError("Could not retrieve transcript from YouTube URL.")
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w+t', suffix='.json', delete=False) as temp_file:
                    transcript_file = temp_file.name
                    json.dump(transcript, temp_file)
                if use_streaming:
                    chunks = chunk_content_streaming(transcript_file)
                else:
                    chunks = chunk_content(transcript_file)

        else:  # Local file path
            transcript_file = file_url
            if use_streaming:
                chunks = chunk_content_streaming(transcript_file)
            else:
                chunks = chunk_content(transcript_file)

        if transcript_file:
            os.remove(transcript_file)

            logging.debug(f"Number of chunks (streaming={use_streaming}): {len(chunks)}")
            logging.debug(f"Chunks: {chunks}")  

            if chunks is None:
                raise ValueError("Transcript chunking failed.")

            critiques = []
            for chunk in chunks:
                logging.debug(f"Processing chunk: {chunk}")
                prompt_text = prompt.format(chunk=chunk)
                logging.debug(f"Prompt sent to LLM: {prompt_text}")

                try:
                    result = await asyncio.wait_for(chain.ainvoke({"chunk": chunk}), timeout=30.0)
                    logging.debug(f"LLM Result: {result}")

                    if not validate_tags(result):
                        logging.warning(f"Invalid tag structure in chunk: {chunk}")
                        continue

                    critiques.append(CritiqueResponse(**result))

                    await asyncio.sleep(0.5)

                except asyncio.TimeoutError:
                    logging.error(f"Chunk processing timed out: {chunk}")
                    continue
                except Exception as e:
                    logging.exception(f"Error processing chunk: {str(e)}")
                    continue

            return critiques
        else:
            raise ValueError("Invalid file URL or path provided.")

    except Exception as e:
        logging.exception(f"Critique generation failed: {str(e)}")
        raise RuntimeError(f"Critique generation failed: {str(e)}")