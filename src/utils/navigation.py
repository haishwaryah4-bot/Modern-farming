"""
Navigation & State Management Helper for AgriSense AI.
Provides open, public information website navigation without any login barriers.
"""

import streamlit as st

PAGES = [
    "🏠 Home Portal",
    "📚 Knowledge Hub (RAG)",
    "🤖 AI Agronomist Agent",
    "🌱 Crop Advisory Guides",
    "🧪 Soil Health Analysis",
    "🔬 Disease & Pest Assistant",
    "🚀 Modern Technology Explorer",
    "📈 Mandi Market & MSP Insights",
]


def normalize_page_name(target: str) -> str:
    """Finds exact match for page from partial or full string."""
    if not target:
        return PAGES[0]
    target_lower = target.lower()
    for p in PAGES:
        if target == p:
            return p
        if ("home" in target_lower or "dashboard" in target_lower) and "home" in p.lower():
            return p
        if ("rag" in target_lower or "knowledge" in target_lower) and "knowledge" in p.lower():
            return p
        if ("agent" in target_lower or "copilot" in target_lower) and "agent" in p.lower():
            return p
        if "advisory" in target_lower and "advisory" in p.lower():
            return p
        if "soil" in target_lower and "soil" in p.lower():
            return p
        if ("disease" in target_lower or "pest" in target_lower) and "disease" in p.lower():
            return p
        if ("modern" in target_lower or "tech" in target_lower) and "modern" in p.lower():
            return p
        if ("market" in target_lower or "mandi" in target_lower or "msp" in target_lower) and "market" in p.lower():
            return p
    return PAGES[0]


def set_page(target: str):
    """
    Safely changes active page in session state.
    """
    exact_page = normalize_page_name(target)
    st.session_state["current_page"] = exact_page


def run_prompt_on_agent(prompt: str):
    """
    Loads prompt into session state and routes to AI Agriculture Agent.
    """
    st.session_state["active_agent_prompt"] = prompt
    st.session_state["dash_ai_input"] = prompt
    set_page("🤖 AI Agronomist Agent")
