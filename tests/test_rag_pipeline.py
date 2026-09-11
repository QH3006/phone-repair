import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.rag_service import (
    RAGDocumentLoader, RAGChunker, RAGVectorRetriever, RAGKnowledgeService
)

client = TestClient(app)


def test_rag_document_loader():
    """Kiểm tra module Ingestion nạp đầy đủ 5 file TXT chuẩn tiếng Việt UTF-8 trong kho tài liệu."""
    docs = RAGDocumentLoader.load_all_documents()
    assert len(docs) == 5, "Kho tài liệu phải có đúng 5 files TXT"
    
    file_types = {d["file_type"] for d in docs}
    assert file_types == {"TXT"}, "Toàn bộ tài liệu phải có định dạng TXT chuẩn UTF-8"
    
    for d in docs:
        assert d["char_count"] > 100, f"Nội dung file {d['file_name']} không được rỗng"
        assert d["size_bytes"] > 0


def test_rag_chunker_and_metadata():
    """Kiểm tra module Chunking: phân đoạn văn bản và gắn đầy đủ Rich Metadata."""
    sample_text = (
        "Chính sách bảo hành PhoneCare áp dụng chế độ 1 đổi 1 trong 07 ngày. "
        "Màn hình linh kiện được bảo hành 06 tháng đối với lỗi cảm ứng. "
        "Pin điện thoại chính hãng được bảo hành 12 tháng nếu tụt pin quá 20%. "
        "Các trường hợp rơi vỡ hoặc ngấm nước sẽ bị từ chối bảo hành miễn phí."
    )
    chunks = RAGChunker.chunk_text(
        text=sample_text,
        doc_name="01_chinh_sach_bao_hanh.txt",
        file_type="TXT",
        chunk_size=120,
        chunk_overlap=30
    )
    assert len(chunks) >= 2, "Văn bản phải được chia thành nhiều hơn 1 chunk"

    for c in chunks:
        assert "chunk_id" in c
        assert "doc_name" in c
        assert "start_char" in c
        assert "end_char" in c
        assert "char_length" in c
        assert "word_count" in c
        assert "preview" in c
        assert "content" in c
        assert c["start_char"] < c["end_char"]
        assert len(c["content"]) == c["char_length"]


def test_rag_retriever_top_k_before_llm():
    """Kiểm tra Bước 1: Retrieval lọc ra đúng Top-K chunks xếp theo điểm Cosine Similarity."""
    query = "máy bị rơi nước có được bảo hành không?"
    ret = RAGKnowledgeService.retrieve(
        query=query,
        top_k=3,
        chunk_size=300,
        chunk_overlap=50,
        file_type_filter="TXT"
    )
    assert ret["query"] == query
    assert ret["top_k"] == 3
    assert len(ret["retrieved_chunks"]) <= 3
    assert len(ret["retrieved_chunks"]) > 0

    # Đảm bảo điểm tương đồng được sắp xếp giảm dần
    scores = [c["similarity_score"] for c in ret["retrieved_chunks"]]
    assert scores == sorted(scores, reverse=True), "Top-K chunks phải được sắp xếp theo điểm tương đồng giảm dần"

    # Đảm bảo có metadata thứ hạng Rank #1, #2, #3
    for i, c in enumerate(ret["retrieved_chunks"], start=1):
        assert c["rank"] == i
        assert "similarity_percent" in c


def test_rag_generate_answer_with_citations():
    """Kiểm tra Bước 2: Sinh câu trả lời có chứa trích dẫn nguồn (Grounding & Citations)."""
    query = "Pin thay mới được bảo hành bao nhiêu tháng và điều kiện đổi trả là gì?"
    res = RAGKnowledgeService.generate_answer(
        query=query,
        top_k=2,
        chunk_size=300,
        chunk_overlap=50
    )
    assert "answer" in res
    assert len(res["answer"]) > 50
    assert "citations" in res
    assert len(res["citations"]) > 0
    assert "augmented_prompt" in res
    # Kiểm tra có trích dẫn nguồn
    assert "Nguồn:" in res["answer"] or "Chunk" in res["answer"] or len(res["citations"]) >= 1


def test_rag_parameter_comparison_ab():
    """Kiểm tra Bộ thực nghiệm A/B: Thay đổi chunk size và top-k để thấy chất lượng biến thiên."""
    query = "Thời gian bảo hành màn hình và điều kiện đổi trả linh kiện hỏng"
    res = RAGKnowledgeService.compare_rag_parameters(query)
    assert "scenarios" in res
    assert len(res["scenarios"]) == 3, "Phải có đủ 3 kịch bản: Nhỏ (80), Chuẩn (300), Lớn (1200)"
    
    scenario_names = [s["name"] for s in res["scenarios"]]
    assert any("Nhỏ" in n for n in scenario_names)
    assert any("Chuẩn" in n for n in scenario_names)
    assert any("Lớn" in n for n in scenario_names)

    # Kịch bản A (80 chars) phải sinh ra nhiều chunks hơn kịch bản C (1200 chars)
    s_a = res["scenarios"][0]
    s_c = res["scenarios"][2]
    assert s_a["total_chunks_created"] > s_c["total_chunks_created"]


def test_rag_api_endpoints():
    """Kiểm tra toàn bộ các HTTP endpoints của phân hệ RAG qua FastAPI TestClient."""
    # 1. GET /api/ai/rag/documents
    r_docs = client.get("/api/ai/rag/documents")
    assert r_docs.status_code == 200
    d_data = r_docs.json()
    assert d_data["total_files"] >= 5

    # 2. GET /api/ai/rag/chunks
    r_chunks = client.get("/api/ai/rag/chunks?chunk_size=250&chunk_overlap=40&file_type_filter=TXT")
    assert r_chunks.status_code == 200
    c_data = r_chunks.json()
    assert c_data["total_chunks"] > 0
    assert len(c_data["sample_chunks"]) > 0

    # 3. POST /api/ai/rag/retrieve (Top-K Chunks TRƯỚC KHI gọi LLM)
    r_ret = client.post("/api/ai/rag/retrieve", json={
        "query": "Quy định hoàn tiền 100% khi nào?",
        "top_k": 2,
        "chunk_size": 300,
        "chunk_overlap": 50,
        "file_type_filter": "TXT"
    })
    assert r_ret.status_code == 200
    ret_data = r_ret.json()
    assert len(ret_data["retrieved_chunks"]) == 2

    # 4. POST /api/ai/rag/generate (Sinh câu trả lời có nguồn)
    r_gen = client.post("/api/ai/rag/generate", json={
        "query": "Quy định hoàn tiền 100% khi nào?",
        "top_k": 2,
        "chunk_size": 300,
        "chunk_overlap": 50,
        "retrieved_chunks": ret_data["retrieved_chunks"]
    })
    assert r_gen.status_code == 200
    gen_data = r_gen.json()
    assert "answer" in gen_data
    assert len(gen_data["citations"]) == 2

    # 5. POST /api/ai/rag/compare (Thực nghiệm so sánh tham số)
    r_cmp = client.post("/api/ai/rag/compare", json={
        "query": "Máy bị dán keo màn hình thì bảo quản thế nào?"
    })
    assert r_cmp.status_code == 200
    cmp_data = r_cmp.json()
    assert len(cmp_data["scenarios"]) == 3
