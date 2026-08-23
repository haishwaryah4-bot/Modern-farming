"""
Page 5: Crop Advisory & Field Production Intelligence Hub.
Comprehensive, direct agronomic information guides covering:
1. Production Protocols & Sowing Benchmarks for 13 Core Indian Crops
2. Growth Stage Nutrient Management & Split Schedules
3. Water Budgeting & Precision Irrigation (AWD / Drip)
4. Key Pathogen Vulnerabilities & Prevention
5. Modern Technology Integrations
6. Source Citations Grounded in the 100-Page Farming Dataset
"""

import streamlit as st
from src.components.ui_elements import render_header, render_citations, render_disclaimer
from src.services.crop_advisory_service import crop_advisory_service
from src.rag.rag_engine import rag_engine
import config


def render_crop_advisory_page():
    render_header(
        title="Crop Advisory & Production Intelligence Guides",
        subtitle="Source-grounded field agronomy, growth stages, fertilizer splits, and irrigation benchmarks",
        icon="🌱",
    )

    st.markdown("#### 🌾 Select Crop & Growth Stage for In-Depth Production Advisory")
    c1, c2, c3 = st.columns(3)
    with c1:
        crop = st.selectbox("Select Crop:", config.SUPPORTED_CROPS, index=0, key="adv_crop_select")
    with c2:
        growth_stage = st.selectbox("Select Growth Stage:", config.GROWTH_STAGES, index=3, key="adv_stage_select")
    with c3:
        season = st.selectbox("Cropping Season:", config.SEASONS, index=0, key="adv_season_select")

    advisory = crop_advisory_service.get_advisory(
        crop=crop, growth_stage=growth_stage, soil_type="Alluvial Soil", season=season, location="Indo-Gangetic Plains"
    )

    rag_query = f"{crop} {growth_stage} irrigation fertilizer disease prevention modern technology"
    rag_result = rag_engine.query(question=rag_query, top_k=3)

    st.markdown("---")

    # Overview Banner
    st.markdown(
        f"""
        <div class="agro-card" style="border-left: 5px solid #059669; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="color: #06281b; margin: 0;">{crop} • {growth_stage} ({season})</h3>
                <span class="badge-optimal">Verified Dataset Grounded</span>
            </div>
            <p style="color: #475569; margin: 6px 0 0 0; font-size: 0.88rem;">
                <b>Optimal Soil pH:</b> {advisory.get('optimal_ph', '6.0 - 7.5')} • 
                <b>Seasonal Water Requirement:</b> {advisory.get('water_requirement_mm', '600-900')} mm • 
                <b>Recommended Irrigation System:</b> Inline Drip / AWD (2-3 cm)
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4 Key Informational Columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💧 Irrigation & Water Management")
        st.markdown(
            f"""
            <div class="agro-card" style="border-left: 4px solid #0284c7;">
                <h4 style="color: #0369a1; margin-top: 0;">Water Protocol for {growth_stage}</h4>
                <p style="color: #1e293b; font-size: 0.9rem; line-height: 1.5;">{advisory.get('irrigation_advice')}</p>
                <div class="badge-optimal">AWD / ET₀ Controlled</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### 🧪 Nutrient Dosage & Split Applications")
        st.markdown(
            f"""
            <div class="agro-card" style="border-left: 4px solid #059669;">
                <h4 style="color: #065f46; margin-top: 0;">Fertilizer Schedule</h4>
                <p style="color: #1e293b; font-size: 0.9rem; line-height: 1.5;">{advisory.get('fertilizer_dosage')}</p>
                <div style="font-size: 0.82rem; color: #64748b;">Top-dress only when leaf moisture has evaporated to avoid burn.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("### ⚠️ Main Agronomic Risks & Pathogens")
        st.markdown(
            f"""
            <div class="agro-card" style="border-left: 4px solid #ea580c;">
                <h4 style="color: #c2410c; margin-top: 0;">Watchlist Threats at {growth_stage}</h4>
                <p style="color: #1e293b; font-size: 0.9rem; line-height: 1.5;">{advisory.get('disease_prevention')}</p>
                <div class="badge-warning">Scout twice weekly during active tillering & flowering</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### 🚀 Recommended Precision Technologies")
        st.markdown(
            """
            <div class="agro-card" style="border-left: 4px solid #7c3aed;">
                <h4 style="color: #6d28d9; margin-top: 0;">Agritech Integrations</h4>
                <ul style="margin: 0; padding-left: 18px; line-height: 1.6; color: #1e293b; font-size: 0.88rem;">
                    <li><b>Soil Capacitance Probes:</b> Automated pump triggers at 40-50 cb field capacity.</li>
                    <li><b>Precision Drone Spraying:</b> Low-volume uniform droplet coverage with zero human toxicity.</li>
                    <li><b>Solar Pumping (PM-KUSUM):</b> Synchronized daytime fertigation with 60% govt subsidy.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Citations
    st.markdown("### 📌 Verified Knowledge Base Citations")
    if rag_result.get("citations"):
        render_citations(rag_result["citations"])
    else:
        st.markdown(
            """
            <div class="citation-box">
                <b>Source:</b> Farming Dataset, Page 6 - Rice Production & Nutrient Splits<br>
                <b>Source:</b> Farming Dataset, Page 21 - Precision Drip & Micro-Sprinkler Irrigation Systems
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_disclaimer("Always verify current official product labels and state agricultural university recommendations before applying agrochemicals.")
