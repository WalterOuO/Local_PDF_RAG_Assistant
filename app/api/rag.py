from fastapi import APIRouter, UploadFile, File, status
from app.models import schemas
from app.services.rag_service import upload_pdf, ask_question


router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.post("/upload", response_model=schemas.UploadResponse, status_code=status.HTTP_201_CREATED)
def upload(file: UploadFile = File(...)):
    return upload_pdf(file)


@router.post("/ask", response_model=schemas.QueryResponse)
def ask(request: schemas.QueryRequest):
    return ask_question(request.filename, request.question)