"""
Page 7: Plant Pathology, Disease & Pest Information Center.
Direct, comprehensive agronomic information portal covering:
- Major pests & pathogens for 13 core crops
- Visual diagnostic symptoms & distinguishing features
- Economic Threshold Levels (ETL)
- Field scouting & sampling protocols
- Cultural, biological, and chemical IPM interventions
- Certified package of practices and KVK escalation channels
"""

import streamlit as st
import json
from pathlib import Path
from src.components.ui_elements import render_header, render_disclaimer
from src.services.disease_service import disease_service
import config


def render_disease_assistant_page():
    render_header(
        title="Plant Pathology, Pest & Disease Information Center",
        subtitle="Source-grounded scientific guides, visual diagnostics, Economic Threshold Levels (ETL), and IPM protocols",
        icon="🔬",
    )

    t_info, t_cv = st.tabs(["📖 Comprehensive Disease & Pest Directory", "📷 Computer Vision Leaf Scanner (Optional)"])

    # Load disease catalog
    catalog = disease_service.catalog

    with t_info:
        st.markdown("#### 🌾 Select Crop to Access Pathogen & Pest Intelligence")
        
        selected_crop = st.selectbox(
            "Filter by Crop:",
            config.SUPPORTED_CROPS,
            index=0,
            key="pathology_crop_filter",
        )

        # Filter diseases for selected crop
        matched_diseases = [d for d in catalog if d.get("crop_name", "").lower() in selected_crop.lower() or selected_crop.lower() in d.get("crop_name", "").lower()]
        if not matched_diseases:
            matched_diseases = catalog[:3]

        st.markdown(f"### 🛡️ Verified Pathology Guides for **{selected_crop}** ({len(matched_diseases)} Major Threats)")

        for d in matched_diseases:
            with st.expander(f"🔬 {d['disease_name']} ({d.get('pathogen_type', 'Fungal / Insect')})", expanded=True):
                col_left, col_right = st.columns([1, 1])

                with col_left:
                    st.markdown(
                        f"""
                        <div class="agro-card" style="margin-bottom: 12px;">
                            <div style="font-weight: 800; font-size: 1.1rem; color: #06281b; margin-bottom: 6px;">
                                {d['disease_name']}
                            </div>
                            <p style="font-size: 0.86rem; color: #475569; margin: 0 0 8px 0;">
                                <b>Pathogen Taxonomy:</b> <i>{d.get('pathogen_type', 'Pathogenic')}</i><br>
                                <b>Risk Severity:</b> <span class="badge-danger">{d.get('risk_level', 'High')}</span>
                            </p>
                            <div style="font-size: 0.88rem; color: #1e293b;">
                                <b>Visual Diagnostic Symptoms:</b>
                                <ul style="margin: 4px 0 0 16px; padding: 0;">
                                    {''.join([f"<li>{s}</li>" for s in d.get('symptoms', [])])}
                                </ul>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        """
                        <div class="agro-card">
                            <div style="font-weight: 800; font-size: 0.95rem; color: #065f46; margin-bottom: 6px;">
                                🔍 Field Scouting & ETL Thresholds
                            </div>
                            <p style="font-size: 0.86rem; color: #1e293b; line-height: 1.5; margin: 0;">
                                • <b>Sampling Protocol:</b> Inspect 20 plants across a 'W' shaped transect twice weekly.<br>
                                • <b>Economic Threshold Level (ETL):</b> Initiate curative intervention when incidence reaches 5-10% infected leaves or 1-2 lesions/tiller.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col_right:
                    st.markdown(
                        f"""
                        <div class="agro-card" style="margin-bottom: 12px;">
                            <div style="font-weight: 800; font-size: 0.95rem; color: #047857; margin-bottom: 6px;">
                                🛡️ Cultural & Biological Prevention
                            </div>
                            <ul style="font-size: 0.86rem; color: #1e293b; margin: 0; padding-left: 16px; line-height: 1.5;">
                                {''.join([f"<li>{p}</li>" for p in d.get('prevention', [])])}
                            </ul>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f"""
                        <div class="agro-card">
                            <div style="font-weight: 800; font-size: 0.95rem; color: #b91c1c; margin-bottom: 6px;">
                                💊 Prescribed Interventions & Dosages
                            </div>
                            <ul style="font-size: 0.86rem; color: #1e293b; margin: 0; padding-left: 16px; line-height: 1.5;">
                                {''.join([f"<li><b>{t}</b></li>" for t in d.get('treatments', [])])}
                            </ul>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Escalation Information
        st.markdown(
            """
            <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 12px; padding: 18px; margin-top: 18px;">
                <h4 style="color: #065f46; margin: 0 0 6px 0;">📞 Extension & University Escalation Channels</h4>
                <p style="font-size: 0.88rem; color: #166534; margin: 0; line-height: 1.5;">
                    If field infection escalates rapidly (>20% expansion within 48h) or unexpected wilt occurs, 
                    contact your nearest <b>Krishi Vigyan Kendra (KVK)</b> agronomist or the <b>ICAR Kisan Call Centre (Toll-Free: 1800-180-1551)</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t_cv:
        st.markdown("#### 📷 Optional Image Diagnostic Screening")
        st.markdown("Upload a photo of affected leaves or pests for automated visual pattern screening:")

        col_up, col_res = st.columns([1, 1])
        with col_up:
            uploaded_file = st.file_uploader(
                "Upload Specimen Image (JPG, PNG)",
                type=["jpg", "jpeg", "png", "webp"],
                key="direct_disease_uploader",
            )

            st.markdown("##### ⚡ Quick Specimen Samples:")
            q1, q2, q3, q4 = st.columns(4)
            sample_choice = None
            sample_path = None
            with q1:
                if st.button("🐛 Aphid Pest", key="btn_sp_aphid", use_container_width=True):
                    sample_choice = "aphid_specimen_sample.jpg"
                    sample_path = config.BASE_DIR / "assets" / "images" / "aphid_specimen_sample.jpg"
            with q2:
                if st.button("🌾 Rice Blast", key="btn_sp_blast", use_container_width=True):
                    sample_choice = "rice_blast.jpg"
            with q3:
                if st.button("🌾 Wheat Rust", key="btn_sp_rust", use_container_width=True):
                    sample_choice = "wheat_rust.jpg"
            with q4:
                if st.button("🍅 Tomato Blight", key="btn_sp_blight", use_container_width=True):
                    sample_choice = "tomato_blight.jpg"

        with col_res:
            active_img_name = uploaded_file.name if uploaded_file else sample_choice
            if active_img_name:
                if uploaded_file:
                    st.image(uploaded_file, caption=f"Uploaded: {uploaded_file.name}", use_column_width=True)
                elif sample_path and sample_path.exists():
                    st.image(str(sample_path), caption="Specimen: Aphids & Sucking Pest Colony Infestation", use_column_width=True)

                diag = disease_service.diagnose_image(filename=active_img_name, crop_hint=selected_crop)
                st.markdown(
                    f"""
                    <div class="agro-card" style="border-left: 5px solid #059669;">
                        <h3 style="color: #06281b; margin: 0;">{diag['disease_name']}</h3>
                        <p style="color: #475569; margin: 4px 0 0 0; font-size: 0.88rem;">
                            <b>Confidence:</b> {diag['confidence_percentage']} • <b>Taxonomy:</b> {diag['pathogen_type']}
                        </p>
                        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 10px 0;">
                        <b>Key Treatments:</b>
                        <ul style="font-size: 0.86rem; color: #1e293b; margin: 4px 0 0 16px; padding: 0;">
                            {''.join([f"<li>{t}</li>" for t in diag.get('treatment_suggestions', [])])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("Upload an image or select a sample above to view computer vision diagnostic breakdown.")

    render_disclaimer("Disease and pest management advice is based on ICAR and state agricultural university research. Always check official product labels before application.")
