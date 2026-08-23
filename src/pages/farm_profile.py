"""
Page: National Agricultural Agro-Climatic Zones & Cropping Systems Directory.
Pure informational guide covering India's 15 Agro-Climatic Zones, cropping calendars,
and key crop recommendations.
"""

import streamlit as st
from src.components.ui_elements import render_header, render_disclaimer
import config


def render_farm_profile_page():
    render_header(
        title="National Agro-Climatic Zones & Cropping Systems Directory",
        subtitle="Overview of India's 15 major planning zones, agro-ecological characteristics, and predominant crop sequences",
        icon="🗺️",
    )

    st.markdown(
        """
        <div class="agro-card" style="margin-bottom: 20px;">
            <h3 style="color: #06281b; margin-top: 0;">🌾 India's Major Agro-Climatic Planning Regions (Planning Commission / ICAR)</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 0.88rem; color: #1e293b;">
                <div style="background: #f8fafc; padding: 14px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <b>1. Western Himalayan Region:</b> J&K, HP, Uttarakhand (Apples, Walnuts, Saffron, Off-season Vegetables).<br><br>
                    <b>2. Eastern Himalayan Region:</b> Assam, NE States, Sub-Himalayan Bengal (Tea, Rice, Jute, Citrus).<br><br>
                    <b>3. Lower Gangetic Plain:</b> West Bengal (Rice-Jute, Rice-Potato, Mustard).<br><br>
                    <b>4. Middle Gangetic Plain:</b> UP, Bihar (Rice-Wheat, Maize, Sugarcane, Pulses).
                </div>
                <div style="background: #f8fafc; padding: 14px; border-radius: 8px; border: 1px solid #e2e8f0;">
                    <b>5. Upper Gangetic Plain:</b> Western UP (Wheat, Rice, Sugarcane, Mustard).<br><br>
                    <b>6. Trans-Gangetic Plain:</b> Punjab, Haryana, Rajasthan (Rice-Wheat, Cotton-Wheat, Mustard).<br><br>
                    <b>7. Central Plateau & Hills:</b> MP, Rajasthan, UP (Soybean, Chickpea, Wheat, Mustard).<br><br>
                    <b>8. Western Dry Region:</b> Western Rajasthan (Bajra, Moth Bean, Cluster Bean, Cumin).
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_disclaimer()
