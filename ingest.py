# ingest.py - Free version using local embeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load PDF and extract text
def load_documents(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    return docs

# Initialize vector store with FREE local embeddings
def create_vector_store(docs):
    # Use free local embeddings instead of OpenAI
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = Chroma.from_documents(
        docs, 
        embedding=embeddings,
        persist_directory="./chroma_db"  # Save to disk
    )
    return vector_store

# Load existing vector store with local embeddings
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return vector_store

def setup_rag_pipeline(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity",  # Remove score threshold - just get most similar
        search_kwargs={"k":5}  # Get top 5 most similar documents
    )
    # Still use OpenAI for the actual chat, but only for the final response
    model = OpenAI(model="gpt-3.5-turbo-instruct")

    qa_chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain 