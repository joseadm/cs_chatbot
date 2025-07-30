# chatbot_optimized.py - Uses pre-built vector store (run setup_once.py first)
from ingest import load_vector_store, setup_rag_pipeline
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def query_rag(qa_chain, query):
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

    return response


if __name__ == "__main__":
    # Check if vector store exists
    if not os.path.exists("./chroma_db"):
        print("Vector store not found!")
        print("Please run 'python setup_once.py' first to process your PDF")
        exit(1)

    print("Loading existing vector store...")
    vector_store = load_vector_store()
    qa_chain = setup_rag_pipeline(vector_store)
    print("Chatbot ready!")

    user_query = "How do I keep track of my returned orders?"

    print("\nResponse After Implementation of RAG")
    print("-" * 20)
    response = query_rag(qa_chain, user_query)
    print(response["result"])
    print("-" * 20)
