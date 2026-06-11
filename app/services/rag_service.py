import os
import shutil
from fastapi import HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .prompt import build_prompt 
from app.db.chroma_client import (
    get_vector_store,
    get_llm
)


vector_store = get_vector_store()
llm = get_llm()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploaded_pdfs")


def upload_pdf(file):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="只支援 PDF 檔案上傳")

    filename = file.filename
    saved_pdf_path = os.path.join(UPLOAD_DIR, filename)

    # 1. 讀取檔案儲存到本地
    with open(saved_pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. 利用 Metadata 檢查此檔案是否曾被處理過
    existing_docs = vector_store.get(
        where={"source_file": filename},
        limit=1
    )

    if len(existing_docs["ids"]) > 0:
        return {
            "message": f"{filename} 已寫入過資料庫",
            "filename": filename
        }

    # 3. 首次上傳：進行 Chunking
    print(f"正在處理新檔案：{filename}...")
    try:
        docs = PyPDFLoader(saved_pdf_path).load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(docs)

        # 4. 幫每個 chunk 加上來源標籤，區隔不同文件
        for chunk in chunks:
            chunk.metadata["source_file"] = filename
            chunk.metadata["page"] = chunk.metadata.get("page")

        # 5. 呼叫 Embedding 並寫入同一個 ChromaDB
        vector_store.add_documents(chunks)
        # 備用：非同步寫法
        # await vector_store.aadd_documents(documents)
        print(f"{filename} Embedding 寫入成功！")

        return {
            "message": f"{filename} 上傳並成功建立向量索引！",
            "filename": filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"解析 PDF 失敗: {str(e)}")




def ask_question(filename, question):
    # 2. 檢索出相關的 chunks
    relevant_docs = vector_store.similarity_search(
        question,
        k=4,
        filter={"source_file": filename}   # 用 filter「限定」只搜尋指定的這份 PDF
    )
    # 備用：非同步寫法
    # relevant_docs = await vector_store.asimilarity_search(question, k=3, filter={"source_file": filename})
                            
    if not relevant_docs:
        return {"filename": filename,
                "question": question,
                "answer": "在該文件中找不到相關參考資料。"
                }

    # 3. 將撈出來的內容組合成 Context 文本
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # 4. 設計 RAG 的 Prompt 模板
    prompt = build_prompt(context, question)

    # 5. 呼叫本地的 Ollama 生成答案
    try:
        answer = str(llm.invoke(prompt))
        return {
            "filename": filename,
            "question": question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama 呼叫失敗: {str(e)}")
