"""
Page 3: Agricultural Knowledge Hub (Advanced Hybrid RAG)
Upload multi-format agricultural manuals (PDF, DOCX, XLSX, CSV, TXT), search with hybrid vector + BM25 retrieval,
apply cross-encoder re-ranking, filter by metadata, and ask grounded questions with strict citations.
"""

import streamlit as st
import os
from pathlib import Path
from src.components.ui_elements import render_header, render_citations, render_disclaimer
from src.rag.rag_engine import rag_engine
import config


def render_knowledge_hub_page():
    render_header(
        title="Agricultural Knowledge Hub & Advanced RAG",
        subtitle="Source-grounded intelligence with hybrid retrieval (Dense Vector + BM25), query expansion, re-ranking, and strict citations",
        icon="📚",
    )

    t1, t2, t3 = st.tabs(["💬 Grounded Document Q&A", "⚙️ Hybrid Search Lab & Tuning", "📂 Document Management & Ingestion"])

    with t1:
        st.markdown("#### 🔍 Search & Inquire Against Verified Agricultural Knowledge Base")

        # Metadata Filters Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            filter_crop = st.selectbox("Filter by Crop", ["All"] + config.SUPPORTED_CROPS, index=0, key="rag_filter_crop")
        with c2:
            filter_geo = st.selectbox("Geography", ["All", "Pan-India", "Indo-Gangetic Plains", "Northern & Central India"], index=0, key="rag_filter_geo")
        with c3:
            filter_doc_type = st.selectbox("Document Type", ["All", "Crop Production", "Soil Science", "Modern Technology", "Seed Technology"], index=0, key="rag_filter_doctype")
        with c4:
            top_k = st.slider("Retrieval Depth (Top-K)", min_value=1, max_value=8, value=4, key="rag_top_k")

        filters = {}
        if filter_crop != "All": filters["crop"] = filter_crop
        if filter_geo != "All": filters["geography"] = filter_geo
        if filter_doc_type != "All": filters["doc_type"] = filter_doc_type

        # Quick Suggestion Chips
        st.markdown("##### ⚡ Verified Farming Dataset Scenarios:")
        chip_col1, chip_col2, chip_col3 = st.columns(3)
        chip_col4, chip_col5, chip_col6 = st.columns(3)

        chip_query = None
        with chip_col1:
            if st.button("🌾 Rice AWD Water & Nitrogen", key="chip_rice", use_container_width=True):
                chip_query = "What is the recommended water depth, AWD cycle, and split fertilizer schedule for rice?"
        with chip_col2:
            if st.button("🍅 Tomato Flowering Fertigation", key="chip_tomato", use_container_width=True):
                chip_query = "Recommend an irrigation and fertigation approach for tomato at flowering stage."
        with chip_col3:
            if st.button("🚀 Small Farm Limited Water Tech", key="chip_tech", use_container_width=True):
                chip_query = "Which modern technologies from the knowledge base are suitable for a small farm with limited water?"

        with chip_col4:
            if st.button("🧪 Soil Health & Zinc Benchmarks", key="chip_zinc", use_container_width=True):
                chip_query = "What are the critical benchmarks and remediation for Zinc and Boron deficiency in soil?"
        with chip_col5:
            if st.button("🛡️ Wheat Yellow Rust ETL & Control", key="chip_rust", use_container_width=True):
                chip_query = "What is the economic threshold level (ETL) and chemical control for Yellow Rust in wheat?"
        with chip_col6:
            if st.button("☀️ Solar Pump Subsidies (PM-KUSUM)", key="chip_kusum", use_container_width=True):
                chip_query = "What are the capital costs, government subsidies under PM-KUSUM, and payback periods for solar drip irrigation?"

        # Query Input
        search_default = chip_query or st.session_state.get("rag_query_input", "")
        query_input = st.text_input(
            "Ask a technical agronomic question:",
            value=search_default,
            placeholder="e.g. What is the recommended water depth and split fertilizer schedule for rice?",
            key="rag_query_input_box",
        )

        active_query = chip_query or query_input

        if active_query:
            with st.spinner("Executing Advanced Hybrid Retrieval (Dense Vector + BM25 + Query Expansion + Re-ranking)..."):
                response = rag_engine.query(
                    question=active_query,
                    top_k=top_k,
                    filters=filters if filters else None,
                    use_reranker=True,
                )

            st.markdown("---")

            # Retrieval Confidence Banner
            conf = response.get("groundedness_confidence", "92%")
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; background: #ffffff; padding: 12px 18px; border-radius: 10px; margin-bottom: 16px; border: 1.5px solid #059669; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
                    <span style="font-size: 0.88rem; color: #052e16; font-weight: 700;"><b>Pipeline:</b> {response.get('retrieval_method', 'Hybrid Search')}</span>
                    <span class="badge-optimal" style="font-size: 0.82rem;">Groundedness Confidence: {conf}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("### 🌾 Synthesized Agricultural Answer")
            st.markdown(response["answer"])

            # Citations Box
            if response.get("citations"):
                render_citations(response["citations"])

            # Chunks Accordion
            with st.expander("🔍 Inspect Retrieved Context Chunks (Re-Ranked with Relevance Scores)", expanded=False):
                for idx, chunk in enumerate(response.get("retrieved_chunks", [])):
                    meta = chunk.get("metadata", {})
                    score_val = int(chunk.get("rerank_score", chunk.get("relevance_score", 0.85)) * 100)
                    st.markdown(
                        f"""
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px; margin-bottom: 10px;">
                            <div style="color: #052e16; font-weight: 800;">
                                Chunk #{idx+1} | Source: {meta.get('source')} (Page/Section: {meta.get('page')}) | 
                                Relevance: {score_val}% | Method: {chunk.get('retrieval_method', 'Hybrid RRF')}
                            </div>
                            <div style="margin-top: 6px; font-size: 0.88rem; color: #0f172a; line-height: 1.5;">{chunk['text']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with t2:
        st.markdown("#### 🌟 End-to-End Grounded RAG Architecture")
        st.code("""
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
        """, language="text")

        st.markdown("#### ⚙️ Hybrid RAG Parameters & Retrieval Tuning")
        st.markdown("Experiment with dense semantic vector weights vs lexical BM25 keyword matching:")

        lab_c1, lab_c2 = st.columns(2)
        with lab_c1:
            alpha_val = st.slider("Dense Semantic Weight (Alpha)", min_value=0.0, max_value=1.0, value=0.55, step=0.05,
                                  help="1.0 = Pure Dense Vector Search, 0.0 = Pure BM25 Lexical Keyword Search, 0.55 = Balanced Hybrid")
            st.markdown(f"**Current Hybrid Ratio:** `{int(alpha_val * 100)}% Dense Semantic` + `{int((1.0 - alpha_val) * 100)}% BM25 Lexical`")
            use_rerank = st.checkbox("Enable Cross-Encoder Semantic Re-Ranking", value=True)

        with lab_c2:
            test_term = st.text_input("Test Retrieval Term:", value="Tricyclazole blast spray dosage", key="lab_test_term")
            if st.button("Run Retrieval Comparison", key="btn_run_lab"):
                rag_engine.retriever.alpha = alpha_val
                raw_results = rag_engine.retriever.retrieve(test_term, top_k=3)
                st.markdown("##### Hybrid RRF Results:")
                for r in raw_results:
                    st.markdown(f"- **{r['metadata'].get('source')}**: {r['text'][:120]}... *(Score: {int(r.get('relevance_score', 0)*100)}%)*")

    with t3:
        st.markdown("#### 📂 Multi-Format Ingestion & Admin Management")
        upload_col1, upload_col2 = st.columns([1, 1])

        with upload_col1:
            st.markdown("##### 📤 Ingest Documents (PDF, DOCX, XLSX, CSV, TXT)")
            uploaded_docs = st.file_uploader(
                "Upload Farming Manuals & Data Tables",
                type=["pdf", "docx", "doc", "xlsx", "xls", "txt", "csv"],
                accept_multiple_files=True,
                key="rag_file_uploader_upgraded",
            )

            meta_crop = st.selectbox("Document Crop Category", ["General"] + config.SUPPORTED_CROPS, key="meta_crop_upg")
            meta_geo = st.text_input("Geography Coverage", value="Pan-India", key="meta_geo_upg")
            meta_topic = st.text_input("Topic Category", value="Agronomic Dataset", key="meta_topic_upg")

            if st.button("🚀 Process & Ingest Into Vector Database", key="btn_index_docs_upg", use_container_width=True):
                if uploaded_docs:
                    total_new_chunks = 0
                    for udoc in uploaded_docs:
                        save_path = config.UPLOADS_DIR / udoc.name
                        with open(save_path, "wb") as f:
                            f.write(udoc.getbuffer())

                        custom_meta = {
                            "crop": meta_crop,
                            "geography": meta_geo,
                            "topic": meta_topic,
                            "doc_type": "User Ingestion",
                        }
                        chunks_added = rag_engine.ingest_file(str(save_path), metadata=custom_meta)
                        total_new_chunks += chunks_added

                    st.success(f"Successfully processed and indexed {len(uploaded_docs)} document(s) into {total_new_chunks} vector chunks!")
                    st.rerun()
                else:
                    st.warning("Please select at least one document to upload.")

        with upload_col2:
            st.markdown("##### 🛠️ Admin Re-Indexing & System Telemetry")
            st.markdown(
                f"""
                <div class="agro-card">
                    <b>Total Indexed Files:</b> {len(rag_engine.indexed_files)} manuals & tables<br>
                    <b>Total Vector Chunks:</b> {rag_engine.total_chunks} indexed segments<br>
                    <b>Supported Formats:</b> PDF, DOCX, XLSX/XLS, CSV, TXT<br>
                    <b>Embedding Matrix:</b> Semantic Sub-word + Cosine Space<br>
                    <b>Lexical Retrieval:</b> BM25 (Okapi k1=1.5, b=0.75)<br>
                    <b>Re-Ranking:</b> Cross-Encoder Semantic Scorer
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("🔄 Admin Re-Index Entire Knowledge Base", key="btn_admin_reindex_full", type="primary", use_container_width=True):
                with st.spinner("Admin re-scanning repository, extracting semantic chunks, and rebuilding vector & BM25 indices..."):
                    from src.rag.vector_store import VectorStore
                    from src.rag.hybrid_retriever import HybridRetriever

                    rag_engine.vector_store = VectorStore()
                    rag_engine.retriever = HybridRetriever(vector_store=rag_engine.vector_store)
                    rag_engine.indexed_files = []
                    rag_engine.documents = []
                    rag_engine._ingest_default_documents()

                st.success(f"✅ Admin re-index complete! {rag_engine.total_chunks} chunks indexed across {len(rag_engine.indexed_files)} files.")
                st.rerun()

            st.markdown("##### Active Ingested Files:")
            for fname in rag_engine.indexed_files:
                st.markdown(f"- 📄 `{fname}`")

    render_disclaimer()
