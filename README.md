# E-commerce RAG Chatbot ✅

**E-commerce-RAG-Chatbot** is a retrieval-augmented generation (RAG) chatbot for product recommendation and review-based Q&A. It ingests product reviews (Flipkart dataset), indexes them in AstraDB as vector embeddings, and answers user queries using a GROQ chat model (llama-3.1-8b-instant) with context from a similarity retriever.

---

## Table of contents
1. Project overview
2. Features
3. Architecture & components
4. Getting started (install & env)
5. Quickstart — run locally
6. Configuration & environment variables
7. Data format
8. Development & contribution
9. Security & privacy notes
10. License & authorship
11. Example requests

---

## 1) Project overview 💡
This project demonstrates a lightweight end-to-end RAG system for e-commerce product Q&A:
- Converts product review CSV into language Documents
- Creates vector embeddings using HuggingFace (`BAAI/bge-small-en`)
- Stores vectors in AstraDB Vector Store (`langchain-astradb`)
- Retrieves relevant review context at query time and invokes GROQ Chat (`langchain_groq`)
- Exposes a simple Flask web chat UI and a POST endpoint for programmatic requests

---

## 2) Key features ✨
- Ingest pipeline to convert CSV reviews to vectorized documents
- Uses HuggingFace embeddings and AstraDB for scalable vector store
- Retrieval + LLM pipeline built with LangChain primitives (prompt template + ChatGroq)
- Simple Flask UI (`templates/chat.html`) and `/get` API endpoint
- Easy to configure environment via `.env` variables

---

## 3) Architecture & components 🔧
- `app.py`: Flask web server, loads env, constructs pipeline
- `ecommbot/data_converter.py`: Reads `data/flipkart_product_review.csv`, converts rows to `Document(page_content, metadata)`
- `ecommbot/ingest.py`: Builds HuggingFace embeddings and AstraDB vector store; supports ingestion mode
- `ecommbot/retreival_generation.py`: Creates a retriever (k=3) and a ChatGroq LLM chain with a prompt template
- `templates/chat.html` + `static/style.css`: Web UI for interactive chat
- `requirements.txt` / `setup.py`: Project dependencies and packaging metadata

Flow:
1. Data -> Documents (reviews)
2. Documents -> Embeddings -> AstraDB collection `chatbotecomm`
3. Query -> Similarity retrieval -> Chat template + LLM -> User response

---

## 4) Getting started — install & prerequisites 🛠️

Prerequisites
- Python 3.10+ recommended
- An AstraDB account or compatible setup (for AstraDBVectorStore)
- A GROQ API key (for ChatGroq)
- Optional GPU (torch.cuda) for HuggingFace embeddings if available

Install
```bash
# inside project root
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Install dependencies
pip install -r requirements.txt
# or editable install
pip install -e .
```

---

## 5) Quickstart — run locally ▶️

1) Create a `.env` in project root with the required variables (see next section).
2) Option A — ingest data (upload documents to AstraDB):
```bash
python -c "from ecommbot.ingest import ingestdata; ingestdata(None)"
# This will add documents and print inserted IDs
```
2) Option B — run the app (reads existing vector store):
```bash
python app.py
# open http://127.0.0.1:5000/
```
3) Use the UI or send a POST to `/get`:
```bash
curl -X POST -F "msg=What are the best budget headphones?" http://localhost:5000/get
```

---

## 6) Configuration & environment variables ⚙️
Create a `.env` with the following keys (example):
```
GROQ_API_KEY=<your_groq_api_key>
ASTRA_DB_API_ENDPOINT=<astra_api_endpoint>
ASTRA_DB_APPLICATION_TOKEN=<astra_app_token>
ASTRA_DB_KEYSPACE=<astra_keyspace>
```

Notes:
- `ingestdata("done")` returns the vector store (used in `app.py`). Passing `None` to `ingestdata` triggers ingestion and returns `(vstore, inserted_ids)`.
- Embeddings: defined in `ingest.py` using `BAAI/bge-small-en` and will use `cuda` if `torch.cuda.is_available()` is true.
- LLM: `retreival_generation.py` uses `ChatGroq` with `model='llama-3.1-8b-instant'` and `temperature=0`. Change as needed.

Tunable parameters:
- Retriever `k` (top-k docs) is set to 3 — update `retriever = vstore.as_retriever(search_kwargs={"k": 3})`
- LLM temperature and model string configurable in `retreival_generation.generation`

---

## 7) Data format & sample 📁
- Source CSV: `data/flipkart_product_review.csv`
- `data_converter.dataconveter()` extracts columns `product_title` and `review` and converts each review into a `Document` with metadata `{product_name: <title>}`

Example row:
- product_title: "BoAt Rockerz 235v2 ..."
- review: "Wowwww it's amezing bluetooth ..."

---

## 8) Development & contribution 🧩
- Coding style: simple, modular with `ecommbot` package
- To add tests: consider pytest and add tests for `dataconveter`, `ingestdata` (mock vstore), and `generation` (mock retriever)
- To extend:
  - Add fallback logic for empty retriever results
  - Add rate limiting / request validation to `/get`
  - Add unit/integration tests and CI pipeline

---

## 9) Security & privacy notes ⚠️
- Do NOT commit secrets to source control; store sensitive keys in `.env` or secret manager
- Be cautious with user-provided content that may contain PII before logging or sending to third-party APIs
- Verify AstraDB credentials and access controls when deploying

---

## 10) License & authorship 📄
- License: Apache License 2.0 
- Author: Arham Rafique 

---

## 11) Example usage & troubleshooting ✅

Start server:
```bash
python app.py
# Visit http://127.0.0.1:5000
```


Ingesting again:
```bash
python -c "from ecommbot.ingest import ingestdata; ingestdata(None)"
```
If ingestion fails, check:
- `.env` values are set
- AstraDB collection name `chatbotecomm` is available
- Network connectivity to AstraDB API endpoint

---

