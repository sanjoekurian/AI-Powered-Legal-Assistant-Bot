from typing import List
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

class QueryAgent:
    def __init__(self, db_path: str):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db = FAISS.load_local(db_path, self.embeddings, allow_dangerous_deserialization=True)
    
    def retrieve_sections(self, query: str, k: int = 3) -> List[str]:
        """
        Retrieve relevant sections from the vector store based on the query.
        
        Args:
            query (str): The user's question
            k (int): Number of relevant sections to retrieve
            
        Returns:
            List[str]: List of relevant text sections
        """
        docs = self.db.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]
    
    def determine_document_type(self, query: str) -> str:
        """
        Determine which legal document to search based on keywords in the query.
        
        Args:
            query (str): The user's question
            
        Returns:
            str: Document type ('litigation' or 'corporate')
        """
        litigation_keywords = ['lawsuit', 'court', 'filing', 'litigation', 'case', 'judge', 'trial']
        corporate_keywords = ['company', 'corporate', 'business', 'incorporation', 'board', 'shareholder']
        
        query_lower = query.lower()
        
        litigation_score = sum(1 for keyword in litigation_keywords if keyword in query_lower)
        corporate_score = sum(1 for keyword in corporate_keywords if keyword in query_lower)
        
        return 'litigation' if litigation_score >= corporate_score else 'corporate' 