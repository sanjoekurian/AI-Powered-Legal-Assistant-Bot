import os
from typing import List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

class SummarizerAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        )
        
    def simplify_legal_text(self, texts: List[str], question: str) -> str:
        """
        Simplify legal text using Groq's LLM, incorporating both document content and LLM knowledge.
        
        Args:
            texts (List[str]): List of legal text sections to simplify
            question (str): The original user question
            
        Returns:
            str: Simplified and clarified text
        """
        combined_text = "\n\n".join(texts)
        
        system_prompt = """You are a legal expert who specializes in making complex legal information 
        accessible to non-lawyers. Your task is to:
        1. Use the provided legal text as your primary reference
        2. Supplement this information with your general knowledge of legal concepts and procedures
        3. Simplify the information while maintaining accuracy and completeness
        4. Use clear, simple language and organize information in a structured way
        5. If there are gaps in the provided text, use your knowledge to fill them in
        6. Clearly indicate when you're using information from your general knowledge vs. the provided text
        
        Always prioritize accuracy and be transparent about the sources of your information."""
        
        human_prompt = f"""Please answer the following question using both the provided legal text and your 
        general knowledge of legal matters. If there are any gaps in the provided text, use your knowledge 
        to provide a complete answer:

        Question: {question}

        Provided legal text:
        {combined_text}

        Please structure your response to:
        1. First address what's directly stated in the provided text
        2. Then supplement with relevant general knowledge
        3. Finally, provide a clear, simplified summary that combines both sources"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content 