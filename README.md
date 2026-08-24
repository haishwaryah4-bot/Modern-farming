# 🌾 AgriSense AI - Modern Farming Knowledge RAG Platform

An India-focused Smart Agriculture platform featuring an **Advanced Hybrid RAG Pipeline** (Dense Vector + BM25 + Re-Ranking), full **Modern Farming Dataset indexing** (PDF, MD, DOCX, CSV, TXT), a **FastAPI Backend** (`server.py`), and a modern **React Chat Interface**.

---

## 🌟 System Architecture & RAG Pipeline Flow

```
                  ┌─────────────────────────────────┐
                  │     Modern Farming Dataset      │
                  └────────────────┬────────────────┘
                                   │
                                   ▼
                  ┌─────────────────────────────────┐
                  │          RAG Indexing           │
                  └────────────────┬────────────────┘
                                   │
                                   ▼
                  ┌─────────────────────────────────┐
                  │         Vector Database         │
                  └────────────────┬────────────────┘
                                   │
                                   │ (Indexed Knowledge Base)
                                   ▼
┌──────────────┐     ┌─────────────────────────────┐     ┌───────────────────────────────┐
│     User     │ ──► │           Chat UI           │ ──► │           /api/chat           │
└──────────────┘     └─────────────────────────────┘     └───────────────┬───────────────┘
                                                                         │
                                                                         ▼
                                                         ┌───────────────────────────────┐
                                                         │          rag_engine           │
                                                         └───────────────┬───────────────┘
                                                                         │
                                                                         ▼
                                                         ┌───────────────────────────────┐
                                                         │       Similarity Search       │
                                                         └───────────────┬───────────────┘
                                                                         │
                                                                         ▼
                                                         ┌───────────────────────────────┐
                                                         │        Relevant Chunks        │
                                                         └───────────────┬───────────────┘
                                                                         │
                                                                         ▼
                                                         ┌───────────────────────────────┐
                                                         │              LLM              │
                                                         └───────────────┬───────────────┘
                                                                         │
                                                                         ▼
                                                         ┌───────────────────────────────┐
                                                         │            Answer             │
                                                         └───────────────────────────────┘
```

### 🔄 End-to-End Execution Flow
1. **Dataset Ingestion**: The complete **Modern Farming Dataset** is parsed and split into semantic chunks during **RAG Indexing**.
2. **Vector Storage**: Chunk embeddings and metadata are stored in the in-memory **Vector Database** (with BM25 lexical indexing).
3. **User Interaction**: The **User** inputs questions via the **Chat UI**, which dispatches requests to the `/api/chat` endpoint.
4. **RAG Engine Processing**: `/api/chat` invokes **`rag_engine`** directly to perform **Similarity Search** against the Vector Database.
5. **Context Retrieval**: The top **Relevant Chunks** with citations and page metadata are retrieved and passed to the **LLM**.
6. **Strictly Grounded Response**: The **LLM** generates the final **Answer** strictly grounded in the retrieved dataset excerpts (or returns an exact refusal for ungrounded queries).

---

## 📚 100-Page Knowledge Base Scope (`Farming Dataset`)
- **Seasons**: Kharif (Monsoon), Rabi (Winter), Zaid (Summer), and Perennial cycles.
- **13 Core Crops**: Rice, Wheat, Maize, Cotton, Soybean, Groundnut, Pigeonpea (Arhar), Chickpea (Gram), Mustard, Potato, Tomato, Chilli, and Brinjal.
- **Soil Science**: 12-parameter Soil Health Card evaluation (pH, EC, OC, NPK, Zn, Fe, B, S, Mn, Cu) with targeted amelioration protocols.
- **Water & Irrigation**: Alternate Wetting & Drying (AWD), Inline Drip, Micro-Sprinklers, and $ET_0$ calculation (FAO-56 Penman-Monteith).
- **Integrated Pest Management (IPM)**: Economic Threshold Levels (ETL), cultural controls, biological parasitoids, and selective chemical interventions.
- **Modern AgriTech**: Drip & Fertigation, Soil Capacitance Probes (IoT), Automated Weather Stations (AWS), Spraying & Multispectral Drones (UAV), Satellite NDVI, Deep Learning Computer Vision, Polyhouses, Solar Pumps (PM-KUSUM), Smart Storage, and Farm ERP.

---

## 🚀 Quick Setup & Execution

### 1. Environment Setup
Copy `.env.example` to `.env` and configure your API keys (optional — offline heuristic fallbacks operate automatically):
```bash
cp .env.example .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Comprehensive Test Suite (21 Tests)
```bash
python run_tests.py
```
*(Verifies RAG, 8 Domain Tools, Ingestion of PDF/DOCX/XLSX, Scenarios, and FastAPI endpoints with 100% pass rate)*

### 4. Start the FastAPI Backend Server
```bash
python server.py
# Or with uvicorn:
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
- API Docs: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/api/health`

### 5. Launch the Web Applications
- **Streamlit 3D Information Portal**:
  ```bash
  streamlit run app.py --server.port 8501
  ```
- **React Single-Page Application**:
  Open `static/index.html` in any modern web browser or serve it via static web server.

---

## 🔌 FastAPI REST Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | System status, vector chunk counts, and indexing telemetry. |
| `POST` | `/api/chat` | AI Agriculture Agent with intent detection, clarification questions, ReAct tool execution, and session memory. |
| `POST` | `/api/rag/query` | Direct Advanced Hybrid RAG search (Dense Vector + BM25 + Cross-Encoder Re-Ranking). |
| `POST` | `/api/documents/upload` | Ingest multi-format files (**PDF, DOCX, XLSX/CSV, TXT**) into vector and BM25 stores. |
| `POST` | `/api/admin/reindex` | Triggers a full knowledge base re-index across all documents. |
| `GET` | `/api/documents` | Lists all active indexed documents and metadata. |

---

## ⚡ Multi-Step Agent Scenarios Handled
1. 🌾 *"I am growing rice in Kharif season. My field has poor drainage and high humidity. Give me an action plan."*
2. 🍅 *"Recommend an irrigation and fertigation approach for tomato at flowering stage."*
3. 🚀 *"Which modern technologies from the knowledge base are suitable for a small farm with limited water?"*
4. 🧪 *"Analyze my soil test values (N 210 kg/ha, P 18 kg/ha, pH 7.8, Zn 0.48 ppm) and recommend required amendments."*
5. 🛡️ *"Compare pest management ETL thresholds and chemical vs biological controls for Pink Bollworm in Cotton and Fall Armyworm in Maize."*
6. ☀️ *"What are the capital costs, government subsidies under PM-KUSUM, and payback periods for solar drip irrigation?"*

---

## 🔒 Safety Disclaimer
*AgriSense AI provides agricultural decision support based on published university research. Always verify official product labels, state university package of practices, and consult local Krishi Vigyan Kendra (KVK) agronomists before field application.*
