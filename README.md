# Local PDF RAG Assistant (FastAPI + Ollama + ChromaDB)

A Retrieval-Augmented Generation (RAG) system built with FastAPI, ChromaDB, Ollama, and HuggingFace Embeddings. Users can upload PDF documents, automatically generate vector embeddings, store them in a vector database, and perform question-answering based on document contents.

---

# Project Overview

This project demonstrates the implementation of an end-to-end AI backend application that combines:

- FastAPI REST API
- PDF document ingestion
- Text chunking
- Vector embeddings
- ChromaDB vector database
- Retrieval-Augmented Generation (RAG)
- Ollama local LLM inference
- Docker containerization
- GitHub Actions CI pipeline

The system allows users to upload PDF files and ask natural language questions grounded in the document content.

---

# System Architecture

```text
                ┌─────────────────┐
                │     PDF File    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  PyPDFLoader    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Text Splitter  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  BGE Embeddings │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    ChromaDB     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Retriever    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Ollama LLM    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Final Answer   │
                └─────────────────┘
```

---

# Tech Stack

## Backend

- FastAPI
- Pydantic
- Uvicorn

## LLM & RAG

- LangChain
- Ollama
- ChromaDB
- HuggingFace Embeddings
- BAAI/bge-small-en-v1.5

## Document Processing

- PyPDF
- RecursiveCharacterTextSplitter

## DevOps

- Docker
- Docker Compose
- GitHub Actions

---

# Project Structure

### 專案資料夾結構

```text
pdf-rag/
├── app/                        # 核心後端應用程式原始碼 (FastAPI)
│   ├── api/                    # API 路由層 (Routing)
│   │   └── rag.py              # 定義 PDF 上傳、詢問等 HTTP 接口 (Endpoints)
│   ├── db/                     # 資料庫連接與語言模型設定
│   │   └── chroma_client.py    # 初始化向量資料庫 ChromaDB 與 Ollama 模型設定
│   ├── models/                 # 資料結構與 Pydantic 模組
│   │   └── schemas.py          # 定義前後端資料交換的 API 欄位格式 (Request/Response)
│   ├── services/               # 核心業務邏輯層 (Business Logic)
│   │   ├── rag_service.py      # 負責 PDF 解析、文字切塊 (Chunking)、Embeddings 與檢索
│   │   └── prompt.py           # 管理餵給大語言模型 (LLM) 的 Prompt 模板
│   └── main.py                 # 應用程式進入點，初始化 FastAPI 並掛載 router 與 CORS
├── chroma_langchain_db/        # 本地端 ChromaDB 向量資料庫的數據儲存資料夾 (綁定 Docker Volume)
├── uploaded_pdfs/              # 存放使用者上傳的原始 PDF 檔案的資料夾 (綁定 Docker Volume)
├── Dockerfile                  # 用於打包 FastAPI Web 服務的 Docker 鏡像設定檔
├── docker-compose.yml          # 定義並編排 Web 服務與 Ollama 容器的部署設定檔
├── requirements.txt            # Python 專案套件依賴清單
└── README.md                   # 專案說明文件             
```


---

# Features

## PDF Upload

Upload PDF documents via REST API.

```http
POST /rag/upload
```

Example:

```bash
curl -X POST \
  "http://localhost:8001/rag/upload" \
  -F "file=@paper.pdf"
```

---

## Vector Indexing

The uploaded PDF is automatically:

1. Parsed
2. Split into chunks
3. Converted into embeddings
4. Stored in ChromaDB

---

## Document Question Answering

Ask questions against a specific indexed PDF.

```http
POST /rag/ask
```

Request:

```json
{
  "filename": "paper.pdf",
  "question": "What is Retrieval-Augmented Generation?"
}
```

Response:

```json
{
  "filename": "paper.pdf",
  "question": "What is Retrieval-Augmented Generation?",
  "answer": "Rag retrieval-augmented generation（簡稱Retrieval-Augmented Generation，RAG）是一種使用retrieve和generative language model組合的技術，以提高output的準確性。"
}
```

---

# RAG Workflow

## Step 1: Upload Document

```python
loader = PyPDFLoader(pdf_path)
docs = loader.load()
```

---

## Step 2: Text Chunking

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

---

## Step 3: Embedding Generation

```python
HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
```

---

## Step 4: Vector Storage

```python
vector_store = Chroma(
    collection_name="local_rag_collection",
    embedding_function=embeddings,
    persist_directory=DB_PATH,
)
```

---

## Step 5: Similarity Retrieval

```python
vector_store.similarity_search(
    question,
    k=4,
    filter={"source_file": filename}
)
```

---

## Step 6: LLM Generation

```python
llm = Ollama(
    model="llama3.2",
    base_url="http://ollama:11434"
    )
```

---

# API Documentation

After the application starts successfully:

```text
http://localhost:8001/docs
```

Swagger UI is automatically generated by FastAPI.

---

# Running Locally

## Clone Repository

```bash
git clone https://github.com/WalterOuO/Local_PDF_RAG_Assistant.git
cd pdf-rag
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Ollama Setup

This project uses Ollama as the local LLM runtime.

Make sure Ollama is installed and running:

```bash
ollama pull llama3.2
```

Start Ollama server:

```bash
ollama serve
```

Default endpoint:
```
http://localhost:11434
```

---

## Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

# Docker Deployment

Build:

```bash
docker compose up -d --build
```

Verify:

```bash
docker ps
```

Open Swagger:

```text
http://localhost:8001/docs
```

---

# CI Pipeline

GitHub Actions is configured to automatically:

- Install dependencies
- Validate project imports
- Build and deploy Docker container

Pipeline file:

```text
.github/workflows/ci.yml
```

---

# Challenges Solved

### Multi-Document Isolation

Each chunk is tagged with metadata:

```python
chunk.metadata["source_file"] = filename
```

This prevents retrieval from unrelated documents.

---

### Duplicate PDF Detection

Before indexing:

```python
vector_store.get(
    where={"source_file": filename}
)
```

Avoids repeated embedding generation.

---

### Hallucination Reduction

Prompt engineering enforces grounded answers:

```text
If the answer cannot be found in the provided context,
respond that the answer is unavailable in the document.
```

---

# Future Improvements

- Hybrid Search (BM25 + Vector Search)
- Reranking Models
- Streaming Responses
- Multi-PDF Question Answering
- Redis Caching
- RAG Evaluation (RAGAS)
- Authentication & User Management
- PostgreSQL Metadata Storage
- Kubernetes Deployment

---

# Skills Demonstrated

## Backend Development

- FastAPI
- REST API Design
- Dependency Management
- Service-Oriented Architecture

## AI Engineering

- RAG Pipeline
- LangChain
- LLM Integration
- Prompt Engineering
- Embeddings
- Vector Databases

## DevOps

- Docker
- CI/CD

