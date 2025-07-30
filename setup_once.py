# setup_once.py - Run this ONCE to process your PDF
from ingest import load_documents, create_vector_store
import os

def setup_initial_vector_store():
    """Run this once to process your PDF and create the vector store"""
    pdf_path = "faqs/faq.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        print("Please add your PDF file to the faqs/ folder")
        return
    
    print("Loading and processing PDF...")
    docs = load_documents(pdf_path)
    print(f"Loaded {len(docs)} document chunks")
    
    print("Creating embeddings and vector store (using FREE local embeddings)...")
    vector_store = create_vector_store(docs)
    print("Vector store created and saved to ./chroma_db/")
    print("You can now run chatbot_optimized.py to use the chatbot without reprocessing!")

if __name__ == "__main__":
    setup_initial_vector_store() 