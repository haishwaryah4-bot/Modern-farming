"""
AgriSense AI - National Smart Agriculture Information Platform.
Master Streamlit Application Entrypoint (Open Public Access, Zero Login Barrier).
"""

import streamlit as st
import os
from pathlib import Path

# Streamlit Page Configuration
st.set_page_config(
    page_title="AgriSense AI | National Smart Agriculture Platform",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load and inject custom AgriTech CSS Design System with Full-Page Background Picture
import base64
css_path = Path(__file__).resolve().parent / "assets" / "styles.css"
img_path = Path(__file__).resolve().parent / "assets" / "images" / "modern_farm_hero.jpg"
bg_b64 = ""
if img_path.exists():
    with open(img_path, "rb") as img_f:
        bg_b64 = base64.b64encode(img_f.read()).decode("utf-8")

if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
        if bg_b64:
            bg_css = f"""
            html, body, [class*="css"], .stApp {{
                background-image: 
                    linear-gradient(170deg, rgba(2, 11, 5, 0.88) 0%, rgba(5, 26, 14, 0.84) 40%, rgba(10, 41, 24, 0.90) 100%),
                    url('data:image/jpeg;base64,{bg_b64}') !important;
                background-size: cover !important;
                background-position: center !important;
                background-attachment: fixed !important;
            }}
            """
            css_content += bg_css
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# Import topbar, sidebar, and page modules
from src.components.topbar import render_topbar
from src.components.sidebar import render_sidebar
from src.pages.dashboard import render_dashboard_page
from src.pages.knowledge_hub import render_knowledge_hub_page
from src.pages.ai_agent import render_ai_agent_page
from src.pages.crop_advisory import render_crop_advisory_page
from src.pages.soil_analysis import render_soil_analysis_page
from src.pages.disease_assistant import render_disease_assistant_page
from src.pages.modern_tech import render_modern_tech_page
from src.pages.market_insights import render_market_insights_page


def main():
    # Render Navigation Sidebar
    sidebar_page = render_sidebar()

    # Render Top Navigation Bar (live indicators + quick navigation pills)
    render_topbar()

    # Current Page Resolution
    selected_page = st.session_state.get("current_page", sidebar_page)

    # 8-Page Open Portal Router
    if "Home" in selected_page or "Dashboard" in selected_page:
        render_dashboard_page()
    elif "Knowledge" in selected_page or "RAG" in selected_page:
        render_knowledge_hub_page()
    elif "Agent" in selected_page or "Copilot" in selected_page:
        render_ai_agent_page()
    elif "Advisory" in selected_page or "Crop" in selected_page:
        render_crop_advisory_page()
    elif "Soil" in selected_page:
        render_soil_analysis_page()
    elif "Disease" in selected_page or "Pest" in selected_page:
        render_disease_assistant_page()
    elif "Modern" in selected_page or "Tech" in selected_page:
        render_modern_tech_page()
    elif "Market" in selected_page or "Mandi" in selected_page or "MSP" in selected_page:
        render_market_insights_page()
    else:
        render_dashboard_page()


if __name__ == "__main__":
    main()
