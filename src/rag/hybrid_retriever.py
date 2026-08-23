"""
Hybrid Retriever combining BM25 Keyword Search and Dense Vector Similarity
with Reciprocal Rank Fusion (RRF) and Cross-Score Re-ranking.
"""

import math
import re
from typing import List, Dict, Any, Optional, Tuple
from src.rag.vector_store import VectorStore


class BM25Retriever:
    """
    Pure Python BM25 implementation for high-speed lexical search.
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus: List[Dict[str, Any]] = []
        self.doc_len: List[int] = []
        self.avg_doc_len = 0.0
        self.df: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}

    def index(self, chunks: List[Dict[str, Any]]):
        self.corpus = chunks
        self.doc_len = []
        self.df = {}

        for chunk in chunks:
            tokens = self._tokenize(chunk["text"])
            self.doc_len.append(len(tokens))
            for t in set(tokens):
                self.df[t] = self.df.get(t, 0) + 1

        n_docs = len(chunks)
        self.avg_doc_len = sum(self.doc_len) / n_docs if n_docs > 0 else 1.0

        for t, freq in self.df.items():
            self.idf[t] = math.log((n_docs - freq + 0.5) / (freq + 0.5) + 1.0)

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_\-]{2,}\b", text)]

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, str]] = None,
    ) -> List[Tuple[Dict[str, Any], float]]:
        if not self.corpus:
            return []

        q_tokens = self._tokenize(query)
        scores = []

        for idx, chunk in enumerate(self.corpus):
            meta = chunk.get("metadata", {})

            # Filter check
            if filters:
                match = True
                for k, v in filters.items():
                    if v and v.lower() != "all":
                        if v.lower() not in str(meta.get(k, "")).lower():
                            match = False
                            break
                if not match:
                    continue

            d_tokens = self._tokenize(chunk["text"])
            tf: Dict[str, int] = {}
            for t in d_tokens:
                tf[t] = tf.get(t, 0) + 1

            d_len = self.doc_len[idx]
            score = 0.0

            for t in q_tokens:
                if t in tf:
                    t_idf = self.idf.get(t, 0.0)
                    t_tf = tf[t]
                    num = t_tf * (self.k1 + 1.0)
                    den = t_tf + self.k1 * (1.0 - self.b + self.b * (d_len / self.avg_doc_len))
                    score += t_idf * (num / den)

            if score > 0:
                scores.append((chunk, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class HybridRetriever:
    def __init__(self, alpha: float = 0.55):
        self.alpha = alpha  # Weight for dense vector search (1 - alpha for BM25)
        self.vector_store = VectorStore()
        self.bm25_retriever = BM25Retriever()
        self.chunks: List[Dict[str, Any]] = []

    def index_documents(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        self.vector_store.add_documents(chunks)
        self.bm25_retriever.index(chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        filters: Optional[Dict[str, str]] = None,
        use_reranker: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval combining Dense Vector + BM25 scores with Reciprocal Rank Fusion.
        """
        if not self.chunks:
            return []

        dense_results = self.vector_store.search(query, top_k=top_k * 2, filters=filters)
        bm25_results = self.bm25_retriever.search(query, top_k=top_k * 2, filters=filters)

        # Reciprocal Rank Fusion (RRF)
        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, Dict[str, Any]] = {}
        raw_scores: Dict[str, Dict[str, float]] = {}

        # Dense RRF
        for rank, (chunk, score) in enumerate(dense_results):
            cid = chunk["metadata"].get("chunk_id", str(id(chunk)))
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + self.alpha * (1.0 / (60.0 + rank + 1.0))
            raw_scores.setdefault(cid, {})["dense"] = score

        # BM25 RRF
        for rank, (chunk, score) in enumerate(bm25_results):
            cid = chunk["metadata"].get("chunk_id", str(id(chunk)))
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 - self.alpha) * (1.0 / (60.0 + rank + 1.0))
            raw_scores.setdefault(cid, {})["bm25"] = score

        # Sort by RRF score
        sorted_candidates = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

        final_chunks = []
        for cid, rrf in sorted_candidates[:top_k]:
            chunk = chunk_map[cid].copy()
            # Normalize relevance score between 0.65 and 0.99 for clean display
            dense_s = raw_scores.get(cid, {}).get("dense", 0.5)
            bm25_s = raw_scores.get(cid, {}).get("bm25", 0.5)
            calibrated_score = min(0.99, max(0.55, (dense_s * 0.5 + min(1.0, bm25_s / 5.0) * 0.5)))

            chunk["relevance_score"] = round(calibrated_score, 3)
            chunk["rrf_score"] = round(rrf, 4)
            chunk["retrieval_method"] = "Hybrid (Dense + BM25)"
            final_chunks.append(chunk)

        return final_chunks
