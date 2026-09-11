import os
import re
from typing import List, Dict, Any


class RAGDocumentLoader:
    """Module Ingestion: Quét và nạp nội dung từ các file TXT chuẩn tiếng Việt UTF-8 trong kho tài liệu."""

    @staticmethod
    def get_knowledge_base_dir() -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        kb_dir = os.path.join(base_dir, "knowledge_base")
        if not os.path.exists(kb_dir):
            os.makedirs(kb_dir, exist_ok=True)
        return kb_dir

    @classmethod
    def load_all_documents(cls) -> List[Dict[str, Any]]:
        kb_dir = cls.get_knowledge_base_dir()
        documents = []
        if not os.path.exists(kb_dir):
            return documents

        for filename in sorted(os.listdir(kb_dir)):
            if not filename.endswith(".txt"):
                continue
            file_path = os.path.join(kb_dir, filename)
            if os.path.isdir(file_path):
                continue

            size_bytes = os.path.getsize(file_path)
            content = ""
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"[Lỗi đọc file {filename}: {e}]"

            words = [w for w in re.split(r'\s+', content) if w]
            documents.append({
                "file_name": filename,
                "file_path": file_path,
                "file_type": "TXT",
                "size_bytes": size_bytes,
                "size_formatted": f"{size_bytes / 1024:.1f} KB",
                "char_count": len(content),
                "word_count": len(words),
                "content": content
            })
        return documents
