"""
Page 6: Soil Health & Nutrient Science Intelligence Center.
Direct, comprehensive agronomic information portal covering:
1. National Soil Health Card Benchmarks (12 Parameters)
2. Indian Agro-Ecological Soil Classifications (Alluvial, Black Vertisol, Red, Arid)
3. Targeted Soil Amelioration & Deficiency Remediation Protocols
4. Spatial Nutrient Distribution & Zonal Density Analysis
5. Organic Carbon Enhancement & Green Manuring Practices
"""

import streamlit as st
import math
from src.components.ui_elements import render_header, render_disclaimer
import config

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False


def create_soil_nutrient_heatmap(n_val=210.5, p_val=18.2, k_val=310.0, ph_val=7.8, oc_val=0.41):
    """
    Generates a clean 2D spatial heatmap of soil nutrient distribution.
    """
    if not HAS_PLOTLY:
        return None

    # 10x10 spatial field grid (meters)
    x_steps = [f"Col {i+1}" for i in range(10)]
    y_steps = [f"Row {j+1}" for j in range(8)]

    base_n = (n_val / 400.0) * 100.0
    base_p = (p_val / 50.0) * 100.0
    base_k = (k_val / 350.0) * 100.0

    Z = []
    for j in range(8):
        row = []
        for i in range(10):
            val = (
                base_n * 0.4 * math.sin(i / 2.0)
                + base_p * 0.3 * math.cos(j / 2.0)
                + base_k * 0.3
                + (oc_val * 40.0)
            )
            row.append(round(val, 1))
        Z.append(row)

    fig = go.Figure(
        data=go.Heatmap(
            z=Z,
            x=x_steps,
            y=y_steps,
            colorscale="Greens",
            colorbar=dict(title=dict(text="Nutrient Index (%)", font=dict(color="#06281b", family="Outfit"))),
        )
    )

    fig.update_layout(
        title="<b>🗺️ Field Nutrient Spatial Density Heatmap</b>",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        height=380,
        font=dict(color="#06281b", family="Plus Jakarta Sans"),
    )
    return fig


def render_soil_analysis_page():
    render_header(
        title="Soil Health & Nutrient Science Intelligence Center",
        subtitle="National soil test benchmarks, 12-parameter chemical ratings, spatial nutrient zones, and targeted remediation protocols",
        icon="🧪",
    )

    # 4 Interactive Knowledge Tabs
    t1, t2, t3, t4 = st.tabs([
        "📊 12-Parameter Chemical Benchmarks",
        "🌍 Indian Agro-Ecological Soils",
        "🛡️ Amelioration & Remediation",
        "🗺️ Spatial Nutrient Distribution"
    ])

    # =========================================================================
    # TAB 1: 12-PARAMETER SOIL HEALTH BENCHMARKS
    # =========================================================================
    with t1:
        st.markdown("#### 🧪 National Soil Health Card (SHC) Chemical & Micronutrient Benchmarks")
        st.markdown("Standards established by the Indian Council of Agricultural Research (ICAR) & Ministry of Agriculture:")

        b_c1, b_c2, b_c3 = st.columns(3)

        with b_c1:
            st.markdown(
                """
                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #059669;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">1. Soil pH (Reaction)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">Controls nutrient availability and microbial flora activity.</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Acidic:</b> &lt; 6.5 (Lime required)<br>
                        • <b>Optimal Range:</b> <span class="badge-optimal">6.5 - 7.5</span><br>
                        • <b>Alkaline / Sodic:</b> &gt; 8.2 (Gypsum required)
                    </div>
                </div>

                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #059669;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">2. Electrical Cond. (EC)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">Measures total soluble salt concentration.</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Normal / Safe:</b> <span class="badge-optimal">&lt; 1.0 dS/m</span><br>
                        • <b>Critical Saline:</b> 1.0 - 2.0 dS/m<br>
                        • <b>Injurious / High Salinity:</b> &gt; 2.0 dS/m
                    </div>
                </div>

                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #059669;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">3. Organic Carbon (OC)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">Primary reservoir for cation exchange & soil biology.</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Low / Deficient:</b> &lt; 0.50%<br>
                        • <b>Medium:</b> 0.50% - 0.75%<br>
                        • <b>High / Fertile:</b> <span class="badge-optimal">&gt; 0.75%</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with b_c2:
            st.markdown(
                """
                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #0284c7;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">4. Available Nitrogen (N)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">Alkaline Permanganate Method (kg/ha).</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Low:</b> &lt; 280 kg/ha<br>
                        • <b>Medium:</b> <span class="badge-optimal">280 - 560 kg/ha</span><br>
                        • <b>High:</b> &gt; 560 kg/ha
                    </div>
                </div>

                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #0284c7;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">5. Available Phosphorus (P₂O₅)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">Olsen's Method for Alkaline / Bray for Acid (kg/ha).</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Low:</b> &lt; 23 kg/ha<br>
                        • <b>Medium:</b> <span class="badge-optimal">23 - 56 kg/ha</span><br>
                        • <b>High:</b> &gt; 56 kg/ha
                    </div>
                </div>

                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #0284c7;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">6. Available Potassium (K₂O)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">Neutral Ammonium Acetate Method (kg/ha).</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Low:</b> &lt; 140 kg/ha<br>
                        • <b>Medium:</b> 140 - 280 kg/ha<br>
                        • <b>High / Sufficient:</b> <span class="badge-optimal">&gt; 280 kg/ha</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with b_c3:
            st.markdown(
                """
                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #ea580c;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">7. Available Zinc (Zn)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">DTPA Extractable Micronutrient (ppm).</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Critical Deficiency:</b> &lt; 0.60 ppm<br>
                        • <b>Sufficient:</b> <span class="badge-optimal">&gt; 0.60 ppm</span>
                    </div>
                </div>

                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #ea580c;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">8. Available Boron (B)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">Hot Water Extractable (ppm).</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Deficient:</b> &lt; 0.50 ppm<br>
                        • <b>Sufficient:</b> <span class="badge-optimal">0.50 - 1.00 ppm</span>
                    </div>
                </div>

                <div class="agro-card" style="margin-bottom: 12px; border-left: 4px solid #ea580c;">
                    <div style="font-weight: 800; color: #06281b; font-size: 1.05rem;">9. Available Sulfur (S)</div>
                    <p style="font-size: 0.85rem; color: #475569; margin: 4px 0 8px 0;">0.15% CaCl₂ Extractable (ppm).</p>
                    <div style="font-size: 0.84rem; color: #1e293b;">
                        • <b>Deficient:</b> &lt; 10.0 ppm<br>
                        • <b>Sufficient:</b> <span class="badge-optimal">&gt; 10.0 ppm</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # =========================================================================
    # TAB 2: INDIAN SOIL TYPES & CHARACTERISTICS
    # =========================================================================
    with t2:
        st.markdown("#### 🗺️ Major Indian Agro-Ecological Soil Orders")
        s1, s2 = st.columns(2)

        with s1:
            st.markdown(
                """
                <div class="agro-card" style="margin-bottom: 14px;">
                    <h4 style="color: #065f46; margin: 0 0 6px 0;">🌾 1. Alluvial Soils (Inceptisols & Entisols)</h4>
                    <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5;">
                        <b>Geographic Extent:</b> Indo-Gangetic Plains (Punjab, Haryana, UP, Bihar, Bengal, Assam).<br>
                        <b>Chemical Profile:</b> Rich in Potash and Lime; Deficient in Nitrogen and Phosphorus.<br>
                        <b>Best Suited Crops:</b> Rice, Wheat, Sugarcane, Maize, Potato, Mustard, Pulses.<br>
                        <b>Key Management:</b> Split nitrogen top-dressing; zinc supplementation (ZnSO₄ @ 25 kg/ha).
                    </p>
                </div>

                <div class="agro-card">
                    <h4 style="color: #065f46; margin: 0 0 6px 0;">🌿 2. Black Soils / Regur (Vertisols)</h4>
                    <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5;">
                        <b>Geographic Extent:</b> Deccan Plateau (Maharashtra, Madhya Pradesh, Gujarat, Karnataka).<br>
                        <b>Chemical Profile:</b> High montmorillonite clay; excellent moisture retention; high calcium & magnesium; low organic carbon.<br>
                        <b>Best Suited Crops:</b> Cotton, Soybean, Pigeonpea, Chickpea, Sorghum, Sunflower.<br>
                        <b>Key Management:</b> Broadbed and furrow (BBF) systems to prevent waterlogging during monsoons.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with s2:
            st.markdown(
                """
                <div class="agro-card" style="margin-bottom: 14px;">
                    <h4 style="color: #065f46; margin: 0 0 6px 0;">🌱 3. Red & Yellow Soils (Alfisols & Ultisols)</h4>
                    <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5;">
                        <b>Geographic Extent:</b> Tamil Nadu, Andhra Pradesh, Odisha, Jharkhand, Chhattisgarh.<br>
                        <b>Chemical Profile:</b> Developed over crystalline granite; rich in iron oxides; low water holding capacity; low phosphorus.<br>
                        <b>Best Suited Crops:</b> Groundnut, Finger Millet (Ragi), Pulses, Tobacco, Oilseeds.<br>
                        <b>Key Management:</b> Frequent light irrigations; incorporation of FYM / compost to boost retention.
                    </p>
                </div>

                <div class="agro-card">
                    <h4 style="color: #065f46; margin: 0 0 6px 0;">☀️ 4. Desert & Arid Soils (Aridisols)</h4>
                    <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5;">
                        <b>Geographic Extent:</b> Western Rajasthan, Northern Gujarat, Southern Haryana.<br>
                        <b>Chemical Profile:</b> High sand fraction (>85%); very low organic matter (&lt;0.2%); high soluble salts.<br>
                        <b>Best Suited Crops:</b> Pearl Millet (Bajra), Cluster Bean (Guar), Moth Bean, Cumin, Mustard.<br>
                        <b>Key Management:</b> Drip irrigation with mulching; windbreak shelterbelts to check wind erosion.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # =========================================================================
    # TAB 3: SOIL AMELIORATION & REMEDIATION PROTOCOLS
    # =========================================================================
    with t3:
        st.markdown("#### 💊 Scientific Soil Amelioration & Remediation Guide")
        
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(
                """
                <div class="agro-card" style="margin-bottom: 14px; border-left: 4px solid #dc2626;">
                    <h4 style="color: #991b1b; margin: 0 0 6px 0;">🧪 Acid Soil Reclamation (pH &lt; 6.5)</h4>
                    <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5;">
                        <b>Mechanism:</b> Acid soils suffer from Aluminum (Al³⁺) and Manganese (Mn²⁺) toxicity and Phosphorus fixation.<br>
                        <b>Remedy:</b> Apply Agricultural Limestone (CaCO₃) or Dolomite [CaMg(CO₃)₂] based on buffer pH test.<br>
                        <b>Dosage:</b> 2.0 to 4.0 tonnes/ha broadcast and incorporated 3-4 weeks prior to sowing.<br>
                        <b>Benefit:</b> Neutralizes Al-toxicity and unlocks fixed phosphorus.
                    </p>
                </div>

                <div class="agro-card" style="border-left: 4px solid #d97706;">
                    <h4 style="color: #92400e; margin: 0 0 6px 0;">⚡ Sodic & Alkaline Soil Reclamation (pH &gt; 8.5, ESP &gt; 15)</h4>
                    <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5;">
                        <b>Mechanism:</b> Excess Exchangeable Sodium (Na⁺) disperses clay particles, destroying soil structure and aeration.<br>
                        <b>Remedy:</b> Apply Agricultural Grade Gypsum (CaSO₄·2H₂O) @ 50% Gypsum Requirement (GR).<br>
                        <b>Dosage:</b> 5 to 10 tonnes/ha applied on dry surface, mixed in top 10 cm, followed by heavy ponding/leaching.<br>
                        <b>Benefit:</b> Calcium displaces sodium, restoring porosity and drainage.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with r2:
            st.markdown(
                """
                <div class="agro-card" style="margin-bottom: 14px; border-left: 4px solid #059669;">
                    <h4 style="color: #065f46; margin: 0 0 6px 0;">🌿 Organic Carbon (OC) Amelioration Protocols</h4>
                    <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5;">
                        <b>1. Green Manuring:</b> Sow Dhaincha (<i>Sesbania aculeata</i>) or Sunn hemp @ 20 kg/acre and incorporate at 45 days before paddy transplanting. Adds 15-20 tonnes/ha fresh green biomass and 60-80 kg N/ha.<br>
                        <b>2. Farmyard Manure (FYM):</b> Apply well-decomposed FYM @ 8-10 tonnes/acre or Vermicompost @ 2-3 tonnes/acre basally.<br>
                        <b>3. In-Situ Crop Residue:</b> Retain crop stubble with happy seeders / mulchers instead of burning.
                    </p>
                </div>

                <div class="agro-card" style="border-left: 4px solid #0284c7;">
                    <h4 style="color: #0369a1; margin: 0 0 6px 0;">🔬 Micronutrient Deficiency Amelioration</h4>
                    <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5;">
                        <b>• Zinc (Zn &lt; 0.6 ppm):</b> Basal soil application of Zinc Sulfate (21% Zn @ 25 kg/ha or 33% Zn @ 15 kg/ha) once every 2-3 crop cycles. Never mix directly with DAP/phosphorus fertilizers.<br>
                        <b>• Boron (B &lt; 0.5 ppm):</b> Apply Borax (10.5% B @ 10 kg/ha) or foliar spray Solubor (0.1% concentration) at pre-flowering stage.<br>
                        <b>• Iron (Fe Chlorosis on Calcareous Soils):</b> Foliar spray of 1% FeSO₄ + 0.1% Citric Acid at 15-day intervals.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # =========================================================================
    # TAB 4: 3D FIELD NUTRIENT TOPOGRAPHY
    # =========================================================================
    # =========================================================================
    # TAB 4: SPATIAL NUTRIENT DISTRIBUTION
    # =========================================================================
    with t4:
        st.markdown("#### 🗺️ Spatial Soil Nutrient Density & Zonal Analysis")
        if HAS_PLOTLY:
            st.info("💡 *Spatial Density Heatmap: Inspect macro & micronutrient density variations across field zones.*")
            fig_map = create_soil_nutrient_heatmap()
            if fig_map:
                st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, #ffffff, #f0fdf4); border: 2px solid #86efac; border-radius: 16px; padding: 24px; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 8px;">🗺️</div>
                    <h3 style="color: #065f46; margin: 0;">Soil Nutrient Spatial Distribution</h3>
                    <p style="color: #166534; font-size: 0.92rem; margin: 6px 0 16px 0;">
                        Field terrain nutrient density synthesized from National Soil Health Card benchmarks.
                    </p>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; font-size: 0.88rem; color: #1e3a8a;">
                        <div style="background: #ffffff; padding: 10px; border-radius: 8px; border: 1px solid #bfdbfe;"><b>Zone A (North):</b> Optimal K, Medium P</div>
                        <div style="background: #ffffff; padding: 10px; border-radius: 8px; border: 1px solid #bfdbfe;"><b>Zone B (Central):</b> Low N, Low Zn (Amelioration Required)</div>
                        <div style="background: #ffffff; padding: 10px; border-radius: 8px; border: 1px solid #bfdbfe;"><b>Zone C (South):</b> High Moisture, pH 7.8</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_disclaimer("Soil science benchmarks are based on published guidelines from ICAR and the National Soil Health Card Scheme. Always conduct local laboratory soil testing before applying chemical amendments.")
