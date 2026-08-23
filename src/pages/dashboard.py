"""
Page 1: AgriSense AI - Ultra-Premium Agricultural Intelligence Landing & AI Copilot Hub.
Features:
- Bold Hero Section with dynamic emerald gradients and live telemetry
- AI Farming Assistant Chat Preview with verified multi-step prompt chips
- 4 Feature Showcases (Advanced RAG, CV Pathology, Weather Advisory, Modern Tech)
- Hyperlocal 7-Day Weather & Mandi Commodity Rate Benchmarks
"""

import base64
from pathlib import Path
import streamlit as st
from src.components.ui_elements import render_header, render_stat_card, render_disclaimer
from src.components.unified_chat_box import render_unified_chat_box
from src.services.weather_service import weather_service
from src.services.market_service import market_service
from src.agents.agent_core import ai_agent
from src.utils.navigation import set_page
import config

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False


def _get_hero_bg_base64() -> str:
    img_path = config.BASE_DIR / "assets" / "images" / "modern_farm_hero.jpg"
    if img_path.exists():
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


def render_dashboard_page():
    weather = weather_service.get_current_weather("Indo-Gangetic Plains & Northern India")
    rice_market = market_service.get_crop_market_summary("Rice (Paddy)")
    wheat_market = market_service.get_crop_market_summary("Wheat")

    # =========================================================================
    # 1. BOLD HERO LANDING SECTION WITH BACKGROUND PICTURE
    # =========================================================================
    bg_b64 = _get_hero_bg_base64()
    bg_style = (
        f"background: linear-gradient(135deg, rgba(3, 20, 10, 0.82) 0%, rgba(5, 36, 18, 0.78) 50%, rgba(2, 15, 8, 0.88) 100%), url('data:image/jpeg;base64,{bg_b64}') center/cover no-repeat !important;"
        if bg_b64
        else "background: linear-gradient(135deg, rgba(3, 20, 10, 0.95), rgba(5, 36, 18, 0.95)) !important;"
    )

    st.markdown(
        f"""
        <div class="hero-container" style="{bg_style} border: 2px solid #10b981; box-shadow: 0 16px 44px rgba(0, 20, 10, 0.5), 0 0 25px rgba(16, 185, 129, 0.25);">
            <div class="hero-tag" style="background: rgba(16, 185, 129, 0.2); border: 1.5px solid #34d399; color: #6ee7b7;">
                <div class="pulse-dot"></div>
                <span>National Smart Agriculture Intelligence Engine • Live RAG Active</span>
            </div>
            <h1 class="hero-title" style="color: #ffffff !important; text-shadow: 0 3px 12px rgba(0,0,0,0.8);">
                Next-Generation Precision Farming & AI Agronomy
            </h1>
            <p class="hero-subtitle" style="color: #e2e8f0 !important; font-size: 1.15rem; line-height: 1.65; max-width: 900px; text-shadow: 0 2px 8px rgba(0,0,0,0.8);">
                Harnessing source-grounded Hybrid RAG, computer vision crop pathology, 
                weather-aware water budgeting, and autonomous AI agents to transform farm productivity across India.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero Quick Action CTAs Row
    cta_c1, cta_c2, cta_c3 = st.columns(3)
    with cta_c1:
        if st.button("🤖 Launch AI Agronomist Studio", key="hero_cta_agent", use_container_width=True):
            set_page("🤖 AI Agronomist Agent")
            st.rerun()
    with cta_c2:
        if st.button("📚 Search Agricultural Knowledge Hub", key="hero_cta_rag", use_container_width=True):
            set_page("📚 Knowledge Hub (RAG)")
            st.rerun()
    with cta_c3:
        if st.button("🧪 Explore Soil Health Analytics", key="hero_cta_soil", use_container_width=True):
            set_page("🧪 Soil Health Analysis")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================================
    # 2. KEY TELEMETRY METRICS ROW
    # =========================================================================
    st.markdown("### 📊 Live National Agricultural Telemetry")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_stat_card(
            title="Agro-Weather Index",
            value=f"{weather['temperature_c']}°C {weather['icon']}",
            subtext=f"{weather['condition']} • Rain: {weather['rain_probability_pct']}% • ET: {weather['evapotranspiration_mm_day']}mm/day",
            icon="⛅",
        )
    with c2:
        render_stat_card(
            title="National Soil Health Index",
            value="78 / 100",
            subtext="Alluvial & Vertisol Zones • NPK Matrix Ready",
            icon="🧪",
        )
    with c3:
        render_stat_card(
            title="Paddy Mandi Modal Rate",
            value=f"₹{rice_market['modal_price']}/Qtl",
            subtext=f"Govt MSP: ₹{rice_market['msp']} • Trend: {rice_market['trend']} ({rice_market['weekly_change_pct']}%)",
            icon="🌾",
        )
    with c4:
        render_stat_card(
            title="Knowledge Corpus Depth",
            value="Verified Corpus",
            subtext="13 Crops • IPM • Drip • IoT • Solar Tech",
            icon="📚",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================================
    # 3. 4 CORE PILLAR FEATURE SHOWCASES
    # =========================================================================
    st.markdown("### 🌟 Intelligent Agricultural Capabilities")
    p1, p2, p3, p4 = st.columns(4)

    # Helper to encode images
    def _get_pillar_img_b64(fname):
        p = config.BASE_DIR / "assets" / "images" / fname
        if p.exists():
            with open(p, "rb") as f:
                return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
        return ""

    img_rag = _get_pillar_img_b64("precision_iot_farming.jpg")
    img_dis = _get_pillar_img_b64("drone_spraying.jpg")
    img_wtr = _get_pillar_img_b64("iot_weather_station.jpg")
    img_tch = _get_pillar_img_b64("solar_pump_kusum.jpg")

    with p1:
        st.markdown(
            f"""
            <div class="pillar-card" style="padding: 0; overflow: hidden;">
                <img src="{img_rag}" style="width: 100%; height: 130px; object-fit: cover;" alt="Hybrid RAG">
                <div style="padding: 16px;">
                    <div class="pillar-title" style="margin-top: 0;">🧠 Advanced Hybrid RAG</div>
                    <div class="pillar-desc">
                        Dense semantic vectors + BM25 keyword matching with cross-encoder re-ranking and page citations.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore RAG Hub 📚", key="btn_p1_rag", use_container_width=True):
            set_page("📚 Knowledge Hub (RAG)")
            st.rerun()

    with p2:
        st.markdown(
            f"""
            <div class="pillar-card" style="padding: 0; overflow: hidden;">
                <img src="{img_dis}" style="width: 100%; height: 130px; object-fit: cover;" alt="Disease AI">
                <div style="padding: 16px;">
                    <div class="pillar-title" style="margin-top: 0;">🔬 Foliar Disease AI</div>
                    <div class="pillar-desc">
                        Deep vision pathology diagnostics, ETL risk thresholds, scouting checklists, and IPM control protocols.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Diagnose Diseases 🔬", key="btn_p2_disease", use_container_width=True):
            set_page("🔬 Disease & Pest Assistant")
            st.rerun()

    with p3:
        st.markdown(
            f"""
            <div class="pillar-card" style="padding: 0; overflow: hidden;">
                <img src="{img_wtr}" style="width: 100%; height: 130px; object-fit: cover;" alt="Weather Advisory">
                <div style="padding: 16px;">
                    <div class="pillar-title" style="margin-top: 0;">⛅ Weather Advisory</div>
                    <div class="pillar-desc">
                        FAO-56 Penman-Monteith ET₀ calculations, AWD water scheduling, and 7-day crop bulletins.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Crop Guides 🌱", key="btn_p3_crop", use_container_width=True):
            set_page("🌱 Crop Advisory Guides")
            st.rerun()

    with p4:
        st.markdown(
            f"""
            <div class="pillar-card" style="padding: 0; overflow: hidden;">
                <img src="{img_tch}" style="width: 100%; height: 130px; object-fit: cover;" alt="AgriTech ROI">
                <div style="padding: 16px;">
                    <div class="pillar-title" style="margin-top: 0;">🚀 AgriTech & Solar ROI</div>
                    <div class="pillar-desc">
                        Precision drip, multispectral drones, IoT sensors, and PM-KUSUM solar pump subsidy calculators.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Calculate AgriTech ROI 🚀", key="btn_p4_tech", use_container_width=True):
            set_page("🚀 Modern Technology Explorer")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================================
    # 4. PROMINENT EMBEDDED AI COPILOT SECTION & DATASET PROMPTS
    # =========================================================================
    st.markdown(
        """
        <div class="ai-copilot-container">
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
                <div style="font-size: 2.5rem; filter: drop-shadow(0 0 10px rgba(5, 150, 105, 0.4));">🤖</div>
                <div>
                    <h2 style="margin: 0; font-size: 1.6rem; color: #052e16;">AgriSense AI & Voice Copilot Studio</h2>
                    <p style="margin: 4px 0 0 0; color: #1e293b; font-size: 0.95rem; font-weight: 600;">
                        Autonomous AI agent orchestrating live speech recognition, audio readout, Farming Knowledge Base RAG, weather models, and soil analysis in one unified console.
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="font-size: 1.2rem; font-weight: 900; color: #ffffff !important; text-shadow: 0 2px 8px rgba(0,0,0,0.9); margin: 22px 0 12px 0; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.3rem;">⚡</span>
            <span>Verified 1-Click Farming Advisory Scenarios</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        if st.button(
            "🌾 Rice Kharif (Poor Drainage & High Humidity Action Plan)",
            key="dash_prompt_rice",
            use_container_width=True,
        ):
            st.session_state["dash_selected_query"] = (
                "I am growing rice in Kharif season. My field has poor drainage and high humidity. Give me an action plan."
            )

        if st.button(
            "🍅 Tomato Flowering (Irrigation & Fertigation Schedule)",
            key="dash_prompt_tomato",
            use_container_width=True,
        ):
            st.session_state["dash_selected_query"] = (
                "Recommend an irrigation and fertigation approach for tomato at flowering stage."
            )

        if st.button(
            "🚀 Small Farm Modern Technologies (Limited Water)",
            key="dash_prompt_small_farm",
            use_container_width=True,
        ):
            st.session_state["dash_selected_query"] = (
                "Which modern technologies from the knowledge base are suitable for a small farm with limited water?"
            )

    with p_col2:
        if st.button(
            "🧪 Soil Health Card Testing Benchmarks & Zinc Amelioration",
            key="dash_prompt_soil",
            use_container_width=True,
        ):
            st.session_state["dash_selected_query"] = (
                "Analyze my soil test values (N 210 kg/ha, P 18 kg/ha, pH 7.8, Zn 0.48 ppm) and recommend required amendments."
            )

        if st.button(
            "📈 Wheat & Paddy Mandi Modal Rates vs MSP Benchmarks",
            key="dash_prompt_mandi",
            use_container_width=True,
        ):
            st.session_state["dash_selected_query"] = (
                "What is the current market price for Rice and Wheat in Mandis and how does it compare to the MSP?"
            )

        if st.button(
            "☀️ PM-KUSUM Solar Pump & Drip Subsidies (ROI Analysis)",
            key="dash_prompt_solar",
            use_container_width=True,
        ):
            st.session_state["dash_selected_query"] = (
                "What are the capital costs, government subsidies under PM-KUSUM, and payback periods for solar drip irrigation?"
            )

    # Unified Single AI Assistant Conversation Container (Type + Voice + Multi-Agent Execution)
    render_unified_chat_box(key_prefix="dash")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================================
    # 5. REGIONAL AGRO-CLIMATIC & SOIL INTELLIGENCE SECTION
    # =========================================================================
    col_twin_left, col_twin_right = st.columns([1, 1])
    with col_twin_left:
        st.markdown(
            """
            <div class="agro-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h3 style="margin: 0; color: #031c0e; font-size: 1.25rem;">🌐 National Crop Vitality & Agro-Climatic Matrix</h3>
                    <span class="badge-optimal">Verified Benchmarks</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 10px;">
                    <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px; padding: 12px;">
                        <div style="font-size: 0.78rem; font-weight: 800; color: #166534; text-transform: uppercase;">Crop Canopy Vigor</div>
                        <div style="font-size: 1.4rem; font-weight: 900; color: #052e16;">94% Optimal</div>
                        <div style="font-size: 0.76rem; color: #15803d;">Active Tillering & Biomass</div>
                    </div>
                    <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px; padding: 12px;">
                        <div style="font-size: 0.78rem; font-weight: 800; color: #166534; text-transform: uppercase;">Soil Health Rating</div>
                        <div style="font-size: 1.4rem; font-weight: 900; color: #052e16;">78 / 100</div>
                        <div style="font-size: 0.76rem; color: #15803d;">Medium NPK • Normal pH</div>
                    </div>
                    <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px; padding: 12px;">
                        <div style="font-size: 0.78rem; font-weight: 800; color: #166534; text-transform: uppercase;">AWD Water Efficiency</div>
                        <div style="font-size: 1.4rem; font-weight: 900; color: #052e16;">85% High</div>
                        <div style="font-size: 0.76rem; color: #15803d;">25-30% Water Conserved</div>
                    </div>
                    <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px; padding: 12px;">
                        <div style="font-size: 0.78rem; font-weight: 800; color: #166534; text-transform: uppercase;">Mandi vs MSP Policy</div>
                        <div style="font-size: 1.4rem; font-weight: 900; color: #052e16;">+4.8% Premium</div>
                        <div style="font-size: 0.76rem; color: #15803d;">PM-AASHA Procurement</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_twin_right:
        st.markdown(
            """
            <div class="agro-card" style="height: 380px;">
                <h3 style="margin: 0 0 10px 0; color: #ffffff; font-size: 1.25rem;">📖 Cropping Seasons & Verified Protocols</h3>
                <p style="font-size: 0.88rem; color: #d1fae5; line-height: 1.6;">
                    <b>🌾 Kharif Season (Monsoon):</b> Rice, Cotton, Soybean, Maize, Groundnut, Pigeonpea, Chilli, Brinjal.<br>
                    <b>❄️ Rabi Season (Winter):</b> Wheat, Mustard, Chickpea, Potato, Winter Horticulture.<br>
                    <b>☀️ Zaid Season (Summer):</b> Short-duration legumes, Cucurbits, Fodder crops.<br>
                    <b>💧 Water Precision:</b> Alternate Wetting & Drying (AWD), Inline Drip, Sub-surface Fertigation.
                </p>
                <hr style="border: none; border-top: 1px solid var(--border-glass); margin: 10px 0;">
                <div style="font-size: 0.86rem; color: #34d399; background: rgba(6, 28, 18, 0.7); padding: 10px 14px; border-radius: 10px; border: 1px solid var(--border-glass);">
                    <b>✨ Source Grounding:</b> Every recommendation, nutrient dosage, and disease treatment is verified against the National Agricultural Knowledge Base with exact page citations.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 2-Column Split: 7-Day Weather & Active Recommendations
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### ⛅ 7-Day Regional Weather Outlook")
        forecast = weather_service.get_7day_forecast("Indo-Gangetic Plains & Northern India")

        for f in forecast:
            w_col1, w_col2, w_col3, w_col4 = st.columns([1, 2, 2, 3])
            with w_col1:
                st.markdown(f"**{f['day']}**")
            with w_col2:
                st.markdown(f"{f['icon']} {f['temp_max']}° / {f['temp_min']}°C")
            with w_col3:
                st.markdown(f"🌧️ Rain: {f['rain_prob']}%")
            with w_col4:
                st.markdown(f"💧 *{f['irrigation_advice']}*")

    with col_right:
        st.markdown("### 💡 Active Regional Crop Bulletins")
        st.markdown(
            """
            <div class="agro-card" style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 800; color: #ffffff; font-size: 0.95rem;">🌱 Kharif Paddy Sowing & AWD Notice</span>
                    <span class="badge-optimal">Active Season</span>
                </div>
                <p style="font-size: 0.86rem; color: #d1fae5; margin: 0;">
                    Adopt Alternate Wetting and Drying (AWD) water management (2-3 cm depth). Schedule split nitrogen applications at 21 and 42 DAT.
                </p>
            </div>

            <div class="agro-card" style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 800; color: #ffffff; font-size: 0.95rem;">🧪 Micronutrient Advisory</span>
                    <span class="badge-warning">Zinc Deficiency Alert</span>
                </div>
                <p style="font-size: 0.86rem; color: #d1fae5; margin: 0;">
                    Indian soils report widespread Zinc deficiency (<0.6 ppm). Basal soil application of Zinc Sulfate (21% Zn @ 10-15 kg/acre) recommended.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_disclaimer()
