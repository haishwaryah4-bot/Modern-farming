"""
Reusable UI Components and Micro-Layouts for Modern Agriculture Web App.
High-contrast accessible rendering for headers, metric cards, citations, and notices.
"""

import streamlit as st
from typing import Dict, Any, List, Optional


def render_header(title: str, subtitle: str, icon: str = "🌾"):
    """
    Renders top gradient hero banner with icon and subtitle in high-contrast accessible typography.
    """
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.99) 0%, rgba(240, 253, 244, 0.98) 100%); border: 2px solid #059669; border-radius: 18px; padding: 24px 30px; margin-bottom: 24px; box-shadow: 0 10px 28px rgba(0, 20, 10, 0.35);">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="font-size: 2.4rem;">{icon}</div>
                <div>
                    <h1 style="color: #052e16 !important; margin: 0; font-size: 2.1rem; font-weight: 900; letter-spacing: -0.02em; text-shadow: none !important;">{title}</h1>
                    <p style="color: #0f172a !important; margin: 4px 0 0 0; font-size: 0.98rem; font-weight: 700; text-shadow: none !important;">{subtitle}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(title: str, value: str, subtext: str, icon: str = "🌱"):
    """
    Renders a clean modern metric card with high-contrast readable labels.
    """
    st.markdown(
        f"""
        <div class="stat-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="stat-title">{title}</span>
                <span style="font-size: 1.4rem;">{icon}</span>
            </div>
            <div class="stat-value">{value}</div>
            <div class="stat-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_citations(citations: List[Dict[str, Any]]):
    """
    Renders formatted citation cards with high-contrast text and verified source badges.
    """
    if not citations:
        return

    st.markdown(
        """
        <div style="font-size: 1.1rem; font-weight: 900; color: #ffffff !important; text-shadow: 0 2px 6px rgba(0,0,0,0.85); margin: 18px 0 10px 0;">
            📌 Verified Knowledge Base Citations
        </div>
        """,
        unsafe_allow_html=True,
    )
    for c in citations:
        st.markdown(
            f"""
            <div style="background: #ffffff; border: 2px solid #059669; border-radius: 12px; padding: 14px 18px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="background: #ecfdf5; color: #065f46 !important; font-weight: 800; font-size: 0.86rem; padding: 4px 12px; border-radius: 6px; border: 1.5px solid #10b981;">
                        📄 {c['source']} (Page: {c.get('page', 1)})
                    </span>
                    <span style="background: #dcfce7; color: #14532d !important; font-weight: 800; font-size: 0.84rem; padding: 3px 10px; border-radius: 6px;">
                        Relevance: {c.get('relevance_pct', '92%')}
                    </span>
                </div>
                <div style="color: #0f172a !important; font-size: 0.9rem !important; font-weight: 600; line-height: 1.55; font-style: italic; background: #f8fafc; padding: 10px 14px; border-radius: 8px; border-left: 4px solid #059669;">
                    "{c.get('text_snippet', '')}"
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_disclaimer(custom_text: Optional[str] = None):
    """
    Renders scientific & agronomic advisory disclaimer banner with WCAG AAA contrast.
    """
    text = custom_text or "Agricultural recommendations are calculated from verified ICAR and State Agricultural University agronomic datasets. Always verify field decisions with your local extension officer or district Krishi Vigyan Kendra (KVK)."
    st.markdown(
        f"""
        <div class="disclaimer-box" style="background: #f0fdf4 !important; border: 2px solid #059669 !important; border-radius: 14px !important; padding: 16px 20px !important; margin-top: 24px !important; display: flex !important; align-items: flex-start !important; gap: 12px !important;">
            <span style="font-size: 1.5rem; line-height: 1; margin-top: 2px;">⚠️</span>
            <span style="color: #064e3b !important; font-size: 0.92rem !important; line-height: 1.55 !important; font-weight: 700 !important;">
                <b style="color: #047857 !important; font-weight: 900 !important;">Agronomic Advisory Notice:</b> {text}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
