import os
from pydantic import BaseModel
from typing import List
from langchain_community.document_loaders import YoutubeLoader, TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from fastapi import HTTPException

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

llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
    )

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def process_youtube(url: str) -> List[str]:
    try:
        yt_loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
        transcript = yt_loader.load()
        return text_splitter.split_text(transcript[0].page_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail={"message":"Error Processing Youtube Video","error": str(e)})

def process_documents(input_type: str, source: str) -> List[str]:
    try:
        if input_type == "pdf":
            loader = PyPDFLoader(source)
        elif input_type == "txt":
            loader = TextLoader(source)
        elif input_type == "docx":
            loader = Docx2txtLoader(source)
        else:
            raise HTTPException(status_code=400, detail="Unsupported document type")

        docs = loader.load()

        return text_splitter.split_text("\n".join([doc.page_content for doc in docs]))

    except Exception as e:
        raise HTTPException(status_code=400, detail={"message":"Error Processing Documents","error": str(e)})
      

def process_input(input_type: str, input_source: str) -> List[str]:
    if input_type == "youtube":
        return process_youtube(input_source)
    elif input_type in ["txt", "pdf", "docx"]:
        return process_documents(input_type, input_source)
    else:
        raise HTTPException(status_code=400, detail="Invalid input type or missing source")

def generate_critique(request: CritiqueGeneratorRequest) -> List[CritiqueGeneratorResponse]:
    
    text_chunks = process_input(request.input_type, request.input_source)
    
    critiques = []
    json_parser = JsonOutputParser()

    for chunk in text_chunks:
        prompt = ChatPromptTemplate([
            SystemMessage(
                content="""
                You are an expert AI critique assistant. Your task is to analyze the given content and provide detailed and constructive critiques in a specific Critino Format based on the user-defined definitions. 
                Your critiques should be insightful, actionable, and aimed at improving the quality of the content.

                Each Critique output should follow the following Critino Format as a Valid JSON object
                - context: The prior discussion or information that helps in understanding the topic or question being addressed. It sets the stage for the query.
                - query: The exact question, statement, or request that led to a response. It represents the main point that needs an answer.
                - optimal_response: The best possible reply that is precise, relevant, and well-suited to the query. It serves as the standard for evaluating other responses.
                - situation: A brief, generalized description (around 10 words) summarizing the core theme of the context and query, making it useful for identifying similar cases.
                
                Only include the above mentioned Critino Format attributes in the JSON. DO NOT ADD ANY OTHER EXTRA ATTIRIBUTES.
                """
            ),
            HumanMessage(
                content=f"""
                
                ## User-Defined Definitions ##
                -context: {request.context}\n
                -query: {request.query}\n
                -optimal_response: {request.optimal_response}\n
                
                Text Chunk: {chunk}\n

                Based on the provided context, query, and optimal response, analyze the text chunk and provide a detailed critique. 
                Ensure your critique is clear, concise, and actionable.
                """
            )
        ])

        critique_chain = prompt | llm | json_parser
        response = critique_chain.invoke({})
        critiques.append(response)
    
    return critiques