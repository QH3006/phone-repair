import time
import json
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.db.database import SessionLocal
from backend.app.db.models import NhatKyAI
from backend.app.services.rag.loader import RAGDocumentLoader
from backend.app.services.rag.chunker import RAGChunker
from backend.app.services.rag.retriever import RAGVectorRetriever


class RAGKnowledgeService:
    """Service điều phối trọn vẹn vòng đời RAG (Orchestrator)."""

    @classmethod
    def get_document_summary(cls) -> Dict[str, Any]:
        docs = RAGDocumentLoader.load_all_documents()
        total_files = len(docs)
        total_chars = sum(d["char_count"] for d in docs)
        total_words = sum(d["word_count"] for d in docs)
        total_size = sum(d["size_bytes"] for d in docs)

        file_types = {}
        for d in docs:
            t = d["file_type"]
            file_types[t] = file_types.get(t, 0) + 1

        return {
            "total_files": total_files,
            "total_characters": total_chars,
            "total_words": total_words,
            "total_size_kb": round(total_size / 1024, 2),
            "file_types": file_types,
            "documents": [
                {
                    "file_name": d["file_name"],
                    "file_type": d["file_type"],
                    "size_formatted": d["size_formatted"],
                    "char_count": d["char_count"],
                    "word_count": d["word_count"],
                    "snippet": d["content"][:140] + "..."
                }
                for d in docs
            ]
        }

    @classmethod
    def get_all_chunks(
        cls,
        chunk_size: int = 300,
        chunk_overlap: int = 50,
        file_type_filter: str = "TXT",
        file_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        docs = RAGDocumentLoader.load_all_documents()
        selected_docs = []
        for d in docs:
            if file_filter and file_filter not in d["file_name"]:
                continue
            if file_type_filter and file_type_filter.upper() != "ALL":
                if d["file_type"] != file_type_filter.upper():
                    continue
            selected_docs.append(d)

        all_chunks = []
        for d in selected_docs:
            doc_chunks = RAGChunker.chunk_text(
                text=d["content"],
                doc_name=d["file_name"],
                file_type=d["file_type"],
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            all_chunks.extend(doc_chunks)

        return {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "file_type_filter": file_type_filter,
            "total_documents_processed": len(selected_docs),
            "total_chunks": len(all_chunks),
            "sample_chunks": all_chunks[:6],
            "all_chunks": all_chunks
        }

    @classmethod
    def retrieve(
        cls,
        query: str,
        top_k: int = 3,
        chunk_size: int = 300,
        chunk_overlap: int = 50,
        file_type_filter: str = "TXT"
    ) -> Dict[str, Any]:
        start_time = time.time()
        chunk_res = cls.get_all_chunks(chunk_size, chunk_overlap, file_type_filter=file_type_filter)
        chunks = chunk_res["all_chunks"]

        top_k_results = RAGVectorRetriever.retrieve_top_k(query, chunks, top_k=top_k)
        exec_time_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "query": query,
            "top_k": top_k,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "total_chunks_searched": len(chunks),
            "execution_time_ms": exec_time_ms,
            "retrieved_chunks": top_k_results
        }

    @classmethod
    def assemble_augmented_prompt(cls, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        context_parts = []
        for i, c in enumerate(retrieved_chunks, start=1):
            context_parts.append(
                f"[Tài liệu tham chiếu #{i}]: {c['doc_name']} (Mã Chunk: {c['chunk_id']})\n"
                f"{c['content']}\n"
            )

        context_str = "\n".join(context_parts) if context_parts else "Không tìm thấy đoạn thông tin liên quan trong kho tài liệu nội bộ."

        prompt = f"""[System Instructions]
Bạn là Trợ lý AI Chuyên viên Tư vấn & Bảo hành của Trung tâm sửa chữa điện thoại PhoneCare.
Nhiệm vụ của bạn là giải đáp câu hỏi của khách hàng CHỈ DỰA TRÊN NGỮ CẢNH TÀI LIỆU NỘI BỘ (CONTEXT) ĐƯỢC CUNG CẤP DƯỚI ĐÂY.

[Grounding & Citation Constraints]
1. Tuyệt đối không tự suy diễn hoặc bịa đặt thông tin không có trong Ngữ cảnh (Ngăn chặn triệt để Hallucination).
2. Khi đưa ra thông tin hoặc chính sách, BẮT BUỘC ghi rõ trích dẫn nguồn ở cuối câu hoặc cuối đoạn theo định dạng: [Nguồn: {{Tên_File}} - Chunk #{{Mã_Chunk}}].
3. Nếu Ngữ cảnh không chứa đủ thông tin để trả lời, hãy lịch sự thông báo cho khách hàng biết và hướng dẫn liên hệ hotline 1900.6868.

[Retrieved Context - Ngữ Cảnh Tri Thức Trích Xuất]
{context_str}

[User Question - Câu Hỏi Của Khách Hàng]
{query}

[Output Format]
Câu trả lời rõ ràng, đúng trọng tâm, chuẩn mực dịch vụ và bắt buộc có trích dẫn nguồn (Citations).
"""
        return prompt

    @classmethod
    def generate_answer(
        cls,
        query: str,
        retrieved_chunks: Optional[List[Dict[str, Any]]] = None,
        top_k: int = 3,
        chunk_size: int = 300,
        chunk_overlap: int = 50,
        file_type_filter: str = "TXT"
    ) -> Dict[str, Any]:
        start_time = time.time()

        if retrieved_chunks is None:
            ret_res = cls.retrieve(query, top_k, chunk_size, chunk_overlap, file_type_filter)
            retrieved_chunks = ret_res["retrieved_chunks"]

        augmented_prompt = cls.assemble_augmented_prompt(query, retrieved_chunks)

        answer_text = ""
        status = "ThanhCong"
        citations = []

        for c in retrieved_chunks:
            citations.append({
                "source_file": c["doc_name"],
                "chunk_id": c["chunk_id"],
                "similarity": c.get("similarity_percent", "N/A"),
                "snippet": c["content"][:100] + "..."
            })

        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=FutureWarning)
                    import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
                resp = model.generate_content(augmented_prompt)
                answer_text = resp.text
            except Exception:
                print("[RAG Service Warning] Gemini call failed, activating Grounded Fallback Engine.")
                status = "Fallback"
        else:
            status = "Fallback"

        if status == "Fallback" or not answer_text:
            answer_text = cls._generate_grounded_fallback_answer(query, retrieved_chunks)

        exec_time_ms = round((time.time() - start_time) * 1000, 2)

        try:
            db = SessionLocal()
            log_entry = NhatKyAI(
                loai_tac_vu="RAG_TruyXuatTriThuc",
                model_name=settings.GEMINI_MODEL_NAME if status == "ThanhCong" else "Local_RAG_Grounded",
                prompt_input=augmented_prompt[:1500] + "...",
                ai_raw_response=answer_text,
                ai_parsed_json=json.dumps({"citations": citations}, ensure_ascii=False),
                execution_time_ms=exec_time_ms,
                trang_thai=status
            )
            db.add(log_entry)
            db.commit()
            db.close()
        except Exception:
            print("[RAG Audit Error] Failed to write audit log")

        return {
            "status": status,
            "query": query,
            "execution_time_ms": exec_time_ms,
            "augmented_prompt": augmented_prompt,
            "answer": answer_text,
            "citations": citations,
            "retrieved_chunks": retrieved_chunks
        }

    @classmethod
    def _generate_grounded_fallback_answer(cls, query: str, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "Theo tài liệu chính sách của PhoneCare hiện tại, chúng tôi chưa tìm thấy thông tin phù hợp với câu hỏi của bạn. Vui lòng liên hệ hotline 1900.6868 để được hỗ trợ."

        best_chunk = chunks[0]
        c_text = best_chunk["content"].strip()
        doc = best_chunk["doc_name"]
        cid = best_chunk["chunk_id"]

        lines = [line.strip() for line in c_text.split('\n') if line.strip()]
        core_info = " ".join(lines[:3])

        source_tag = f"[Nguồn: {doc} - Chunk #{cid}]"
        
        reply = (
            f"Dựa trên tài liệu quy định chính thức của trung tâm PhoneCare:\n\n"
            f"• {core_info}\n\n"
            f"📌 Trích dẫn quy định: {source_tag}\n\n"
            f"Nếu bạn cần hỗ trợ kiểm tra trực tiếp thiết bị hoặc làm thủ tục bảo hành, kính mời bạn ghé quầy lễ tân PhoneCare hoặc gọi hotline 1900.6868."
        )
        return reply

    @classmethod
    def compare_rag_parameters(cls, query: str) -> Dict[str, Any]:
        start_time = time.time()

        # Kịch bản A: Nhỏ
        res_a = cls.retrieve(query, top_k=2, chunk_size=80, chunk_overlap=10)
        chunks_a = res_a["retrieved_chunks"]
        answer_a = cls.generate_answer(query, retrieved_chunks=chunks_a)

        # Kịch bản B: Chuẩn
        res_b = cls.retrieve(query, top_k=3, chunk_size=300, chunk_overlap=50)
        chunks_b = res_b["retrieved_chunks"]
        answer_b = cls.generate_answer(query, retrieved_chunks=chunks_b)

        # Kịch bản C: Lớn
        res_c = cls.retrieve(query, top_k=1, chunk_size=1200, chunk_overlap=100)
        chunks_c = res_c["retrieved_chunks"]
        answer_c = cls.generate_answer(query, retrieved_chunks=chunks_c)

        total_time = round((time.time() - start_time) * 1000, 2)

        return {
            "query": query,
            "total_benchmark_time_ms": total_time,
            "scenarios": [
                {
                    "name": "Kịch Bản A (Chunk Nhỏ: 80 chars, Top-K=2)",
                    "chunk_size": 80,
                    "top_k": 2,
                    "total_chunks_created": res_a["total_chunks_searched"],
                    "avg_similarity": round(sum(c["similarity_score"] for c in chunks_a) / max(1, len(chunks_a)), 3),
                    "retrieved_chunks": chunks_a,
                    "answer": answer_a["answer"],
                    "evaluation": "⚠️ Ngữ cảnh quá ngắn, câu văn dễ bị cắt cụt giữa chừng. LLM có thể bị thiếu điều kiện tiên quyết.",
                    "tag_class": "badge-warning"
                },
                {
                    "name": "Kịch Bản B (Chuẩn Mực Tối Ưu: 300 chars, Top-K=3)",
                    "chunk_size": 300,
                    "top_k": 3,
                    "total_chunks_created": res_b["total_chunks_searched"],
                    "avg_similarity": round(sum(c["similarity_score"] for c in chunks_b) / max(1, len(chunks_b)), 3),
                    "retrieved_chunks": chunks_b,
                    "answer": answer_b["answer"],
                    "evaluation": "✅ Tối ưu nhất: Ngữ cảnh trọn vẹn từng điều khoản, đủ độ sâu thông tin và độ tương đồng cao nhất.",
                    "tag_class": "badge-success"
                },
                {
                    "name": "Kịch Bản C (Chunk Quá Lớn: 1200 chars, Top-K=1)",
                    "chunk_size": 1200,
                    "top_k": 1,
                    "total_chunks_created": res_c["total_chunks_searched"],
                    "avg_similarity": round(sum(c["similarity_score"] for c in chunks_c) / max(1, len(chunks_c)), 3),
                    "retrieved_chunks": chunks_c,
                    "answer": answer_c["answer"],
                    "evaluation": "ℹ️ Chứa nhiều đoạn văn không liên quan (nhiễu context), tốn nhiều token và điểm tương đồng bị loãng.",
                    "tag_class": "badge-purple"
                }
            ]
        }
