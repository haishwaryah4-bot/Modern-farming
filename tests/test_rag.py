"""
Tests for Advanced Hybrid RAG Engine, Loader, Splitter, and Citations.
"""

from src.rag.document_loader import DocumentLoader
from src.rag.text_splitter import TextSplitter
from src.rag.hybrid_retriever import HybridRetriever
from src.rag.rag_engine import rag_engine
import config


def test_document_loader_txt():
    sample_txt = config.SAMPLE_DOCS_DIR / "rice_cultivation_guide.txt"
    docs = DocumentLoader.load_file(str(sample_txt))
    assert len(docs) > 0
    assert "Rice" in docs[0]["text"]
    assert docs[0]["metadata"]["source"] == "rice_cultivation_guide.txt"


def test_document_loader_csv():
    sample_csv = config.SAMPLE_DOCS_DIR / "pm_kisan_and_government_schemes.csv"
    docs = DocumentLoader.load_file(str(sample_csv))
    assert len(docs) >= 5
    assert "PM-KISAN" in docs[0]["text"]


def test_text_splitter():
    splitter = TextSplitter(chunk_size=300, chunk_overlap=50)
    raw_doc = [{"text": "First paragraph.\n\nSecond paragraph with more agronomic details.", "metadata": {"source": "test.txt", "page": 1}}]
    chunks = splitter.split_documents(raw_doc)
    assert len(chunks) >= 1
    assert "chunk_id" in chunks[0]["metadata"]


def test_hybrid_retrieval_and_rrf():
    retriever = HybridRetriever(alpha=0.55)
    sample_chunks = [
        {"text": "Rice requires shallow water depth of 2-3 cm during tillering stage.", "metadata": {"source": "rice.txt", "crop": "Rice (Paddy)"}},
        {"text": "Wheat yellow rust should be treated with Propiconazole fungicide.", "metadata": {"source": "wheat.txt", "crop": "Wheat"}},
        {"text": "PM-KISAN provides Rs 6000 per year direct benefit transfer.", "metadata": {"source": "schemes.csv", "crop": "General"}},
    ]
    retriever.index_documents(sample_chunks)

    results = retriever.retrieve("rice water depth", top_k=2)
    assert len(results) > 0
    assert "Rice" in results[0]["text"]
    assert results[0]["relevance_score"] > 0


def test_minilm_embeddings():
    from src.rag.embeddings import embedder
    query_emb = embedder.embed_query("Alternate wetting and drying AWD irrigation in rice")
    assert len(query_emb) == 384
    assert any(v != 0.0 for v in query_emb)

    doc_embs = embedder.embed_documents([
        "Soil test showed low available Zinc (0.48 ppm).",
        "Cotton pink bollworm ETL threshold is 8-10 moths/trap."
    ])
    assert len(doc_embs) == 2
    assert len(doc_embs[0]) == 384
    assert len(doc_embs[1]) == 384


def test_rag_engine_query():
    res = rag_engine.query("What is the irrigation protocol for rice?", top_k=2)
    assert "answer" in res
    assert len(res["citations"]) > 0
    assert res["grounded"] is True
