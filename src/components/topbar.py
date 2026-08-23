"""
Top Navigation Bar and Global Status Component for AgriSense AI.
Provides open public website navigation across all knowledge hubs and live AI status.
"""

import streamlit as st
import config
from src.utils.navigation import set_page, normalize_page_name


def render_topbar():
    """
    Renders top navigation pill bar and live system indicators.
    """
    pages = [
        ("🏠 Home", "🏠 Home Portal"),
        ("📚 RAG Knowledge", "📚 Knowledge Hub (RAG)"),
        ("🤖 AI Agent", "🤖 AI Agronomist Agent"),
        ("🌱 Crop Guides", "🌱 Crop Advisory Guides"),
        ("🧪 Soil Health", "🧪 Soil Health Analysis"),
        ("🔬 Pest & Disease", "🔬 Disease & Pest Assistant"),
        ("🚀 AgriTech", "🚀 Modern Technology Explorer"),
        ("📈 Mandi Market", "📈 Mandi Market & MSP Insights"),
    ]

    current_page = normalize_page_name(st.session_state.get("current_page", "🏠 Home Portal"))

    # Top Brand Header
    st.markdown(
        """
        <div class="top-nav-bar" style="background: #ffffff !important; border: 2px solid #059669 !important;">
            <div class="top-brand">
                <span style="font-size: 1.5rem;">🌾</span>
                <span style="color: #031c0e !important; font-weight: 900 !important; font-size: 1.35rem !important;">AgriSense AI</span>
                <span style="font-size: 0.88rem !important; font-weight: 700 !important; color: #334155 !important; margin-left: 8px;">
                    • National Smart Agriculture Information Portal
                </span>
            </div>
            <div class="live-indicator" style="background: #ecfdf5 !important; border: 1.5px solid #059669 !important;">
                <span style="display:inline-block; width:8px; height:8px; background:#10b981; border-radius:50%; margin-right:4px;"></span>
                <span style="color: #047857 !important; font-weight: 800 !important; font-size: 0.86rem !important;">National Agricultural Portal • Live Intelligence Active</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top Navigation Buttons Row
    cols = st.columns(len(pages))
    for idx, (label, target_page) in enumerate(pages):
        with cols[idx]:
            is_active = (current_page == target_page)
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"top_nav_btn_{idx}", type=btn_type, use_container_width=True):
                set_page(target_page)
                st.rerun()

    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
