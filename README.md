# Legal Assistant Bot

A multi-agent chatbot that answers questions about Indian legal procedures using a combination of provided legal documents and advanced language model knowledge. The system uses semantic search to find relevant information and a large language model to provide comprehensive, easy-to-understand answers.

## Features

- Answers questions about Indian litigation and corporate law
- Uses semantic search to find relevant information from legal documents
- Combines document knowledge with LLM's general legal knowledge
- Provides transparent, source-aware responses
- Simplifies complex legal language using Groq's LLaMA3-70B
- FastAPI backend with optional Streamlit frontend
- Maintains chat history in the Streamlit interface

## How It Works

The bot uses a sophisticated multi-step process to provide comprehensive answers:

1. **Question Analysis**
   - Analyzes the user's question to determine if it's about litigation or corporate law
   - Uses keyword matching to route the question to the appropriate document

2. **Document Search**
   - Uses FAISS vector store with HuggingFace embeddings to find relevant sections
   - Retrieves the most semantically similar content from the legal documents
   - Uses the "all-MiniLM-L6-v2" model for efficient semantic search

3. **Knowledge Integration**
   - Combines information from two sources:
     - Primary source: Retrieved sections from legal documents
     - Secondary source: LLM's general legal knowledge
   - Fills gaps in document information with relevant general knowledge
   - Maintains transparency about information sources

4. **Response Generation**
   - Structures the response in three parts:
     1. Information directly from the provided documents
     2. Supplementary information from general legal knowledge
     3. A clear, simplified summary combining both sources
   - Uses Groq's LLaMA3-70B model for high-quality text generation
   - Ensures responses are accurate, complete, and easy to understand

## Prerequisites

- Python 3.8 or higher
- Groq API key (for LLaMA3-70B access)
- Legal documents in PDF format:
  - `data/guide_litigation.pdf`
  - `data/corporate_laws.pdf`

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd legal-chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

5. Place your legal documents in the `data` directory:
```
data/
├── guide_litigation.pdf
└── corporate_laws.pdf
```

6. Process the PDFs to create embeddings:
```bash
python ingest.py
```

## Running the Application

1. Start the FastAPI backend:
```bash
uvicorn app:app --reload --port 8000
```

2. In a new terminal, start the Streamlit frontend (optional):
```bash
streamlit run streamlit_app.py
```

3. Access the application:
- API documentation: http://localhost:8000/docs
- Streamlit interface: http://localhost:8501

## Usage

1. Enter your legal question in the text input field
2. Click "Ask" to get a response
3. The bot will:
   - Determine if your question is about litigation or corporate law
   - Find relevant sections from the appropriate document
   - Combine document information with general legal knowledge
   - Provide a structured response with:
     - Information from the documents
     - Supplementary general knowledge
     - A clear, simplified summary
   - Display the answer with previous questions in the chat history

## API Endpoints

- `POST /ask`: Submit a legal question
  ```json
  {
    "question": "What are the steps involved in filing a lawsuit in India?"
  }
  ```

- `GET /`: Health check endpoint

## Project Structure

```
legal_chatbot/
├── app.py                     # FastAPI API entrypoint
├── agents/
│   ├── query_agent.py         # Retrieval logic and document routing
│   └── summarizer.py          # LLM-based knowledge integration and summarization
├── data/
│   ├── guide_litigation.pdf   # Source legal document 1
│   └── corporate_laws.pdf     # Source legal document 2
├── ingest.py                  # Embeds PDFs using FAISS
├── vectorstore/               # Stores FAISS index files
├── requirements.txt
└── streamlit_app.py           # Optional Streamlit frontend
```

## Technical Details

### Document Processing
- Uses PyPDFLoader for PDF parsing
- Implements RecursiveCharacterTextSplitter for optimal chunking
- Creates embeddings using HuggingFace's sentence-transformers
- Stores vectors in FAISS for efficient similarity search

### Knowledge Integration
- Primary source: Retrieved document sections
- Secondary source: LLM's general knowledge
- Transparent source attribution
- Gap-filling with relevant general knowledge

### Response Generation
- Structured three-part response format
- Clear separation of document and general knowledge
- Simplified language for better understanding
- Maintains legal accuracy while being accessible

## License

This project is licensed under the MIT License - see the LICENSE file for details. 