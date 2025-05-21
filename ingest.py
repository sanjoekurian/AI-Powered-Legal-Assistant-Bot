import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader

def process_pdf(file_path: str, save_path: str):
    """
    Process a PDF file, split it into chunks, and create embeddings.
    
    Args:
        file_path (str): Path to the PDF file
        save_path (str): Path to save the FAISS index
    """
    print(f"Processing {file_path}...")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Load and split the PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    
    print(f"Created {len(chunks)} chunks from {file_path}")
    
    # Create embeddings and store in FAISS
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embeddings)
    
    # Save the index
    db.save_local(save_path)
    print(f"Saved FAISS index to {save_path}")

def main():
    # Process litigation guide
    process_pdf(
        "data/guide_litigation.pdf",
        "vectorstore/guide_litigation"
    )
    
    # Process corporate laws guide
    process_pdf(
        "data/corporate_laws.pdf",
        "vectorstore/corporate_laws"
    )

if __name__ == "__main__":
    main() 