import re
from typing import List, Dict, Any


class RAGChunker:
    """
    Module Semantic Sentence & Clause Chunking:
    Phân đoạn văn bản thông minh theo ranh giới câu, đoạn văn và mệnh đề tự nhiên,
    bảo toàn nguyên vẹn ngữ cảnh ngữ nghĩa tiếng Việt, không bị cắt đứt cụt từ ghép hay câu văn dở dang.
    """

    @staticmethod
    def chunk_text(
        text: str,
        doc_name: str,
        file_type: str = "TXT",
        chunk_size: int = 300,
        chunk_overlap: int = 50
    ) -> List[Dict[str, Any]]:
        if not text:
            return []

        chunk_size = max(60, min(chunk_size, 3000))
        chunk_overlap = max(0, min(chunk_overlap, int(chunk_size * 0.7)))

        chunks = []
        text_len = len(text)
        start = 0
        chunk_idx = 1

        doc_prefix_match = re.search(r'(\d+)', doc_name)
        doc_tag = f"D{doc_prefix_match.group(1)}" if doc_prefix_match else "DOC"

        while start < text_len:
            # 1. Bỏ qua khoảng trắng hoặc dòng trống ở đầu
            while start < text_len and text[start].isspace():
                start += 1
            if start >= text_len:
                break

            ideal_end = start + chunk_size
            if ideal_end >= text_len:
                end = text_len
            else:
                window_start = start + int(chunk_size * 0.55)
                window_end = min(text_len, start + int(chunk_size * 1.15))
                search_region = text[window_start:window_end]

                chosen_cut = None

                # Ưu tiên 1: Xuống dòng đôi (hết đoạn văn bản)
                pos = search_region.rfind('\n\n')
                if pos != -1:
                    chosen_cut = window_start + pos

                # Ưu tiên 2: Xuống dòng có gạch đầu dòng hoặc số thứ tự mục tiêu chuẩn
                if chosen_cut is None:
                    match = list(re.finditer(r'\n(?=[-•\d])', search_region))
                    if match:
                        chosen_cut = window_start + match[-1].start()

                # Ưu tiên 3: Dấu chấm câu (. ! ?) kết thúc câu hoàn chỉnh
                if chosen_cut is None:
                    match = list(re.finditer(r'[\.\!\?]\s', search_region))
                    if match:
                        chosen_cut = window_start + match[-1].start() + 1

                # Ưu tiên 4: Xuống dòng đơn lẻ
                if chosen_cut is None:
                    pos = search_region.rfind('\n')
                    if pos != -1:
                        chosen_cut = window_start + pos

                # Ưu tiên 5: Dấu phân tách mệnh đề (, ; :)
                if chosen_cut is None:
                    match = list(re.finditer(r'[,;:]\s', search_region))
                    if match:
                        chosen_cut = window_start + match[-1].start() + 1

                # Ưu tiên 6: Khoảng trắng ranh giới từ gần nhất trước ideal_end
                if chosen_cut is None:
                    pos = text.rfind(' ', window_start, min(text_len, ideal_end))
                    if pos != -1 and pos > start:
                        chosen_cut = pos
                    else:
                        chosen_cut = min(text_len, ideal_end)

                end = chosen_cut

            chunk_content = text[start:end].strip()
            if chunk_content:
                words = [w for w in re.split(r'\s+', chunk_content) if w]
                chunks.append({
                    "chunk_id": f"{doc_tag}-CHK{chunk_idx:03d}",
                    "doc_name": doc_name,
                    "file_type": file_type,
                    "start_char": start,
                    "end_char": end,
                    "char_length": len(chunk_content),
                    "word_count": len(words),
                    "preview": chunk_content[:90] + ("..." if len(chunk_content) > 90 else ""),
                    "content": chunk_content
                })
                chunk_idx += 1

            if end >= text_len:
                break

            # 2. Tính toán vị trí bắt đầu cho chunk tiếp theo (Overlap theo ranh giới ngữ nghĩa)
            if chunk_overlap == 0:
                next_start = end
            else:
                target_min = max(start + 1, end - chunk_overlap)
                overlap_region = text[target_min:end]

                overlap_start = None
                # Ưu tiên bắt đầu sau dấu xuống dòng hoặc gạch đầu dòng
                match = list(re.finditer(r'\n[-•\s]*', overlap_region))
                if match:
                    overlap_start = target_min + match[0].end()

                # Ưu tiên bắt đầu sau dấu chấm kết thúc câu
                if overlap_start is None:
                    match = list(re.finditer(r'[\.\!\?]\s+', overlap_region))
                    if match:
                        overlap_start = target_min + match[0].end()

                # Ưu tiên bắt đầu sau dấu phân tách mệnh đề
                if overlap_start is None:
                    match = list(re.finditer(r'[,;:]\s+', overlap_region))
                    if match:
                        overlap_start = target_min + match[0].end()

                # Căn lề đầu từ hoàn chỉnh
                if overlap_start is None:
                    pos = target_min
                    while pos < end and not text[pos].isspace():
                        pos += 1
                    while pos < end and text[pos].isspace():
                        pos += 1
                    overlap_start = pos if pos < end else target_min

                next_start = overlap_start

            while next_start < text_len and text[next_start].isspace():
                next_start += 1
            if next_start <= start:
                next_start = end

            start = next_start

        return chunks
