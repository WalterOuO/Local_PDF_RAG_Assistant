# Local PDF RAG Assistant
### (FastAPI + Ollama + ChromaDB + Docker)

A Retrieval-Augmented Generation (RAG) system built with FastAPI, ChromaDB, Ollama, and HuggingFace Embeddings. Users can upload PDF documents, automatically generate vector embeddings, store them in a vector database, and perform question-answering based on document contents.

---

## Project Overview

This project demonstrates the implementation of an end-to-end AI backend application that combines:

- FastAPI REST API
- PDF document ingestion
- Text chunking
- Vector embeddings
- ChromaDB vector database
- Retrieval-Augmented Generation (RAG)
- Ollama local LLM inference
- Docker containerization
- GitHub Actions CI/CD pipeline

The system allows users to upload PDF files and ask natural language questions grounded in the document content.

---

## System Architecture

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

## Tech Stack

### Backend

- FastAPI
- Pydantic
- Uvicorn

### LLM & RAG

- LangChain
- Ollama
- ChromaDB
- HuggingFace Embeddings
- BAAI/bge-small-en-v1.5

### Document Processing

- PyPDF
- RecursiveCharacterTextSplitter

### DevOps

- Docker
- Docker Compose
- GitHub Actions

---

## Project Structure

```text
pdf-rag/
│
├── app/                            # 核心應用程式資料夾
│   ├── api/                        # API 路由控制層 (Controller)
│   │   └── rag.py                  # 負責 PDF 上傳、語意問答與檢索的 API 端點定義
│   │
│   ├── db/                         # 資料庫連接與初始化 (Database Layer)
│   │   └── chroma_client.py        # 初始化 ChromaDB 向量資料庫與 Ollama LLM 模型配置
│   │
│   ├── models/                     # Pydantic 資料驗證與 Schema 定義
│   │   └── schemas.py              # 定義前後端資料交換的 API 欄位格式 (Request / Response)
│   │
│   ├── services/                   # 核心業務邏輯層 (Service Layer)
│   │   ├── rag_service.py          # 實作 PDF 解析、文字切片 (Chunking)、Embedding 整合與檢索
│   │   └── prompt.py               # 集中管理與維護餵給大語言模型 (LLM) 的提示詞模板 (Prompt Template)
│   │
│   └── main.py                     # FastAPI 應用程式進入點 (初始化服務、掛載中間件與路由)
│
├── chroma_langchain_db/            # [Bind Mount] 本機 ChromaDB 向量資料庫持久化目錄
├── uploaded_pdfs/                  # [Bind Mount] 本機 PDF 檔案上傳暫存目錄
│
├── Dockerfile                      # 用於打包 FastAPI Web 服務環境的映像檔定義
├── docker-compose.yml              # 系統容器編排設定檔 (Web 服務與 Ollama 容器之網路通道配置)
├── requirements.txt                # 專案 Python 套件依賴清單
└── README.md                       # 專案說明文件
```


---

##  API Documentation

###  Upload PDF Document

```http
POST /rag/upload
```

Request:
```text
form-data:
file: pdf file
```

Response:
```json
{
  "message": "paper.pdf 上傳並成功建立向量索引！",
  "filename": "paper.pdf"
}
```

### Ask Question (RAG)

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

## RAG Workflow

### Step 1: Upload Document

```python
loader = PyPDFLoader(pdf_path)
docs = loader.load()
```


### Step 2: Text Chunking

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```


### Step 3: Embedding Generation

```python
HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
```


### Step 4: Vector Storage

```python
vector_store = Chroma(
    collection_name="local_rag_collection",
    embedding_function=embeddings,
    persist_directory=DB_PATH,
)
```


### Step 5: Similarity Retrieval

```python
vector_store.similarity_search(
    question,
    k=4,
    filter={"source_file": filename}
)
```


### Step 6: LLM Generation

```python
llm = Ollama(
    model="llama3.2",
    base_url="http://ollama:11434"
    )
```


---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/WalterOuO/Local_PDF_RAG_Assistant.git
cd pdf-rag
```


### Install Dependencies

```bash
pip install -r requirements.txt
```


### Ollama Setup

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


### Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Docker Deployment

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

## CI Pipeline

GitHub Actions is configured to automatically:

- Install dependencies
- Validate project imports
- Build and deploy Docker container

Pipeline file:

```text
.github/workflows/ci.yml
```

---

## Challenges Solved

### Multi-Document Isolation

Each chunk is tagged with metadata:

```python
chunk.metadata["source_file"] = filename
```

This prevents retrieval from unrelated documents.


### Duplicate PDF Detection

Before indexing:

```python
vector_store.get(
    where={"source_file": filename}
)
```

Avoids repeated embedding generation.


### Hallucination Reduction

Prompt engineering enforces grounded answers:

```text
If the answer cannot be found in the provided context,
respond that the answer is unavailable in the document.
```

---

## Future Improvements

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

## Skills Demonstrated

### Backend Development

- FastAPI
- REST API Design
- Dependency Management
- Service-Oriented Architecture

### AI Engineering

- RAG Pipeline
- LangChain
- LLM Integration
- Prompt Engineering
- Embeddings
- Vector Databases

### DevOps

- Docker
- CI/CD

