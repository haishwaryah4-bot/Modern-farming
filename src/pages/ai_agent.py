import streamlit as st
from src.components.ui_elements import render_header, render_disclaimer
from src.components.unified_chat_box import render_unified_chat_box
from src.agents.agent_core import ai_agent
from src.agents.tools import TOOL_REGISTRY
import config


def render_ai_agent_page():
    render_header(
        title="AgriSense AI Assistant & Voice Studio",
        subtitle="Autonomous agricultural intelligence with live speech recognition, audio readout, and multi-agent reasoning in ONE unified chat box",
        icon="🌱",
    )

    farm = st.session_state.get("farm_profile", config.DEFAULT_FARM_PROFILE)

    # Active Tools Available Banner
    st.markdown(
        """
        <div style="font-size: 1.15rem; font-weight: 800; color: #ffffff !important; text-shadow: 0 2px 6px rgba(0,0,0,0.8); margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
            <span>🛠️</span>
            <span>Integrated Agent Tool Suite (8 Typed Tools + 🎙️ Voice Agent):</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(4)
    tool_keys = list(TOOL_REGISTRY.keys())
    for i, tkey in enumerate(tool_keys):
        tinfo = TOOL_REGISTRY[tkey]
        with cols[i % 4]:
            st.markdown(
                f"""
                <div class="tool-pill" title="{tinfo['description']}">
                    {tinfo['icon']} {tkey.replace('_', ' ').title()}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Control Row: Clear Memory & Active Context
    ctrl_col1, ctrl_col2 = st.columns([4, 1])
    with ctrl_col1:
        st.markdown(
            f"<div style='font-size: 0.92rem; color: #ffffff !important; text-shadow: 0 1px 4px rgba(0,0,0,0.8); padding-top: 8px; font-weight: 700;'><b>Active Context:</b> <span style='color: #6ee7b7;'>{farm.get('farmer_name')}</span> • {farm.get('selected_crop')} ({farm.get('season')}) • {farm.get('district')}, {farm.get('state')}</div>",
            unsafe_allow_html=True,
        )
    with ctrl_col2:
        if st.button("🗑️ Reset Chat Memory", key="btn_clear_agent_mem", use_container_width=True):
            st.session_state["studio_unified_chat_messages"] = []
            st.session_state["active_agent_prompt"] = None
            ai_agent.clear_memory()
            st.rerun()

    # Preset Multi-Step Dataset Prompts
    st.markdown(
        """
        <div style="font-size: 1.2rem; font-weight: 900; color: #ffffff !important; text-shadow: 0 2px 8px rgba(0,0,0,0.9); margin: 20px 0 12px 0; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.3rem;">💡</span>
            <span>Verified 1-Click Farming Advisory Scenarios</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    p_row1_c1, p_row1_c2, p_row1_c3 = st.columns(3)
    p_row2_c1, p_row2_c2, p_row2_c3 = st.columns(3)

    with p_row1_c1:
        if st.button("🌾 Rice Kharif (Drainage & Humidity)", key="btn_q_rice", use_container_width=True):
            st.session_state["studio_selected_query"] = (
                "I am growing rice in Kharif season. My field has poor drainage and high humidity. Give me an action plan."
            )
            st.rerun()
    with p_row1_c2:
        if st.button("🍅 Tomato Flowering (Fertigation Plan)", key="btn_q_tomato", use_container_width=True):
            st.session_state["studio_selected_query"] = (
                "Recommend an irrigation and fertigation approach for tomato at flowering stage."
            )
            st.rerun()
    with p_row1_c3:
        if st.button("🚀 Small Farm Tech (Limited Water)", key="btn_q_tech_small", use_container_width=True):
            st.session_state["studio_selected_query"] = (
                "Which modern technologies from the knowledge base are suitable for a small farm with limited water?"
            )
            st.rerun()

    with p_row2_c1:
        if st.button("🧪 Soil Health & Zinc Remediation", key="btn_q_soil_zinc", use_container_width=True):
            st.session_state["studio_selected_query"] = (
                "Analyze my soil test values (N 210 kg/ha, P 18 kg/ha, pH 7.8, Zn 0.48 ppm) and recommend required amendments."
            )
            st.rerun()
    with p_row2_c2:
        if st.button("🛡️ Cotton Pink Bollworm & Maize FAW", key="btn_q_pest_ipm", use_container_width=True):
            st.session_state["studio_selected_query"] = (
                "Compare pest management ETL thresholds and chemical vs biological controls for Pink Bollworm in Cotton and Fall Armyworm in Maize."
            )
            st.rerun()
    with p_row2_c3:
        if st.button("☀️ PM-KUSUM Solar Drip ROI", key="btn_q_kusum_roi", use_container_width=True):
            st.session_state["studio_selected_query"] = (
                "What are the capital costs, government subsidies under PM-KUSUM, and payback periods for solar drip irrigation?"
            )
            st.rerun()

    # Check if there is an active prompt pending from another page
    pending_prompt = st.session_state.get("active_agent_prompt")
    if pending_prompt:
        st.session_state["studio_selected_query"] = pending_prompt
        st.session_state["active_agent_prompt"] = None

    # Unified Single AI Assistant Conversation Container (Type + Voice + Multi-Agent Execution)
    render_unified_chat_box(key_prefix="studio")

    render_disclaimer()
