"""
Page 7: Market Insights & Commodity Intelligence Directory.
Pure informational guide covering:
1. Live commodity modal prices across 13 crops
2. Government Minimum Support Price (MSP) benchmarks and premium calculations
3. Historical price trajectory analysis
4. State & Mandi level quotation benchmarks
5. National Procurement Schemes & Price Support Policies (PM-AASHA / MSP)
"""

import streamlit as st
from src.components.ui_elements import render_header, render_stat_card, render_disclaimer
from src.services.market_service import market_service
import config


def render_market_insights_page():
    render_header(
        title="Agricultural Market Insights & Mandi Intelligence",
        subtitle="Live commodity modal prices, MSP benchmarks, mandi comparisons, and national procurement policies",
        icon="📈",
    )

    # Crop Selector
    c1, c2 = st.columns([1, 2])
    with c1:
        selected_crop = st.selectbox(
            "Select Agricultural Commodity:",
            ["Rice (Paddy)", "Wheat", "Cotton", "Tomato", "Potato", "Onion", "Soybean", "Mustard", "Chickpea (Gram)"],
            index=0,
            key="mkt_crop_select",
        )

    summary = market_service.get_crop_market_summary(selected_crop)

    # 3 Stat Cards Row
    k1, k2, k3 = st.columns(3)
    with k1:
        render_stat_card(
            title=f"Average Mandi Modal Price",
            value=f"₹{summary['modal_price']}",
            subtext=f"Range: ₹{summary['min_price']} - ₹{summary['max_price']} / Quintal",
            icon="💰",
        )
    with k2:
        diff = round(summary["modal_price"] - summary["msp"], 1)
        diff_str = f"+₹{diff}" if diff >= 0 else f"-₹{abs(diff)}"
        render_stat_card(
            title="Govt Minimum Support Price (MSP)",
            value=f"₹{summary['msp']}",
            subtext=f"Mandi Premium: {diff_str} / Quintal",
            icon="🏛️",
        )
    with k3:
        render_stat_card(
            title="Weekly Price Velocity",
            value=f"{summary['weekly_change_pct']}%",
            subtext=f"Market Outlook: {summary['trend']}",
            icon="📈" if "+" in str(summary['weekly_change_pct']) else "📉",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["📊 Historical 30-Day Trajectory", "🏬 Mandi Quotation Directory", "🏛️ MSP & National Procurement Policies"])

    with t1:
        st.markdown(f"#### 📈 30-Day Modal Price Trajectory: {selected_crop}")
        history = market_service.generate_price_history_series(selected_crop, days=30)

        dates = [h["date"] for h in history]
        prices = [h["modal_price"] for h in history]
        msps = [h["msp"] for h in history]

        st.markdown(
            f"""
            <div class="agro-card" style="margin-bottom: 12px;">
                <b>Latest Closing Modal Rate:</b> ₹{prices[-1]}/Qtl &nbsp;|&nbsp; 
                <b>30-Day Peak:</b> ₹{max(prices)}/Qtl &nbsp;|&nbsp; 
                <b>30-Day Floor:</b> ₹{min(prices)}/Qtl &nbsp;|&nbsp; 
                <b>Official MSP Benchmark:</b> ₹{msps[-1]}/Qtl
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Recent Price Trend Samples:")
        recent_cols = st.columns(5)
        for idx, col in enumerate(recent_cols):
            h_item = history[-(idx+1)]
            with col:
                st.markdown(
                    f"""
                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; text-align: center;">
                        <div style="font-size: 0.75rem; color: #64748b;">{h_item['date']}</div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #065f46;">₹{h_item['modal_price']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with t2:
        st.markdown(f"#### 🏬 State & Mandi Level Quotations for {selected_crop}")
        mandi_list = summary.get("mandis") or market_service.get_all_prices()
        for m in mandi_list:
            st.markdown(
                f"""
                <div class="agro-card" style="margin-bottom: 8px; padding: 14px 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <b>🏬 {m.get('mandi', 'Mandi')}, {m.get('state', 'State')}</b>
                            <div style="font-size: 0.8rem; color: #64748b;">Arrival Volume: {m.get('arrivals_qtl', 120)} Quintals</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.2rem; font-weight: 800; color: #065f46;">₹{m.get('modal_price', 2200)}/Qtl</div>
                            <div style="font-size: 0.76rem; color: #475569;">Min: ₹{m.get('min_price', 2100)} | Max: ₹{m.get('max_price', 2300)}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with t3:
        st.markdown("#### 🏛️ Minimum Support Price (MSP) & Government Procurement Mechanisms")
        st.markdown(
            """
            <div class="agro-card">
                <h4 style="color: #065f46; margin: 0 0 8px 0;">🌾 National Price Support Policies (CACP & PM-AASHA):</h4>
                <div style="font-size: 0.88rem; color: #1e293b; line-height: 1.6;">
                    • <b>Determination of MSP:</b> Recommended by the Commission for Agricultural Costs and Prices (CACP) at a minimum of 1.5 times the cost of production (A2+FL formula).<br>
                    • <b>PM-AASHA (Pradhan Mantri Annadata Aay Sanraksan Abhiyan):</b> Comprises the Price Support Scheme (PSS) for pulses & oilseeds, Price Deficiency Payment Scheme (PDPS), and Private Procurement Stockist Scheme (PPSS).<br>
                    • <b>Food Corporation of India (FCI) Operations:</b> Direct procurement of Paddy and Wheat at designated Mandis during Kharif and Rabi marketing seasons.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_disclaimer()
