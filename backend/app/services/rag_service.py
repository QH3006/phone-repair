"""
RAG Service Module (Facade)
Tách nhỏ các chức năng thành các module chuyên biệt trong backend.app.services.rag:
- loader.py: Quản lý nạp và trích xuất tài liệu TXT/PDF (Ingestion)
- chunker.py: Phân đoạn văn bản và gắn Rich Metadata (Chunking)
- retriever.py: Tính toán TF-IDF & Cosine Similarity (Retrieval)
- service.py: Điều phối luồng RAG, ghép prompt và sinh câu trả lời (Orchestrator)
"""

from backend.app.services.rag.loader import RAGDocumentLoader
from backend.app.services.rag.chunker import RAGChunker
from backend.app.services.rag.retriever import RAGVectorRetriever
from backend.app.services.rag.service import RAGKnowledgeService

__all__ = [
    "RAGDocumentLoader",
    "RAGChunker",
    "RAGVectorRetriever",
    "RAGKnowledgeService"
]
