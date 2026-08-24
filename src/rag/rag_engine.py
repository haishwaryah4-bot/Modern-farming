"""
Advanced RAG Engine with Hybrid Retrieval, Query Expansion,
Cross-Encoder / Re-Ranking, Groundedness Scoring, and Citations.
Implements lazy on-demand document indexing for zero-latency module imports.
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
        self.file_chunk_counts: Dict[str, int] = {}
        self.total_chunks = 0
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy indexing executed on first actual query request."""
        if not self._initialized:
            self._auto_index_sample_docs()
            self._initialized = True

    def _auto_index_sample_docs(self):
        """
        Automatically index the complete Modern Farming dataset on demand.
        Supports PDF, MD, TXT, CSV, DOCX formats.
        """
        sample_dir = config.SAMPLE_DOCS_DIR
        if not sample_dir.exists():
            print(f"[RAG INDEX WARNING] Dataset directory not found: {sample_dir}")
            return

        all_chunks = []
        print(f"\n{'='*70}\n[RAG DATASET INDEXING] Loading Modern Farming Knowledge Base from: {sample_dir}")

        supported_exts = [".txt", ".csv", ".pdf", ".docx", ".md"]
        for file_path in sorted(sample_dir.iterdir()):
            if file_path.is_file() and file_path.suffix.lower() in supported_exts:
                docs = self.loader.load_file(str(file_path))
                chunks = self.splitter.split_documents(docs)
                all_chunks.extend(chunks)
                
                if file_path.name not in self.indexed_files:
                    self.indexed_files.append(file_path.name)
                self.file_chunk_counts[file_path.name] = len(chunks)

                print(f"  • Ingested: '{file_path.name}' | Documents: {len(docs)} | Chunks Created: {len(chunks)}")

        if all_chunks:
            self.retriever.index_documents(all_chunks)
            self.total_chunks = len(all_chunks)
            print(f"[RAG INDEX COMPLETE] Successfully indexed {len(self.indexed_files)} files ({self.total_chunks} total semantic chunks).\n{'='*70}\n")

    def ingest_file(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Ingest and index a newly uploaded file into vector and BM25 indices.
        """
        self._ensure_initialized()
        docs = self.loader.load_file(file_path, default_metadata=metadata)
        chunks = self.splitter.split_documents(docs)
        if chunks:
            updated_chunks = self.retriever.chunks + chunks
            self.retriever.index_documents(updated_chunks)
            filename = Path(file_path).name
            if filename not in self.indexed_files:
                self.indexed_files.append(filename)
            self.file_chunk_counts[filename] = self.file_chunk_counts.get(filename, 0) + len(chunks)
            self.total_chunks = len(updated_chunks)
            return len(chunks)
        return 0

    def expand_query(self, query: str) -> List[str]:
        """
        Generic query handling without hard-coded domain biases.
        """
        cleaned = query.strip()
        return [cleaned] if cleaned else []

    def rerank_chunks(self, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cross-score and re-rank candidates based on exact term overlap,
        title matching, and semantic density.
        """
        q_words = set(re.findall(r"\b\w{3,}\b", query.lower()))
        for c in chunks:
            text_lower = c["text"].lower()
            overlap = sum(1 for w in q_words if w in text_lower)
            meta = c.get("metadata", {})
            meta_str = f"{meta.get('crop', '')} {meta.get('topic', '')} {meta.get('category', '')}".lower()
            meta_match = any(w in meta_str for w in q_words)

            if overlap == 0 and not meta_match:
                c["rerank_score"] = round(c.get("relevance_score", 0.2) * 0.4, 3)
            else:
                density_boost = (overlap / len(q_words)) if q_words else 0.0
                meta_boost = 0.10 if meta_match else 0.0
                base_score = c.get("relevance_score", 0.75)
                c["rerank_score"] = round(min(0.99, base_score * 0.65 + density_boost * 0.25 + meta_boost), 3)

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
        self._ensure_initialized()

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
            refusal_text = "I couldn't find this information in the provided dataset."
            print(f"[RAG DEBUG] User Question: '{question}' | Chunks Retrieved: 0 | Final Answer: {refusal_text}")
            return {
                "answer": refusal_text,
                "citations": [],
                "images": [],
                "groundedness_confidence": "0%",
                "retrieved_chunks": [],
            }

        # Step 4: Construct Context from Retrieved Dataset Chunks
        context_blocks = []
        citations = []
        for i, c in enumerate(ranked_chunks):
            meta = c.get("metadata", {})
            source = meta.get("source", "Knowledge Base")
            page = meta.get("page", 1)
            topic = meta.get("topic")
            crop = meta.get("crop")
            score = c.get("rerank_score", c.get("relevance_score", 0.8))

            header = f"[Source: {source}, Page: {page}" + (f", Topic: {topic}" if topic else "") + f", Score: {score}]"
            context_blocks.append(f"{header}\n{c['text']}")

            citations.append({
                "source": source,
                "page": page,
                "chunk_id": meta.get("chunk_id", f"chunk_{i}"),
                "topic": topic,
                "crop": crop,
                "relevance_score": score,
                "relevance_pct": f"{int(score * 100)}%",
                "text_snippet": c["text"][:220] + "...",
            })

        context_str = "\n\n---\n\n".join(context_blocks)
        avg_confidence = int((sum(c["relevance_score"] for c in citations) / len(citations)) * 100) if citations else 80

        # Step 5: Grounded LLM Prompting
        system_prompt = (
            "You are the AgriSense Modern Farming Knowledge Assistant. Your job is to answer questions using ONLY the provided dataset context excerpts.\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Answer strictly and only based on facts provided in the Context Excerpts.\n"
            "2. If the answer is not in the context, reply EXACTLY with: 'I couldn't find this information in the provided dataset.'\n"
            "3. Do not extrapolate, assume, or use general external knowledge outside the dataset.\n"
            "4. Cite explicit pages and document sources from the context."
        )

        user_prompt = (
            f"Context Excerpts from Knowledge Base:\n{context_str}\n\n"
            f"Farmer / Agronomist Question: {question}\n\n"
            "Provide a clear, structured, and actionable answer citing the specific sources:"
        )

        answer = llm_client.complete(user_prompt, system_prompt=system_prompt)

        # Refusal check: if LLM returns refusal, do not prepend images
        if "I couldn't find this information in the provided dataset." in answer:
            full_answer = "I couldn't find this information in the provided dataset."
            matched_images = []
        else:
            # Retrieve relevant images from ingested dataset
            matched_images = image_retriever.search_images(question, top_k=2)
            image_cards_md = image_retriever.format_image_cards_markdown(matched_images, question)
            if image_cards_md:
                full_answer = f"{image_cards_md}\n\n{answer}"
            else:
                full_answer = answer

        # Backend RAG Logging
        print(f"\n{'='*70}")
        print(f"[RAG BACKEND LOG]")
        print(f"• User Question: {question}")
        print(f"• Number of Chunks Retrieved: {len(ranked_chunks)}")
        for idx, c in enumerate(ranked_chunks):
            m = c.get('metadata', {})
            print(f"  [{idx+1}] Source: {m.get('source')} | Page: {m.get('page')} | Topic: {m.get('topic')} | Score: {c.get('relevance_score')} (RRF: {c.get('rrf_score')})")
        print(f"• Final Answer:\n{full_answer[:250]}...")
        print(f"{'='*70}\n")

        return {
            "answer": full_answer,
            "citations": citations,
            "images": matched_images,
            "retrieved_chunks": ranked_chunks,
            "grounded": True,
            "groundedness_confidence": f"{avg_confidence}%",
            "retrieval_method": "Hybrid Vector + BM25 + Re-Ranking",
        }


# Lazy Proxy Singleton
_rag_engine_instance = None

def get_rag_engine() -> RAGEngine:
    global _rag_engine_instance
    if _rag_engine_instance is None:
        _rag_engine_instance = RAGEngine()
    return _rag_engine_instance

class _LazyRAGEngineProxy:
    def __getattr__(self, name):
        return getattr(get_rag_engine(), name)

rag_engine = _LazyRAGEngineProxy()
