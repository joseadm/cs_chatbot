from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ingest import load_vector_store, setup_rag_pipeline
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global variables for the QA chain (load once at startup)
qa_chain = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global qa_chain
    if not os.path.exists("./chroma_db"):
        raise RuntimeError("Vector store not found! Please run 'python setup_once.py' first")
    
    print("Loading vector store and initializing QA chain...")
    vector_store = load_vector_store()
    qa_chain = setup_rag_pipeline(vector_store)
    print("✅ RAG Chatbot API is ready!")
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="RAG Chatbot API",
    description="AI chatbot using RAG with your PDF knowledge base",
    lifespan=lifespan
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    question: str
    status: str


def query_rag(qa_chain, query):
    """Same function from your chatbot, but adapted for API"""
    try:
        retrieval_results = qa_chain.retriever.get_relevant_documents(query)

        if not retrieval_results:
            return "I couldn't find enough relevant details in my knowledge base."

        # Combine retrieved document texts
        retrieved_text = "\n\n".join([doc.page_content for doc in retrieval_results])

        # Structured Prompt with better handling for greetings and off-topic questions
        structured_prompt = f"""
        You are a friendly AI assistant for customer support. You have access to a knowledge base about orders, returns, refunds, and account management.

        **User Message:** {query}

        **Available Knowledge Base Information:**
        {retrieved_text}

        **Instructions:**
        1. **First, determine if the user is:**
           - Greeting you (hello, hi, hey, etc.) → Respond with a friendly greeting and offer to help
           - Asking a casual question unrelated to your knowledge base → Politely redirect them to topics you can help with
           - Asking a legitimate question about orders/returns/accounts → Use the knowledge base to answer

        2. **For greetings and casual chat:**
           - Be friendly and natural
           - Mention what topics you can help with (orders, returns, refunds, account issues)
           - Don't force step-by-step format

        3. **For knowledge base questions:**
           - Use ONLY the provided knowledge base information
           - Provide step-by-step instructions when helpful
           - Use bullet points for lists
           - Be clear and detailed

        4. **For off-topic questions:**
           - Politely explain you specialize in customer support topics
           - Redirect to what you can help with

        **Respond naturally and appropriately to the user's message.**
        """

        # Invoke OpenAI model with structured prompt
        response = qa_chain(structured_prompt)
        return response["result"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RAG Chatbot API is running", "status": "healthy"}


@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Main chat endpoint - send a question and get an AI response"""
    global qa_chain

    if qa_chain is None:
        raise HTTPException(status_code=503, detail="QA chain not initialized")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer = query_rag(qa_chain, request.question)
        return QueryResponse(answer=answer, question=request.question, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "vector_store_exists": os.path.exists("./chroma_db"),
        "qa_chain_loaded": qa_chain is not None,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
