import re
import math
from collections import Counter
from typing import List, Dict, Any


class RAGVectorRetriever:
    """Module Retrieval: Tính toán vector TF-IDF & Cosine Similarity."""

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        tokens = re.findall(r'\b[\w_]+\b', text.lower())
        bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
        return tokens + bigrams

    @classmethod
    def retrieve_top_k(
        cls,
        query: str,
        chunks: List[Dict[str, Any]],
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        if not query or not chunks:
            return []

        query_tokens = cls._tokenize(query)
        if not query_tokens:
            return []

        df = Counter()
        N = len(chunks)
        chunk_token_counts = []

        for chunk in chunks:
            tokens = cls._tokenize(chunk["content"])
            token_counts = Counter(tokens)
            chunk_token_counts.append(token_counts)
            for token in token_counts.keys():
                df[token] += 1

        query_counts = Counter(query_tokens)
        query_vec = {}
        for token, count in query_counts.items():
            idf = math.log((N + 1) / (df[token] + 1)) + 1.0
            query_vec[token] = count * idf

        query_norm = math.sqrt(sum(val ** 2 for val in query_vec.values())) or 1.0

        scored_chunks = []
        for idx, chunk in enumerate(chunks):
            token_counts = chunk_token_counts[idx]
            chunk_vec = {}
            dot_product = 0.0

            for token, count in token_counts.items():
                idf = math.log((N + 1) / (df[token] + 1)) + 1.0
                weight = count * idf
                chunk_vec[token] = weight
                if token in query_vec:
                    dot_product += query_vec[token] * weight

            chunk_norm = math.sqrt(sum(val ** 2 for val in chunk_vec.values())) or 1.0
            similarity = dot_product / (query_norm * chunk_norm)

            query_plain = query.lower()
            if any(term in chunk["content"].lower() for term in re.findall(r'\b\w{3,}\b', query_plain)):
                similarity += 0.05

            scored_chunks.append({
                **chunk,
                "similarity_score": round(similarity, 4),
                "similarity_percent": f"{min(100.0, max(0.0, similarity * 100)):.1f}%"
            })

        scored_chunks.sort(key=lambda x: x["similarity_score"], reverse=True)
        top_results = scored_chunks[:top_k]

        for rank, item in enumerate(top_results, start=1):
            item["rank"] = rank

        return top_results
