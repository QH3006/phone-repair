from fastapi import APIRouter, Query, Body, HTTPException
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from backend.app.services.rag_service import RAGKnowledgeService

router = APIRouter(prefix="/ai/rag", tags=["Phân Hệ RAG - Tra Cứu Tri Thức Doanh Nghiệp (Retrieval-Augmented Generation)"])


class RAGRetrieveRequest(BaseModel):
    query: str = Field(..., description="Câu hỏi của người dùng cần tra cứu tri thức")
    top_k: int = Field(3, ge=1, le=10, description="Số lượng chunks phù hợp nhất cần trích xuất")
    chunk_size: int = Field(300, ge=50, le=3000, description="Kích thước ký tự của mỗi chunk")
    chunk_overlap: int = Field(50, ge=0, le=500, description="Độ gối đầu giữa các chunks")
    file_type_filter: str = Field("TXT", description="'TXT', 'PDF', hoặc 'ALL'")


class RAGGenerateRequest(BaseModel):
    query: str = Field(..., description="Câu hỏi của người dùng")
    top_k: int = Field(3, ge=1, le=10)
    chunk_size: int = Field(300, ge=50, le=3000)
    chunk_overlap: int = Field(50, ge=0, le=500)
    file_type_filter: str = Field("TXT", description="'TXT', 'PDF', hoặc 'ALL'")
    retrieved_chunks: Optional[List[Dict[str, Any]]] = Field(None, description="Danh sách top-k chunks từ bước retrieval")


class RAGCompareRequest(BaseModel):
    query: str = Field(..., description="Câu hỏi dùng để chạy thực nghiệm so sánh đa tham số")


@router.get("/documents")
def get_documents_overview():
    """
    Yêu cầu 1 & 2: Hiển thị danh sách file tài liệu (PDF/TXT), tổng số file, dung lượng.
    """
    return RAGKnowledgeService.get_document_summary()


@router.get("/chunks")
def get_chunks_preview(
    chunk_size: int = Query(300, ge=50, le=3000),
    chunk_overlap: int = Query(50, ge=0, le=500),
    file_type_filter: str = Query("TXT", description="'TXT', 'PDF', hoặc 'ALL'")
):
    """
    Yêu cầu 2: Hiển thị tổng số chunk sinh ra, danh sách chunk mẫu và metadata chi tiết.
    """
    return RAGKnowledgeService.get_all_chunks(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        file_type_filter=file_type_filter
    )


@router.post("/retrieve")
def retrieve_top_k_chunks(req: RAGRetrieveRequest):
    """
    Yêu cầu 3: Cho nhập câu hỏi và hiển thị top-k chunks TRƯỚC KHI gọi LLM.
    Trả về điểm số tương đồng Cosine Similarity, thứ hạng, và trích đoạn.
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập nội dung câu hỏi.")
    return RAGKnowledgeService.retrieve(
        query=req.query,
        top_k=req.top_k,
        chunk_size=req.chunk_size,
        chunk_overlap=req.chunk_overlap,
        file_type_filter=req.file_type_filter
    )


@router.post("/generate")
def generate_grounded_answer(req: RAGGenerateRequest):
    """
    Yêu cầu 4: Hiển thị Augmented Prompt và câu trả lời có trích dẫn nguồn (Citations).
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập nội dung câu hỏi.")
    return RAGKnowledgeService.generate_answer(
        query=req.query,
        retrieved_chunks=req.retrieved_chunks,
        top_k=req.top_k,
        chunk_size=req.chunk_size,
        chunk_overlap=req.chunk_overlap
    )


@router.post("/compare")
def compare_parameter_sensitivity(req: RAGCompareRequest):
    """
    Yêu cầu 5: Thử thay chunk size hoặc top-k để sinh viên thấy chất lượng thay đổi.
    Chạy đối chiếu đồng thời:
    - Kịch bản A: Chunk nhỏ (80 chars, K=2)
    - Kịch bản B: Chuẩn mực tối ưu (300 chars, K=3)
    - Kịch bản C: Chunk lớn (1200 chars, K=1)
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập nội dung câu hỏi.")
    return RAGKnowledgeService.compare_rag_parameters(query=req.query)
