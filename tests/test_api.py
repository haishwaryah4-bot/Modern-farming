"""
Tests for Backend API Functions (/api/health, /api/chat, /api/rag/query, /api/documents).
"""

from server import health_check, chat_with_agent, query_rag, list_documents, ChatRequest, RAGQueryRequest


def test_api_health():
    data = health_check()
    assert data["status"] == "healthy"
    assert data["total_vector_chunks"] > 0


def test_api_chat_endpoint():
    req = ChatRequest(
        message="I am growing rice in Kharif season with poor drainage and high humidity. Give me an action plan.",
        session_id="test_session_01"
    )
    res = chat_with_agent(req)
    assert len(res.answer) > 0
    assert len(res.execution_traces) > 0
    assert res.session_id == "test_session_01"


def test_api_rag_query():
    req = RAGQueryRequest(
        query="What is the recommended irrigation schedule and split fertilizer application for rice?",
        top_k=3,
        use_reranker=True
    )
    res = query_rag(req)
    assert len(res.answer) > 0
    assert len(res.citations) > 0


def test_api_list_documents():
    data = list_documents()
    assert data["total_documents"] > 0
    assert len(data["files"]) > 0
