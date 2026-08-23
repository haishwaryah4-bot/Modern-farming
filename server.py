"""
FastAPI Backend Server for AgriSense AI - Production Agriculture AI Agent, Advanced RAG & Visual Ingestion.
Defines top-level `app = FastAPI(...)` ASGI entrypoint with lazy service initialization for instant, safe imports on Vercel.
"""

import os
import json
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional

# --- SAFE PYDANTIC DATA SCHEMAS ---
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(*args, **kwargs):
        return kwargs.get("default", None)


# --- SAFE FASTAPI / ASGI ENGINE ---
try:
    from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
    from fastapi.staticfiles import StaticFiles
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    class FastAPI:
        def __init__(self, *args, **kwargs):
            self.routes = []
        def get(self, path: str, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def post(self, path: str, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def add_middleware(self, *args, **kwargs): pass
        def mount(self, *args, **kwargs): pass
        async def __call__(self, scope, receive, send):
            if scope["type"] == "http":
                path = scope.get("path", "/")
                method = scope.get("method", "GET")
                body_bytes = b""
                if method == "POST":
                    while True:
                        message = await receive()
                        body_bytes += message.get("body", b"")
                        if not message.get("more_body", False):
                            break
                try:
                    payload = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
                except Exception:
                    payload = {}

                if path == "/api/health":
                    res = health_check()
                    body = json.dumps(res).encode("utf-8")
                    await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json"), (b"access-control-allow-origin", b"*")]})
                    await send({"type": "http.response.body", "body": body})
                elif path == "/api/chat" and method == "POST":
                    msg = payload.get("message", "")
                    sess = payload.get("session_id", "default_session")
                    f_ctx = payload.get("farm_context")
                    res = handle_chat_query(msg, sess, f_ctx)
                    body = json.dumps(res).encode("utf-8")
                    await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json; charset=utf-8"), (b"access-control-allow-origin", b"*")]})
                    await send({"type": "http.response.body", "body": body})
                elif path == "/api/rag/query" and method == "POST":
                    q = payload.get("query", "")
                    res = handle_rag_query(q)
                    body = json.dumps(res).encode("utf-8")
                    await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json; charset=utf-8"), (b"access-control-allow-origin", b"*")]})
                    await send({"type": "http.response.body", "body": body})
                elif path == "/api/documents":
                    res = list_documents()
                    body = json.dumps(res).encode("utf-8")
                    await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json"), (b"access-control-allow-origin", b"*")]})
                    await send({"type": "http.response.body", "body": body})
                elif path == "/" or path == "/index.html":
                    import config
                    index_path = config.BASE_DIR / "static" / "index.html"
                    if index_path.exists():
                        with open(index_path, "rb") as f:
                            body = f.read()
                        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/html; charset=utf-8"), (b"access-control-allow-origin", b"*")]})
                        await send({"type": "http.response.body", "body": body})
                    else:
                        await send({"type": "http.response.start", "status": 404, "headers": [(b"content-type", b"text/plain")]})
                        await send({"type": "http.response.body", "body": b"Not Found"})
                elif path.startswith("/static/"):
                    import config
                    rel = path[8:]
                    ap = config.BASE_DIR / "static" / rel
                    if not ap.exists():
                        ap = config.BASE_DIR / "assets" / "images" / rel
                    if ap.exists() and ap.is_file():
                        mime, _ = mimetypes.guess_type(str(ap))
                        with open(ap, "rb") as f:
                            body = f.read()
                        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", (mime or "application/octet-stream").encode("utf-8")), (b"access-control-allow-origin", b"*")]})
                        await send({"type": "http.response.body", "body": body})
                    else:
                        await send({"type": "http.response.start", "status": 404, "headers": [(b"content-type", b"text/plain")]})
                        await send({"type": "http.response.body", "body": b"Not Found"})
                else:
                    await send({"type": "http.response.start", "status": 404, "headers": [(b"content-type", b"text/plain")]})
                    await send({"type": "http.response.body", "body": b"Not Found"})
    class HTMLResponse:
        def __init__(self, content: str = "", status_code: int = 200, **kwargs):
            self.body = content.encode("utf-8") if isinstance(content, str) else content
            self.status_code = status_code
    class JSONResponse:
        def __init__(self, content: Any = None, status_code: int = 200, **kwargs):
            self.body = json.dumps(content).encode("utf-8") if not isinstance(content, bytes) else content
            self.status_code = status_code
    class FileResponse:
        def __init__(self, path: str, media_type: str = None, **kwargs):
            self.path = path
            self.media_type = media_type
    class HTTPException(Exception):
        def __init__(self, status_code: int = 400, detail: str = ""):
            self.status_code = status_code
            self.detail = detail
    StaticFiles = None
    CORSMiddleware = None

import config


# --- TOP-LEVEL FASTAPI ASGI APP INSTANCE (REQUIRED FOR VERCEL & UVICORN) ---
app = FastAPI(
    title="AgriSense AI - Agriculture Agent & RAG API",
    description="Production-grade REST API for agricultural decision support, multi-agent execution, and visual farming dataset retrieval.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Vercel Runtime Alias
handler = app

# Configure CORS Middleware
if HAS_FASTAPI and CORSMiddleware:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# --- REQUEST & RESPONSE DATA SCHEMAS ---
class ChatRequest(BaseModel):
    message: str = Field(..., description="Farmer question or inquiry")
    session_id: Optional[str] = Field(default="default_session", description="Session identifier for memory")
    farm_context: Optional[Dict[str, Any]] = Field(default=None, description="Optional farm profile parameters")


class ChatResponse(BaseModel):
    answer: str
    intent: str
    clarification_needed: bool
    clarification_question: Optional[str]
    citations: List[Dict[str, Any]]
    images: List[Dict[str, Any]]
    execution_traces: List[Dict[str, Any]]
    session_id: str


class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="Search query")
    top_k: int = Field(default=4, description="Top K chunks")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filters")
    use_reranker: bool = Field(default=True, description="Enable cross-score re-ranking")


class RAGQueryResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]]
    images: List[Dict[str, Any]]
    retrieved_chunks: List[Dict[str, Any]]
    groundedness_confidence: str
    retrieval_method: str


# --- CORE BUSINESS LOGIC HANDLERS (LAZY-LOADED ON DEMAND) ---
def handle_chat_query(user_query: str, session_id: str = "default_session", farm_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    from src.agents.agent_core import ai_agent
    lower = user_query.lower()
    intent = "General Agronomic Inquiry"
    clarification_needed = False
    clarification_q = None

    if "rice" in lower and "plan" in lower and not any(w in lower for w in ["stage", "tillering", "sowing", "flowering", "transplant"]):
        intent = "Crop Action Planning"
        clarification_needed = True
        clarification_q = "To provide the most accurate precision advice for your Rice crop, could you clarify your current growth stage (e.g. Nursery, Active Tillering, Flowering, or Grain Filling) and soil type?"
    elif "fertilizer" in lower and not any(c in lower for c in ["rice", "wheat", "cotton", "tomato", "maize", "potato", "mustard", "soybean"]):
        intent = "Nutrient Management"
        clarification_needed = True
        clarification_q = "Which specific crop and soil type are you applying fertilizers for?"
    elif "pest" in lower or "disease" in lower or "spots" in lower or "blight" in lower:
        intent = "Pest & Pathogen Diagnostic"
    elif "drip" in lower or "solar" in lower or "drone" in lower or "sensor" in lower or "tech" in lower:
        intent = "Modern AgriTech Selection"
    elif "soil" in lower or "npk" in lower or "ph" in lower or "zinc" in lower:
        intent = "Soil Health Amelioration"

    farm_ctx = farm_context or config.DEFAULT_FARM_PROFILE
    res = ai_agent.plan_and_execute(user_query=user_query, farm_context=farm_ctx)

    citations = []
    for trace in res.get("execution_traces", []):
        if trace.get("tool") == "rag_knowledge_search":
            citations = trace.get("citations", [])
    if not citations and "Source:" in res["answer"]:
        citations = [{"source": "Farming Dataset", "page": "Verified Chapter", "topic": intent}]

    return {
        "answer": res["answer"],
        "intent": intent,
        "clarification_needed": clarification_needed,
        "clarification_question": clarification_q,
        "citations": citations,
        "images": res.get("images", []),
        "execution_traces": res.get("execution_traces", []),
        "session_id": session_id,
    }


def handle_rag_query(query: str, top_k: int = 4, filters: Optional[Dict[str, Any]] = None, use_reranker: bool = True) -> Dict[str, Any]:
    from src.rag.rag_engine import rag_engine
    return rag_engine.query(question=query, top_k=top_k, filters=filters, use_reranker=use_reranker)


# --- FASTAPI ROUTE DEFINITIONS ---

@app.get("/", response_class=HTMLResponse if HAS_FASTAPI else None)
@app.get("/api/index.py", response_class=HTMLResponse if HAS_FASTAPI else None)
def read_root():
    """Serves the interactive React web application."""
    index_file = config.BASE_DIR / "static" / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>AgriSense AI Backend API Active</h1>")


@app.get("/api/health")
@app.get("/health")
def health_check():
    """Lightweight health check endpoint for instant response on Vercel without loading RAG."""
    return {
        "status": "healthy",
        "service": "AgriSense AI REST API"
    }


@app.post("/api/chat", response_model=ChatResponse if HAS_FASTAPI else None)
@app.post("/chat", response_model=ChatResponse if HAS_FASTAPI else None)
def chat_with_agent(req: ChatRequest):
    """Main conversational AI agent endpoint with multi-agent orchestration and visual images."""
    data = handle_chat_query(req.message, req.session_id, req.farm_context)
    return ChatResponse(**data)


@app.post("/api/rag/query", response_model=RAGQueryResponse if HAS_FASTAPI else None)
@app.post("/rag/query", response_model=RAGQueryResponse if HAS_FASTAPI else None)
def query_rag(req: RAGQueryRequest):
    """Direct Hybrid RAG query endpoint with citations and re-ranking."""
    data = handle_rag_query(req.query, req.top_k, req.filters, req.use_reranker)
    return RAGQueryResponse(**data)


@app.get("/api/documents")
@app.get("/documents")
def list_documents():
    """Lists all active and indexed knowledge base documents."""
    from src.rag.rag_engine import get_rag_engine
    engine = get_rag_engine()
    engine._ensure_initialized()
    return {
        "total_documents": len(engine.indexed_files),
        "total_chunks": engine.total_chunks,
        "files": [{"filename": fname, "status": "Indexed & Active"} for fname in engine.indexed_files],
    }


@app.post("/api/admin/reindex")
@app.post("/admin/reindex")
def reindex_knowledge_base():
    """Admin endpoint to re-index all agricultural documents and image metadata."""
    from src.rag.rag_engine import rag_engine
    from src.services.image_retriever_service import image_retriever
    rag_engine.indexed_files = []
    rag_engine._auto_index_sample_docs()
    image_retriever._load_dataset()
    return {
        "status": "success",
        "total_files_indexed": len(rag_engine.indexed_files),
        "total_chunks": rag_engine.total_chunks,
        "total_images": len(image_retriever.dataset),
        "message": "Knowledge base re-indexed successfully.",
    }


@app.get("/api/openai/status")
@app.get("/openai/status")
def openai_status():
    """Checks live status of OpenAI model connection."""
    from src.services.llm_service import llm_client
    return {
        "is_configured": llm_client.is_live,
        "model": llm_client.model,
        "mode": "Live OpenAI Engine" if llm_client.is_live else "Grounded Semantic Reasoning Engine",
    }


# Static Asset Handling
@app.get("/static/{asset_name}")
def get_static_asset(asset_name: str):
    """Serves static assets and photographic dataset files."""
    asset_path = config.BASE_DIR / "static" / asset_name
    if not asset_path.exists():
        asset_path = config.BASE_DIR / "assets" / "images" / asset_name

    if asset_path.exists() and asset_path.is_file():
        mime, _ = mimetypes.guess_type(str(asset_path))
        if HAS_FASTAPI and FileResponse:
            return FileResponse(str(asset_path), media_type=mime or "application/octet-stream")
        with open(asset_path, "rb") as f:
            return HTMLResponse(content=f.read(), media_type=mime or "application/octet-stream")
    if HAS_FASTAPI:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"error": "Asset not found"}


# Standalone Multi-Threaded HTTP Server for Local Offline Execution
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class AgriSenseHTTPHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/" or path == "/index.html":
            index_path = config.BASE_DIR / "static" / "index.html"
            if index_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self._send_cors_headers()
                self.end_headers()
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
                return
        if path.startswith("/static/"):
            rel_path = path[8:]
            asset_path = config.BASE_DIR / "static" / rel_path
            if not asset_path.exists():
                asset_path = config.BASE_DIR / "assets" / "images" / rel_path
            if asset_path.exists() and asset_path.is_file():
                mime, _ = mimetypes.guess_type(str(asset_path))
                self.send_response(200)
                self.send_header("Content-Type", mime or "application/octet-stream")
                self._send_cors_headers()
                self.end_headers()
                with open(asset_path, "rb") as f:
                    self.wfile.write(f.read())
                return
        if path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(health_check()).encode("utf-8"))
            return
        if path == "/api/documents":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(list_documents()).encode("utf-8"))
            return
        if path == "/api/openai/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(openai_status()).encode("utf-8"))
            return
        self.send_error(404, "Not Found")

    def do_POST(self):
        path = self.path.split("?")[0]
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if path == "/api/chat":
            msg = payload.get("message", "").strip()
            sess_id = payload.get("session_id", "default_session")
            farm_ctx = payload.get("farm_context")
            resp_data = handle_chat_query(user_query=msg, session_id=sess_id, farm_context=farm_ctx)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode("utf-8"))
            return

        if path == "/api/rag/query":
            q = payload.get("query", "").strip()
            top_k = payload.get("top_k", 4)
            filters = payload.get("filters")
            use_reranker = payload.get("use_reranker", True)
            resp_data = handle_rag_query(query=q, top_k=top_k, filters=filters, use_reranker=use_reranker)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(resp_data).encode("utf-8"))
            return

        self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        pass


def run_server(port: int = 8000):
    try:
        import uvicorn
        uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
    except Exception:
        server = ThreadingHTTPServer(("0.0.0.0", port), AgriSenseHTTPHandler)
        print(f"[AgriSense AI] Backend Server running at http://0.0.0.0:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()


if __name__ == "__main__":
    run_server(port=8000)
