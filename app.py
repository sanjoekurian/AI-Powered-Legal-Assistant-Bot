import os
from typing import Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from agents.query_agent import QueryAgent
from agents.summarizer import SummarizerAgent

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Legal Assistant Bot",
    description="A multi-agent chatbot that answers legal questions using Indian legal documents",
    version="1.0.0"
)

# Initialize agents
query_agent_litigation = QueryAgent("vectorstore/guide_litigation")
query_agent_corporate = QueryAgent("vectorstore/corporate_laws")
summarizer = SummarizerAgent()

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(question: Question) -> Dict[str, str]:
    """
    Process a legal question and return a simplified answer.
    
    Args:
        question (Question): The user's question
        
    Returns:
        Dict[str, str]: The simplified answer
    """
    try:
        # Determine which document to search
        doc_type = query_agent_litigation.determine_document_type(question.question)
        
        # Get relevant sections
        query_agent = query_agent_litigation if doc_type == "litigation" else query_agent_corporate
        relevant_sections = query_agent.retrieve_sections(question.question)
        
        if not relevant_sections:
            return {"response": "I couldn't find any relevant information to answer your question."}
        
        # Simplify the legal text, now passing the original question
        simplified_answer = summarizer.simplify_legal_text(relevant_sections, question.question)
        
        return {"response": simplified_answer}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Legal Assistant Bot is running"} 