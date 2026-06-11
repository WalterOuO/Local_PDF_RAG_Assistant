from dotenv import load_dotenv
from fastapi import FastAPI
from .api import rag
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="Local PDF RAG Assistant")
app.include_router(rag.router)

# 設定 CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Local PDF RAG Assistant!"}

