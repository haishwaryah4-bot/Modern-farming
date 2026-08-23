"""
Application Sidebar Component for AgriSense AI.
Provides open public navigation, OpenAI settings configuration, and portal statistics.
"""

import os
import streamlit as st
import config
from src.utils.navigation import PAGES, normalize_page_name
from src.services.llm_service import llm_client


def render_sidebar():
    """
    Renders the modern agricultural portal sidebar with public knowledge links and OpenAI configuration.
    """
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding-bottom: 14px; border-bottom: 1.5px solid rgba(52, 211, 153, 0.3); margin-bottom: 18px;">
                <div style="font-size: 2.4rem; margin-bottom: 4px;">🌾</div>
                <h3 style="margin: 0; color: #ffffff; font-weight: 900; font-size: 1.4rem; letter-spacing: -0.02em;">AgriSense AI</h3>
                <p style="font-size: 0.82rem; color: #6ee7b7; margin: 2px 0 0 0; font-weight: 700;">Smart Agriculture Information Portal</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Initialize current_page
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = PAGES[0]

        # Ensure current_page is normalized
        current = normalize_page_name(st.session_state["current_page"])
        st.session_state["current_page"] = current

        # Render Selectbox using index without conflicting key
        selected_page = st.selectbox(
            "🧭 Portal Navigation",
            PAGES,
            index=PAGES.index(current) if current in PAGES else 0,
        )

        # If user selected a new page via the selectbox, update state and rerun
        if selected_page != current:
            st.session_state["current_page"] = selected_page
            st.rerun()

        st.markdown("---")

        # =========================================================================
        # ⚡ OpenAI API & Intelligence Engine Settings
        # =========================================================================
        with st.expander("⚡ OpenAI & Intelligence Engine", expanded=False):
            st.markdown(
                """
                <div style="font-size: 0.82rem; color: #cbd5e1; margin-bottom: 8px;">
                    Configure your <b>OpenAI API Key</b> to power the AI Assistant with live GPT-4o intelligence:
                </div>
                """,
                unsafe_allow_html=True,
            )

            current_key = st.session_state.get("openai_api_key", os.environ.get("OPENAI_API_KEY", config.OPENAI_API_KEY or ""))
            input_key = st.text_input(
                "OpenAI API Key:",
                value=current_key,
                type="password",
                placeholder="sk-proj-...",
                key="sidebar_openai_key_input",
                help="Your key is stored securely in this session.",
            )

            current_model = st.session_state.get("openai_model", os.environ.get("OPENAI_MODEL", config.OPENAI_MODEL or "gpt-4o-mini"))
            models_list = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
            model_index = models_list.index(current_model) if current_model in models_list else 0
            
            selected_model = st.selectbox(
                "OpenAI Model:",
                models_list,
                index=model_index,
                key="sidebar_openai_model_select",
            )

            col_test, col_save = st.columns(2)
            with col_test:
                if st.button("🔌 Test API", key="btn_test_openai", use_container_width=True):
                    with st.spinner("Testing OpenAI connection..."):
                        res = llm_client.test_connection(test_key=input_key, test_model=selected_model)
                        if res["success"]:
                            st.session_state["openai_api_key"] = input_key
                            st.session_state["openai_model"] = selected_model
                            os.environ["OPENAI_API_KEY"] = input_key
                            os.environ["OPENAI_MODEL"] = selected_model
                            st.success(res["message"])
                        else:
                            st.error(res["message"])

            with col_save:
                if st.button("💾 Apply", key="btn_save_openai", use_container_width=True):
                    st.session_state["openai_api_key"] = input_key
                    st.session_state["openai_model"] = selected_model
                    os.environ["OPENAI_API_KEY"] = input_key
                    os.environ["OPENAI_MODEL"] = selected_model
                    st.success("✅ OpenAI Configuration Active!")

            # Live Engine Status Badge
            if llm_client.is_live:
                st.markdown(
                    f"""
                    <div style="background: #ecfdf5; border: 1.5px solid #10b981; border-radius: 8px; padding: 6px 10px; margin-top: 8px; font-size: 0.78rem; color: #047857; font-weight: 800;">
                        🟢 Live OpenAI Engine ({llm_client.model}) Active
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 6px 10px; margin-top: 8px; font-size: 0.78rem; color: #475569; font-weight: 700;">
                        ⚪ Offline Agricultural Reasoning Engine Active
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Portal Knowledge Scope
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.96); border: 1.5px solid #059669; border-radius: 12px; padding: 14px; margin-top: 10px; margin-bottom: 14px; box-shadow: 0 4px 14px rgba(0,0,0,0.25);">
                <div style="font-size: 0.8rem; font-weight: 900; color: #052e16; text-transform: uppercase; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                    <span>📖</span> Open Knowledge Scope
                </div>
                <div style="font-size: 0.84rem; color: #0f172a; line-height: 1.55; font-weight: 500;">
                    • <b>13 Core Crops:</b> Rice, Wheat, Maize, Cotton, Soybean, Pulses & Vegetables<br>
                    • <b>Cropping Seasons:</b> Kharif, Rabi, Zaid & Perennials<br>
                    • <b>12 Soil Parameters:</b> NPK, pH, EC, OC, Micronutrients<br>
                    • <b>Modern Tech:</b> Drip, Drones, IoT, AWS, Solar Pumps
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Knowledge Base Status Indicator
        with st.expander("📊 Knowledge Base & RAG Telemetry", expanded=False):
            from src.rag.rag_engine import rag_engine

            st.markdown(
                f"""
                <div style="font-size: 0.84rem; color: #0f172a; line-height: 1.5;">
                    <b>Dataset:</b> National Agricultural Knowledge Base<br>
                    <b>Embedding:</b> <code>all-MiniLM-L6-v2</code> 384-dim<br>
                    <b>Indexed Files:</b> {len(rag_engine.indexed_files)} active manuals<br>
                    <b>Total Chunks:</b> {rag_engine.total_chunks} vector chunks<br>
                    <b>Retrieval:</b> Hybrid (Dense + BM25 + Re-Ranking)<br>
                    <b>Citations:</b> Page-Level Verified
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Footer
        st.markdown(
            """
            <div style="margin-top: 24px; text-align: center; font-size: 0.76rem; color: #94a3b8; font-weight: 600;">
                AgriSense AI Information Platform<br>
                Open-Access Agricultural Decision Support
            </div>
            """,
            unsafe_allow_html=True,
        )

        return st.session_state["current_page"]
