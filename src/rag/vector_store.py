"""
Vector Store and Dense Semantic Index.
Provides 384-dimensional dense semantic retrieval using sentence-transformers/all-MiniLM-L6-v2
with cosine similarity scoring and metadata filtering.
"""

from typing import List, Dict, Any, Optional, Tuple
from src.rag.embeddings import embedder


class VectorStore:
    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.vectors: List[List[float]] = []
        self.embedder = embedder

    def add_documents(self, chunks: List[Dict[str, Any]]):
        """
        Index chunked documents and compute 384-dim all-MiniLM-L6-v2 dense semantic vectors.
        """
        if not chunks:
            return

        self.chunks.extend(chunks)
        texts = [c["text"] for c in chunks]
        new_vectors = self.embedder.embed_documents(texts)
        self.vectors.extend(new_vectors)

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, str]] = None,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Retrieve top-k chunks by cosine similarity in the all-MiniLM-L6-v2 384-dim embedding space.
        """
        if not self.chunks or not self.vectors:
            return []

        query_vec = self.embedder.embed_query(query)
        scores = []

        for idx, doc_vec in enumerate(self.vectors):
            chunk = self.chunks[idx]
            meta = chunk.get("metadata", {})

            # Apply metadata filters
            if filters:
                match = True
                for k, v in filters.items():
                    if v and str(v).lower() != "all":
                        doc_val = str(meta.get(k, "")).lower()
                        if str(v).lower() not in doc_val:
                            match = False
                            break
                if not match:
                    continue

            # Dot product of L2-normalized vectors = Cosine Similarity
            sim = sum(q * d for q, d in zip(query_vec, doc_vec))
            if sim > 0:
                scores.append((chunk, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
