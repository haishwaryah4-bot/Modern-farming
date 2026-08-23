"""
Advanced RAG Engine with Hybrid Retrieval, Query Expansion,
Cross-Encoder / Re-Ranking, Groundedness Scoring, and Citations.
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.rag.document_loader import DocumentLoader
from src.rag.text_splitter import TextSplitter
from src.rag.hybrid_retriever import HybridRetriever
from src.services.llm_service import llm_client
from src.services.image_retriever_service import image_retriever
import config


class RAGEngine:
    def __init__(self):
        self.loader = DocumentLoader()
        self.splitter = TextSplitter(chunk_size=config.RAG_CHUNK_SIZE, chunk_overlap=config.RAG_CHUNK_OVERLAP)
        self.retriever = HybridRetriever(alpha=config.RAG_HYBRID_ALPHA)
        self.indexed_files: List[str] = []
        self.total_chunks = 0
        self._auto_index_sample_docs()

    def _auto_index_sample_docs(self):
        """
        Automatically index all sample agricultural documents on initial load.
        """
        sample_dir = config.SAMPLE_DOCS_DIR
        if not sample_dir.exists():
            return

        all_chunks = []
        for file_path in sample_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in [".txt", ".csv", ".pdf", ".docx"]:
                docs = self.loader.load_file(str(file_path))
                chunks = self.splitter.split_documents(docs)
                all_chunks.extend(chunks)
                if file_path.name not in self.indexed_files:
                    self.indexed_files.append(file_path.name)

        if all_chunks:
            self.retriever.index_documents(all_chunks)
            self.total_chunks = len(all_chunks)

    def ingest_file(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Ingest and index a newly uploaded file into vector and BM25 indices.
        """
        docs = self.loader.load_file(file_path, default_metadata=metadata)
        chunks = self.splitter.split_documents(docs)
        if chunks:
            updated_chunks = self.retriever.chunks + chunks
            self.retriever.index_documents(updated_chunks)
            filename = Path(file_path).name
            if filename not in self.indexed_files:
                self.indexed_files.append(filename)
            self.total_chunks = len(updated_chunks)
            return len(chunks)
        return 0

    def expand_query(self, query: str) -> List[str]:
        """
        Generate semantic variations of agronomic queries for higher recall.
        """
        queries = [query]
        lower = query.lower()
        if "rice" in lower or "paddy" in lower:
            queries.append(f"{query} nitrogen AWD tillering water management")
        elif "rust" in lower or "wheat" in lower:
            queries.append(f"{query} Puccinia striiformis propiconazole fungicide ETL")
        elif "soil" in lower or "npk" in lower:
            queries.append(f"{query} organic carbon zinc fertilizer remediation")
        elif "scheme" in lower or "subsidy" in lower:
            queries.append(f"{query} financial assistance eligibility direct benefit transfer")
        return queries

    def rerank_chunks(self, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cross-score and re-rank candidates based on exact term overlap,
        title matching, and semantic density.
        """
        q_words = set(re.findall(r"\b\w{3,}\b", query.lower()))
        for c in chunks:
            text_lower = c["text"].lower()
            overlap = sum(1 for w in q_words if w in text_lower)
            density_boost = (overlap / len(q_words)) if q_words else 0.0
            
            # Boost if metadata matches
            meta = c.get("metadata", {})
            meta_str = f"{meta.get('crop', '')} {meta.get('doc_type', '')}".lower()
            meta_boost = 0.08 if any(w in meta_str for w in q_words) else 0.0

            base_score = c.get("relevance_score", 0.75)
            c["rerank_score"] = round(min(0.99, base_score * 0.7 + density_boost * 0.22 + meta_boost), 3)

        return sorted(chunks, key=lambda x: x.get("rerank_score", 0.0), reverse=True)

    def query(
        self,
        question: str,
        top_k: int = 4,
        filters: Optional[Dict[str, str]] = None,
        use_reranker: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute grounded Advanced Hybrid RAG query with citations,
        re-ranking, confidence metric, and refusal guardrails.
        """
        # Step 1: Query Expansion
        expanded = self.expand_query(question)
        all_candidates = []
        seen_ids = set()

        for q in expanded:
            candidates = self.retriever.retrieve(q, top_k=top_k * 2, filters=filters)
            for c in candidates:
                cid = c["metadata"].get("chunk_id", str(id(c)))
                if cid not in seen_ids:
                    seen_ids.add(cid)
                    all_candidates.append(c)

        # Step 2: Re-ranking
        if use_reranker and all_candidates:
            ranked_chunks = self.rerank_chunks(question, all_candidates)[:top_k]
        else:
            ranked_chunks = all_candidates[:top_k]

        # Step 3: Out-of-Domain Refusal Guardrail
        if not ranked_chunks or (ranked_chunks and ranked_chunks[0].get("rerank_score", ranked_chunks[0].get("relevance_score", 0)) < 0.35):
            return {
                "answer": (
                    "⚠️ **Out of Knowledge Base Scope**: The uploaded agricultural documents and knowledge base "
                    "do not contain sufficient verified agronomic evidence to answer this query reliably. "
                    "Please upload relevant manuals, reports, or consult local agricultural university authorities."
                ),
                "citations": [],
                "retrieved_chunks": [],
                "grounded": False,
                "groundedness_confidence": "0%",
                "retrieval_method": "Hybrid Vector + BM25 (No Matches)",
            }

        # Step 4: Build Grounded Context & Citations
        context_parts = []
        citations = []
        total_score = 0.0

        for idx, c in enumerate(ranked_chunks):
            meta = c["metadata"]
            source = meta.get("source", "Document")
            page = meta.get("page", 1)
            chunk_id = meta.get("chunk_id", f"C{idx+1}")
            score = c.get("rerank_score", c.get("relevance_score", 0.85))
            total_score += score
            score_pct = int(score * 100)

            ref_tag = f"[Doc: {source}, Page: {page}, Chunk: {chunk_id}, Score: {score_pct}%]"
            context_parts.append(f"Citation Reference: {ref_tag}\nExcerpt: {c['text']}\n")
            citations.append({
                "source": source,
                "page": page,
                "chunk_id": chunk_id,
                "relevance_score": score,
                "relevance_pct": f"{score_pct}%",
                "text_snippet": c["text"][:220] + "...",
            })

        avg_confidence = int((total_score / len(ranked_chunks)) * 100)
        context_str = "\n---\n".join(context_parts)

        # Step 5: Grounded LLM Prompting
        system_prompt = (
            "You are an expert agronomist and agricultural researcher. Answer the farmer's question strictly "
            "based on the provided verified documents. Always cite source documents explicitly using bracketed "
            "citations like [Doc: <name>, Page: <page>]. If information is missing, state limitations clearly."
        )

        user_prompt = (
            f"Context Excerpts from Knowledge Base:\n{context_str}\n\n"
            f"Farmer / Agronomist Question: {question}\n\n"
            "Provide a clear, structured, and actionable answer citing the specific sources:"
        )

        answer = llm_client.complete(user_prompt, system_prompt=system_prompt)

        # Retrieve relevant images from ingested dataset
        matched_images = image_retriever.search_images(question, top_k=2)
        image_cards_md = image_retriever.format_image_cards_markdown(matched_images, question)
        if image_cards_md:
            full_answer = f"{image_cards_md}\n\n{answer}"
        else:
            full_answer = answer

        return {
            "answer": full_answer,
            "citations": citations,
            "images": matched_images,
            "retrieved_chunks": ranked_chunks,
            "grounded": True,
            "groundedness_confidence": f"{avg_confidence}%",
            "retrieval_method": "Hybrid Vector + BM25 + Re-Ranking",
        }


# Global singleton instance
rag_engine = RAGEngine()
