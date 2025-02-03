import os
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.utils.youtube import get_transcript
from app.services.content_processor import chunk_content
from app.schemas import CritiqueRequest, CritiqueResponse
from app.config import settings
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from app.services.content_processor import chunk_content, chunk_content_streaming # Import both
import json
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=""
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
        # Check if number of opening tags matches closing tags
        opening_tags = content.count('<')
        closing_tags = content.count('</') * 2  # Each closing tag has two brackets
        if opening_tags != closing_tags:
            return False
    return True
@retry(
    stop=stop_after_attempt(3), 
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def generate_critiques(request: CritiqueRequest, use_streaming=False) -> List[CritiqueResponse]: # Add use_streaming parameter
    """Generate structured critiques with robust error handling."""
    try:
        transcript = get_transcript(request.file_url)

        # Save transcript to a temp file for chunking
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+t', suffix='.json', delete=False) as temp_file:
            temp_file_name = temp_file.name
            json.dump(transcript, temp_file)  # Assuming transcript is a list of dicts
        if use_streaming:
          chunks = chunk_content_streaming(temp_file_name)  # Use streaming if needed
        else:
          chunks = chunk_content(temp_file_name) # Use file path instead of string.
        os.remove(temp_file_name) # Delete after used

        if chunks is None:  # Check for chunking errors
            raise ValueError("Transcript chunking failed.")
        critiques = []
        for chunk in chunks:
            try:
                # Add timeout to prevent indefinite waiting
                result = await asyncio.wait_for(
                    chain.ainvoke({"chunk": chunk}), 
                    timeout=30.0  # 30 seconds timeout
                )
                
                # Validate tag structure
                if not validate_tags(result):
                    print(f"Invalid tag structure in chunk: {chunk}")
                    continue
                
                critiques.append(CritiqueResponse(**result))
                
                # Small delay to prevent rate limiting
                await asyncio.sleep(0.5)
                
            except asyncio.TimeoutError:
                print(f"Chunk processing timed out: {chunk}")
                continue
            except Exception as e:
                print(f"Error processing chunk: {str(e)}")
                continue
        
        return critiques
    
    except Exception as e:
        raise RuntimeError(f"Critique generation failed: {str(e)}")
