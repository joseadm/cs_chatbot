# Customer Service RAG Chatbot (OpenAI + FastAPI + React)

<img width="1246" height="792" alt="Screenshot" src="https://github.com/user-attachments/assets/855d72ac-ffdc-41d1-8c18-d40a57853da2" />

## Overview
A production-ready Retrieval-Augmented Generation (RAG) chatbot for customer support. It answers questions strictly from your uploaded knowledge base (e.g., FAQs) and is optimized for clarity, reliability, and low cost.

- Backend: FastAPI (Python) serving a /chat endpoint
- Retrieval: Local vector store (Chroma) with sentence-transformers embeddings
- LLM: OpenAI (for responses only)
- Frontend: React (TypeScript) clean chat UI

Key features:
- Greeting/off-topic detection with friendly redirection
- Step-by-step, bullet-point answers for support questions
- Persistent vector store (no re-embedding each run)
- Ready-to-use REST API and web UI

## Repository Structure
- `api.py`: FastAPI app exposing the chatbot API
- `chatbot.py`: CLI entry to test the RAG flow
- `ingest.py`: PDF loading, splitting, embeddings, vector store
- `setup_once.py`: One-time script to process PDF and build vector store
- `faqs/faq.pdf`: Example knowledge base file (replace with yours)
- `chatbot-ui/`: React TypeScript chat UI
- `requirements.txt`: Backend dependencies
- `.env`: Your OpenAI API key (not committed)

## Prerequisites
- Python 3.12 (use the provided `venv`)
- Node.js 18+
- OpenAI API key with billing enabled

## Quick Start

1) Environment
- Create `.env` in project root:
  ```
  OPENAI_API_KEY=your_openai_api_key_here
  ```
- Install backend deps:
  ```bash
  ./venv/bin/python -m pip install -r requirements.txt
  ```

2) Build the vector store (run once)
- Place your PDF at `faqs/faq.pdf`
- Create embeddings and persist to `./chroma_db`:
  ```bash
  ./venv/bin/python setup_once.py
  ```

3) Start the API
```bash
./venv/bin/python api.py
```
- Health: `http://localhost:8000/health`
- Docs: `http://localhost:8000/docs`

4) Start the React UI
```bash
cd chatbot-ui
npm install
npm start
```
- UI: `http://localhost:3000`

## How It Works
1. PDF is split into semantic chunks and embedded locally
2. Chroma vector store is persisted on disk
3. For each query, top-k chunks are retrieved
4. A structured prompt is built with retrieved context
5. OpenAI generates the final answer while avoiding hallucinations

## Adding/Updating Knowledge
- Replace or add PDFs in `faqs/`
- Re-run:
  ```bash
  ./venv/bin/python setup_once.py
  ```
- For multiple sources or formats, extend `ingest.py` to load additional documents and metadata.

## Production Notes
- Restrict CORS in `api.py` to your domain
- Store conversation logs and analytics (e.g., Postgres + a dashboard)
- Consider managed vector DB (Pinecone/Qdrant/Weaviate) for scale
- Add auth (JWT/OAuth) if exposing publicly
- Implement rate limits and request validation

## Troubleshooting
- Quota errors: Ensure OpenAI billing is enabled
- No answers found: Check PDF text quality and re-run setup
- UI can’t connect: Verify API at `http://localhost:8000/health`

## License
MIT