from pydantic import BaseModel


class QueryRequest(BaseModel):
    filename: str
    question: str
    

class QueryResponse(BaseModel):
    filename: str
    question: str
    answer: str


class UploadResponse(BaseModel):
    message: str
    filename: str