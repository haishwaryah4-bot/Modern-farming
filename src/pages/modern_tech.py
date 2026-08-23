"""
Page 8: Modern Farming Technology Explorer & AgriTech Intelligence.
Visual directory with real photographic illustrations covering:
1. 15 Modern Agritech Systems (Drones, Drip, Solar Pumps, Hydroponics, Vertical Farming, IoT, NDVI, Polyhouses)
2. Engineering Specifications, Operating Requirements & Maintenance Protocols
3. Government Subsidy Schemes (PMKSY, PM-KUSUM, SMAM, MIDH, NHB)
4. Comparative Economic Payback & ROI Benchmarks from the 100-Page Farming Dataset
"""

import base64
from pathlib import Path
import streamlit as st
from src.components.ui_elements import render_header, render_stat_card, render_disclaimer
import config


TECH_CATALOG = {
    "Precision Farming & Connected Smart Tractors": {
        "icon": "🚜",
        "image_file": "precision_iot_farming.jpg",
        "category": "Precision & Telematics",
        "description": "RTK-GPS auto-steered tractors with ISO-BUS telematics, variable rate seeding, and section-controlled fertilizer application.",
        "benefits": [
            "Eliminates overlap passes, reducing diesel fuel consumption by 15-20%",
            "Precision seed placement with millimeter accuracy",
            "Real-time engine telemetry, fuel monitoring, and acreage logging"
        ],
        "requirements": "RTK-GPS base station or 4G NTRIP subscription; ISO-BUS compatible implements.",
        "maintenance": "Quarterly GPS antenna firmware updates; hydraulic calibration; dust filter blowing.",
        "risks": "Satellite signal attenuation under dense tree cover; high initial capital.",
        "indicative_cost_per_acre": "₹7.5 - ₹12 Lakhs (Tractor + Auto-Steer Guidance kit)",
        "subsidy": "Up to 40-50% subsidy under Sub-Mission on Agricultural Mechanization (SMAM)",
        "approx_payback": "2.5 - 3.5 Years",
        "page_citation": "Source: Farming Dataset, Page 20 - Precision Farm Guidance & GPS Telematics"
    },
    "Agricultural Spraying & Multispectral Drones (UAV)": {
        "icon": "🛸",
        "image_file": "drone_spraying.jpg",
        "category": "Aerial Precision",
        "description": "DGCA-certified agricultural hexacopter drones for ultra-low volume foliar spraying and multispectral NDVI health mapping.",
        "benefits": [
            "Sprays 1 acre in 6-8 minutes with 90% water reduction (10 L/acre vs 150 L manual)",
            "Rotor downwash turbulence coats both upper and lower leaf surfaces",
            "Eliminates toxic human applicator chemical exposure"
        ],
        "requirements": "DGCA Remote Pilot Certificate (RPC), unobstructed airspace, portable battery generator.",
        "maintenance": "Propeller inspection, nozzle decalcification, LiPo battery charge-balancing.",
        "risks": "Spray drift during high wind (>15 km/h); battery overheating in extreme heat (42°C+).",
        "indicative_cost_per_acre": "Rental rate: ₹450 - ₹650 / Acre (Equipment cost ₹5.5 - ₹8 Lakhs)",
        "subsidy": "Up to 40-50% subsidy under SMAM; up to 100% for ICAR/KVK institutes",
        "approx_payback": "1.5 - 2 Years for Custom Hiring Center (CHC)",
        "page_citation": "Source: Farming Dataset, Page 25 - Agricultural Drones (UAVs)"
    },
    "Drip Irrigation & Automated Fertigation": {
        "icon": "💧",
        "image_file": "drip_irrigation.jpg",
        "category": "Water & Nutrient Precision",
        "description": "Pressure-compensating inline drippers delivering 100% water-soluble fertilizers directly to the active root zone.",
        "benefits": [
            "40-60% water savings over conventional flood irrigation",
            "20-35% higher crop yield and uniform canopy development",
            "Increases Fertilizer Use Efficiency (NUE) from 35% to 75%",
            "Suppresses inter-row weed germination by 50%"
        ],
        "requirements": "Assured filtration (Screen/Disc/Media filters), 1.5 bar operating pump, fertigation venturi injector.",
        "maintenance": "Weekly lateral line flushing; seasonal acid treatment (HCl pH 4.0) to dissolve carbonate scale.",
        "risks": "Emitter clogging from poor filtration or mixing Calcium with Phosphates/Sulfates.",
        "indicative_cost_per_acre": "₹45,000 - ₹65,000 / Acre (Gross)",
        "subsidy": "Up to 55% capital subsidy for small/marginal farmers under PMKSY (Per Drop More Crop)",
        "approx_payback": "1 - 1.5 Cropping Seasons",
        "page_citation": "Source: Farming Dataset, Page 21 & 22 - Drip Irrigation & Automated Fertigation"
    },
    "Hydroponic NFT & Substrate Cultivation": {
        "icon": "🥬",
        "image_file": "hydroponics.jpg",
        "category": "Soilless Agriculture",
        "description": "Nutrient Film Technique (NFT) and Dutch bucket recirculating soilless systems for high-value leafy greens, strawberries, and herbs.",
        "benefits": [
            "90-95% water conservation via closed-loop nutrient recirculation",
            "Zero soil-borne nematodes, fungal root rots, or weed competition",
            "30-40% faster crop turnaround cycles with year-round production"
        ],
        "requirements": "Automated EC/pH dosing controllers, RO water supply, continuous aeration pumps.",
        "maintenance": "Weekly nutrient reservoir dump & recalibration; UV/Ozone sterilization.",
        "risks": "Rapid crop wilt if water circulation pumps fail during hot midday hours.",
        "indicative_cost_per_acre": "₹25 - ₹40 Lakhs per Acre (Commercial Greenhouse NFT)",
        "subsidy": "Up to 50% credit-linked subsidy under Mission for Integrated Development of Horticulture (MIDH)",
        "approx_payback": "2.5 - 3.5 Years",
        "page_citation": "Source: Farming Dataset, Page 26 - Hydroponics & Protected Horticulture"
    },
    "Vertical Indoor Farming & Controlled Environments": {
        "icon": "🏢",
        "image_file": "vertical_farming.jpg",
        "category": "Indoor CEA",
        "description": "Multi-tier vertical racking with customized spectrum LED grow lights, automated HVAC climate control, and CO2 enrichment.",
        "benefits": [
            "10-20x higher productivity per square meter of footprint",
            "100% pesticide-free pristine organic produce",
            "Completely insulated from droughts, floods, and unseasonal weather"
        ],
        "requirements": "Three-phase electrical grid connection, HVAC chillers, HEPA air filtration.",
        "maintenance": "LED array heat sink cleaning; environmental sensor recalibration.",
        "risks": "High electricity operational costs; cooling load in tropical summer months.",
        "indicative_cost_per_acre": "₹50 - ₹90 Lakhs (High-density indoor facility)",
        "subsidy": "State AgriTech innovation grants and venture debt co-funding",
        "approx_payback": "3.5 - 4.5 Years",
        "page_citation": "Source: Farming Dataset, Page 27 - Controlled Environment Agriculture (CEA)"
    },
    "Farm Mechanization & Advanced Tractors": {
        "icon": "🚜",
        "image_file": "farm_tractor_mechanization.jpg",
        "category": "Farm Machinery",
        "description": "Heavy-duty 4WD agricultural tractors equipped with pneumatic seeders, laser levelers, and hydraulic tipping trailers.",
        "benefits": [
            "Completes deep tillage and seedbed preparation in hours instead of days",
            "Laser land leveling saves 20-25% irrigation water by ensuring uniform field grade",
            "Reduces labor bottlenecks during tight harvesting and planting windows"
        ],
        "requirements": "Adequate implement horsepower matching; diesel fuel storage; trained operators.",
        "maintenance": "Greasing universal joints every 50 operating hours; engine oil change at 250h.",
        "risks": "Soil compaction from heavy axle loads when operating on wet soils.",
        "indicative_cost_per_acre": "₹6.5 - ₹11 Lakhs (50 HP to 75 HP 4WD Tractors)",
        "subsidy": "40-50% subsidy under Sub-Mission on Agricultural Mechanization (SMAM)",
        "approx_payback": "2 - 3 Years (Custom Hiring / Commercial)",
        "page_citation": "Source: Farming Dataset, Page 19 - Farm Power & Mechanization Standards"
    },
    "On-Farm Automated Weather Station (AWS)": {
        "icon": "⛅",
        "image_file": "iot_weather_station.jpg",
        "category": "Microclimate Intelligence",
        "description": "Solar-powered telemetry sensor mast measuring wind speed, solar radiation, rainfall, relative humidity, and leaf wetness.",
        "benefits": [
            "Computes real-time Reference Evapotranspiration (ET0) using FAO-56 Penman-Monteith",
            "Predicts fungal disease outbreaks (Late Blight, Blast, Rust) 48-72 hours in advance",
            "Issues localized frost and heatwave emergency advisories"
        ],
        "requirements": "Open unobstructed field installation (minimum 4x distance from trees/buildings).",
        "maintenance": "Monthly solar panel wipe; rain gauge funnel cleaning; sensor recalibration.",
        "risks": "Lightning strikes (requires grounding rod); bird fouling on sensors.",
        "indicative_cost_per_acre": "₹35,000 - ₹75,000 per AWS unit",
        "subsidy": "Up to 50% subsidy under Mission for Integrated Development of Horticulture (MIDH)",
        "approx_payback": "1.5 - 2 Years",
        "page_citation": "Source: Farming Dataset, Page 24 - On-Farm Automated Weather Stations"
    },
    "Soil Health, Organic Humus & Compost Management": {
        "icon": "🌱",
        "image_file": "soil_health_compost.jpg",
        "category": "Soil Regeneration",
        "description": "Microbial composting, vermiculture, and biochar amendment protocols to boost Soil Organic Carbon (SOC) above 0.75%.",
        "benefits": [
            "Increases soil water holding capacity by up to 20,000 gallons per acre for every 1% SOC gain",
            "Improves microbial biomass carbon and mycorrhizal nutrient exchange",
            "Buffers soil pH against extreme alkalinity and salinity"
        ],
        "requirements": "Farmyard manure (FYM), crop residues, microbial inoculants, composting sheds.",
        "maintenance": "Turning compost piles at 15-day intervals; moisture maintenance at 50-60%.",
        "risks": "Weed seed survival if composting temperature fails to reach 55-65°C.",
        "indicative_cost_per_acre": "₹3,500 - ₹6,000 / Acre per Season",
        "subsidy": "100% assistance under Paramparagat Krishi Vikas Yojana (PKVY) for organic clusters",
        "approx_payback": "Immediate (Reduced chemical fertilizer bill)",
        "page_citation": "Source: Farming Dataset, Page 12 - Soil Organic Carbon & Microbiome Protocols"
    },
    "High-Yield Fresh Organic Vegetable Production": {
        "icon": "🧺",
        "image_file": "vegetable_harvest_basket.jpg",
        "category": "Horticulture Excellence",
        "description": "Intensive multi-layer vegetable cultivation integrating drip fertigation, silver-black plastic mulching, and biological IPM.",
        "benefits": [
            "3-4x higher net profit margins compared to traditional cereal mono-cropping",
            "Continuous weekly cash flow from staggered harvesting schedules",
            "Meets premium export and direct-to-consumer supermarket quality standards"
        ],
        "requirements": "Certified F1 hybrid seeds, micro-irrigation, trellising support for vines.",
        "maintenance": "Regular pruning of suckers; timely harvesting during early cool morning hours.",
        "risks": "Perishable commodity price volatility in local Mandis during peak arrivals.",
        "indicative_cost_per_acre": "₹35,000 - ₹60,000 / Acre per Crop",
        "subsidy": "Assistance under National Horticulture Mission (NHM) for vegetable seed and mulching",
        "approx_payback": "1 Season (3-4 Months)",
        "page_citation": "Source: Farming Dataset, Page 16 - Commercial Vegetable Production Systems"
    },
    "Aquaponics & Closed-Loop Fish-Plant Symbiosis": {
        "icon": "🐟",
        "image_file": "aquaponics_system.jpg",
        "category": "Integrated Aquaculture",
        "description": "Recirculating aquaculture system (RAS) where fish waste (ammonia) is converted into nitrate by nitrifying bacteria to fertilize plants.",
        "benefits": [
            "Dual revenue streams from fresh fish (Tilapia/Carp) and high-value leafy vegetables",
            "Zero synthetic chemical fertilizers required; 95% water recirculation",
            "Organic, premium chemical-free culinary product certification"
        ],
        "requirements": "Fish rearing tanks, mechanical swirl filters, biological biofilters, aeration blowers.",
        "maintenance": "Daily dissolved oxygen (DO) and ammonia testing; mechanical sludge flushing.",
        "risks": "Fish mortality if aeration power fails; biofilter crash from temperature shock.",
        "indicative_cost_per_acre": "₹8 - ₹16 Lakhs for 500 sq.m commercial setup",
        "subsidy": "Up to 40-60% subsidy under Pradhan Mantri Matsya Sampada Yojana (PMMSY)",
        "approx_payback": "2.5 - 3.5 Years",
        "page_citation": "Source: Farming Dataset, Page 31 - Integrated Aquaponics & Closed-Loop Systems"
    },
    "Climate-Controlled Polyhouses & Greenhouses": {
        "icon": "🏡",
        "image_file": "greenhouse_polyhouse.jpg",
        "category": "Protected Cultivation",
        "description": "Naturally ventilated or fan-pad cooled polyhouses for high-value horticulture, cherry tomato, capsicum, and cucumber.",
        "benefits": [
            "4-6x higher productivity per unit area with 90% A-grade export quality",
            "Year-round cultivation shielded from unseasonal rain, hail, and viral pests",
            "Enables precise microclimate humidity and temperature regulation"
        ],
        "requirements": "GI structural frame, 200-micron UV-stabilized poly film, drip fertigation, high capital.",
        "maintenance": "Polyfilm replacement every 4-5 years; fogger nozzle decalcification.",
        "risks": "High initial capital expenditure; power failure in fan-pad systems.",
        "indicative_cost_per_acre": "₹9.5 - ₹12.5 Lakhs per 1000 sq.m (0.25 Acre)",
        "subsidy": "50% capital subsidy under National Horticulture Board (NHB) & State Horticulture Missions",
        "approx_payback": "2.5 - 3 Years",
        "page_citation": "Source: Farming Dataset, Page 28 - Protected Cultivation & Polyhouses"
    },
    "NDVI Satellite & Aerial Multispectral Health Mapping": {
        "icon": "🗺️",
        "image_file": "ndvi_satellite_mapping.jpg",
        "category": "Satellite Telemetry",
        "description": "Sentinel-2 and PlanetScope multispectral vegetation indices (NDVI, NDRE, EVI) providing 5-day crop canopy health zonation.",
        "benefits": [
            "Identifies nutrient deficiency and disease foci 7-10 days before visible to human eye",
            "Generates Variable Rate Application (VRA) fertilizer prescription maps",
            "Monitors regional farm vegetation index history across multi-year cycles"
        ],
        "requirements": "Internet connectivity; field geo-boundary polygon mapping (KML/GeoJSON).",
        "maintenance": "Automated cloud-masking algorithms; ground-truth validation samples.",
        "risks": "Cloud cover obscuring optical satellite imagery during peak monsoon months.",
        "indicative_cost_per_acre": "₹25 - ₹50 / Acre / Season (Satellite SaaS analytics)",
        "subsidy": "Free access via national portal and state agriculture spatial platforms",
        "approx_payback": "Immediate (Targeted spot fertilization savings)",
        "page_citation": "Source: Farming Dataset, Page 30 - Remote Sensing & Satellite NDVI Zonation"
    },
    "Conservation Tillage, Crop Residue Mulching & Seedling Emergence": {
        "icon": "🌾",
        "image_file": "mulching_conservation_tillage.jpg",
        "category": "Conservation Ag",
        "description": "Zero-till Happy Seeder planting into standing crop stubble combined with surface organic residue mulching.",
        "benefits": [
            "Zero stubble burning; prevents atmospheric smog and particulate pollution",
            "Conserves 30-40% residual soil moisture from previous crop",
            "Cuts seedbed preparation tractor diesel costs by ₹1,500 - ₹2,200 per acre"
        ],
        "requirements": "50+ HP tractor, Happy Seeder / Super Seeder implement, uniform stubble spreader on combine.",
        "maintenance": "Flail blade sharpening; seeder boot alignment.",
        "risks": "Initial slug/rodent activity in thick straw mulch; requires proper seed depth adjustment.",
        "indicative_cost_per_acre": "Custom hiring: ₹1,400 - ₹1,800 / Acre (Implement cost ₹1.8 - ₹2.5 Lakhs)",
        "subsidy": "50% individual subsidy and 80% CHC subsidy under Crop Residue Management (CRM) scheme",
        "approx_payback": "1 Season",
        "page_citation": "Source: Farming Dataset, Page 14 - Conservation Agriculture & In-Situ Residue Management"
    },
    "Solar Agricultural Pumping Systems (PM-KUSUM)": {
        "icon": "☀️",
        "image_file": "solar_pump_kusum.jpg",
        "category": "Renewable Power",
        "description": "DC/AC solar photovoltaic pumping with Variable Frequency Drives (VFD) optimized for off-grid drip irrigation.",
        "benefits": [
            "Zero electricity bills and zero diesel fuel dependency",
            "Reliable daytime irrigation when crops actively transpire",
            "Grid net-metering option under PM-KUSUM Component C"
        ],
        "requirements": "Borewell / open well with adequate water recharge; shadow-free land for solar PV array.",
        "maintenance": "Weekly panel cleaning with water; inverter dust blowing.",
        "risks": "Theft of panels in isolated fields; ground water over-extraction without sensors.",
        "indicative_cost_per_acre": "₹1.8 - ₹2.8 Lakhs (3 HP to 7.5 HP standalone)",
        "subsidy": "Up to 60% capital subsidy (30% Central + 30% State) under PM-KUSUM Component B",
        "approx_payback": "2.5 - 3.5 Years",
        "page_citation": "Source: Farming Dataset, Page 29 - Solar Irrigation & PM-KUSUM Scheme"
    },
    "Digital Farm Management Software & Mobile AI Decision Support": {
        "icon": "📱",
        "image_file": "digital_farm_tablet.jpg",
        "category": "Digital Decision Support",
        "description": "Unified digital tablet and smartphone farm ERP integrating live telemetry, soil maps, mandi rates, and AI advisory.",
        "benefits": [
            "Real-time financial profit/loss accounting and input expenditure tracking",
            "Automated push alerts for spray schedules, weather events, and mandi price spikes",
            "Complete traceability log for organic and GAP export certification"
        ],
        "requirements": "Android / iOS smartphone or tablet, internet connection.",
        "maintenance": "Regular app updates; database backup synchronization.",
        "risks": "Data privacy concerns; rural digital literacy gaps.",
        "indicative_cost_per_acre": "Free to ₹100 / Acre / Year",
        "subsidy": "Provided free under Digital Agriculture Mission and AgriStack national initiatives",
        "approx_payback": "Immediate",
        "page_citation": "Source: Farming Dataset, Page 32 - Digital Agriculture, IoT & AgriStack"
    }
}


def _get_image_base64(filename: str) -> str:
    path = config.BASE_DIR / "assets" / "images" / filename
    if path.exists():
        with open(path, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""


def render_modern_tech_page():
    render_header(
        title="Modern Agricultural Technologies & AgriTech Intelligence",
        subtitle="Visual directory of 15 precision agriculture systems, engineering specifications, subsidies, and comparative ROI models",
        icon="🚀",
    )

    t_catalog, t_gallery, t_roi = st.tabs([
        "💡 Technology Specifications & Blueprints",
        "🖼️ Visual AgriTech Photo Gallery (15 Systems)",
        "📊 Government Subsidies & Financial ROI"
    ])

    with t_catalog:
        selected_tech = st.selectbox(
            "Select Modern Agricultural Technology to Inspect:",
            list(TECH_CATALOG.keys()),
            index=0,
            key="modern_tech_select",
        )

        tech = TECH_CATALOG[selected_tech]
        img_b64 = _get_image_base64(tech["image_file"])

        c_img, c_specs = st.columns([1.1, 1.9])
        with c_img:
            if img_b64:
                st.markdown(
                    f"""
                    <div style="border: 2.5px solid #059669; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 28px rgba(0,20,10,0.35); margin-bottom: 12px;">
                        <img src="{img_b64}" style="width: 100%; height: 260px; object-fit: cover; display: block;" alt="{selected_tech}">
                        <div style="background: #ffffff; padding: 10px 14px; border-top: 1.5px solid #059669;">
                            <div style="font-weight: 800; color: #031c0e; font-size: 0.95rem;">{tech['icon']} {selected_tech}</div>
                            <div style="font-size: 0.8rem; color: #059669; font-weight: 700;">{tech['category']}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with c_specs:
            c1, c2, c3 = st.columns(3)
            with c1:
                render_stat_card("Indicative Investment", tech["indicative_cost_per_acre"], "Gross equipment cost", icon="💰")
            with c2:
                render_stat_card("Govt Subsidy Support", "Up to 50-60%", tech["subsidy"][:32] + "...", icon="🏛️")
            with c3:
                render_stat_card("Estimated Payback", tech["approx_payback"], "Based on yield boost & savings", icon="⏱️")

        st.markdown(
            f"""
            <div class="agro-card" style="margin-top: 10px;">
                <h3 style="color: #031c0e; margin-top: 0;">{tech['icon']} {selected_tech}</h3>
                <p style="font-size: 1rem; color: #1e293b; font-weight: 600;">{tech['description']}</p>
                <hr style="border: none; border-top: 1.5px solid #e2e8f0; margin: 12px 0;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div>
                        <h4 style="color: #047857; margin-bottom: 6px; font-weight: 800;">✨ Core Agronomic Benefits:</h4>
                        <ul style="color: #1e293b; padding-left: 18px; line-height: 1.55; font-weight: 600;">{''.join([f'<li>{b}</li>' for b in tech['benefits']])}</ul>
                        <h4 style="color: #0284c7; margin-bottom: 6px; font-weight: 800;">⚙️ Infrastructure Requirements:</h4>
                        <p style="font-size: 0.88rem; color: #334155; font-weight: 600;">{tech['requirements']}</p>
                    </div>
                    <div>
                        <h4 style="color: #d97706; margin-bottom: 6px; font-weight: 800;">🛠️ Maintenance Protocols:</h4>
                        <p style="font-size: 0.88rem; color: #334155; font-weight: 600;">{tech['maintenance']}</p>
                        <h4 style="color: #dc2626; margin-bottom: 6px; font-weight: 800;">⚠️ Key Risks & Mitigation:</h4>
                        <p style="font-size: 0.88rem; color: #334155; font-weight: 600;">{tech['risks']}</p>
                    </div>
                </div>
                <div class="citation-badge" style="margin-top: 14px;">
                    📄 {tech['page_citation']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t_gallery:
        st.markdown("#### 🖼️ 15 Modern AgriTech Visual Blueprints & Field Implementations")
        st.markdown("Click any technology below to inspect its detailed specifications, engineering requirements, and subsidies:")

        tech_list = list(TECH_CATALOG.items())
        # Display in a 3-column grid (5 rows x 3 cols = 15 systems)
        for row_idx in range(0, len(tech_list), 3):
            cols = st.columns(3)
            for col_idx in range(3):
                item_idx = row_idx + col_idx
                if item_idx < len(tech_list):
                    t_name, t_data = tech_list[item_idx]
                    t_img_b64 = _get_image_base64(t_data["image_file"])
                    with cols[col_idx]:
                        st.markdown(
                            f"""
                            <div style="background: #ffffff; border: 2px solid #059669; border-radius: 14px; overflow: hidden; box-shadow: 0 6px 18px rgba(0,0,0,0.15); margin-bottom: 16px;">
                                <img src="{t_img_b64}" style="width: 100%; height: 180px; object-fit: cover; display: block;" alt="{t_name}">
                                <div style="padding: 12px 14px;">
                                    <div style="font-weight: 800; color: #031c0e; font-size: 0.94rem; margin-bottom: 4px;">{t_data['icon']} {t_name}</div>
                                    <div style="font-size: 0.8rem; color: #059669; font-weight: 700; margin-bottom: 6px;">{t_data['category']}</div>
                                    <div style="font-size: 0.82rem; color: #475569; line-height: 1.4; font-weight: 500;">{t_data['description'][:95]}...</div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

    with t_roi:
        st.markdown("#### 📊 Comparative Economic Payback & Subsidy Framework (Verified Agronomic Models)")
        
        st.markdown(
            """
            <div class="agro-card" style="margin-bottom: 14px;">
                <h4 style="color: #031c0e; margin: 0 0 8px 0; font-weight: 800;">🏛️ Key National AgriTech Subsidy Programs:</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.88rem; color: #1e293b;">
                    <div style="background: #f0fdf4; padding: 14px; border-radius: 10px; border: 1.5px solid #059669;">
                        <b style="color: #047857;">1. PMKSY (Per Drop More Crop):</b><br>
                        55% capital subsidy for Small/Marginal farmers, 45% for Other farmers for Inline Drip and Micro-Sprinklers.
                    </div>
                    <div style="background: #f0fdf4; padding: 14px; border-radius: 10px; border: 1.5px solid #059669;">
                        <b style="color: #047857;">2. PM-KUSUM (Component B & C):</b><br>
                        60% capital subsidy (30% Central + 30% State) for 3 HP to 7.5 HP standalone solar agricultural pumps.
                    </div>
                    <div style="background: #f0fdf4; padding: 14px; border-radius: 10px; border: 1.5px solid #059669;">
                        <b style="color: #047857;">3. SMAM (Sub-Mission on Agri Mechanization):</b><br>
                        40-50% subsidy on precision drone sprayers, laser land levelers, and automated seed drills.
                    </div>
                    <div style="background: #f0fdf4; padding: 14px; border-radius: 10px; border: 1.5px solid #059669;">
                        <b style="color: #047857;">4. National Horticulture Board (NHB):</b><br>
                        50% credit-linked capital subsidy for naturally ventilated polyhouses and high-tech greenhouses.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### 📈 Standard Financial Return & Payback Benchmarks:")
        st.markdown(
            """
            <div class="agro-card">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem; color: #1e293b; font-weight: 600;">
                    <thead>
                        <tr style="border-bottom: 2px solid #cbd5e1; text-align: left; color: #031c0e; font-weight: 800;">
                            <th style="padding: 10px;">Technology</th>
                            <th style="padding: 10px;">Gross Capital Cost</th>
                            <th style="padding: 10px;">Govt Subsidy</th>
                            <th style="padding: 10px;">Annual Economic Gain</th>
                            <th style="padding: 10px;">Payback Period</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 10px;"><b>💧 Inline Drip (1 Acre)</b></td>
                            <td style="padding: 10px;">₹55,000</td>
                            <td style="padding: 10px; color: #059669; font-weight: 800;">55% (₹30,250)</td>
                            <td style="padding: 10px;">₹22,000 (Water & yield)</td>
                            <td style="padding: 10px; color: #047857; font-weight: 800;">1.1 Seasons</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 10px;"><b>☀️ Solar Pump 5 HP (PM-KUSUM)</b></td>
                            <td style="padding: 10px;">₹2,40,000</td>
                            <td style="padding: 10px; color: #059669; font-weight: 800;">60% (₹1,44,000)</td>
                            <td style="padding: 10px;">₹45,000 (Diesel savings)</td>
                            <td style="padding: 10px; color: #047857; font-weight: 800;">2.1 Years</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 10px;"><b>📡 IoT Soil Moisture Probes</b></td>
                            <td style="padding: 10px;">₹25,000</td>
                            <td style="padding: 10px; color: #059669; font-weight: 800;">40% (₹10,000)</td>
                            <td style="padding: 10px;">₹12,000 (Pumping power)</td>
                            <td style="padding: 10px; color: #047857; font-weight: 800;">1.2 Years</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 10px;"><b>🛸 Agricultural Spray Drone</b></td>
                            <td style="padding: 10px;">₹6,50,000</td>
                            <td style="padding: 10px; color: #059669; font-weight: 800;">50% (₹3,25,000)</td>
                            <td style="padding: 10px;">₹1,80,000 (Custom spraying)</td>
                            <td style="padding: 10px; color: #047857; font-weight: 800;">1.8 Years</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;"><b>🏡 Polyhouse 1000 sq.m (NHB)</b></td>
                            <td style="padding: 10px;">₹11,00,000</td>
                            <td style="padding: 10px; color: #059669; font-weight: 800;">50% (₹5,50,000)</td>
                            <td style="padding: 10px;">₹2,20,000 (Horticulture)</td>
                            <td style="padding: 10px; color: #047857; font-weight: 800;">2.5 Years</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_disclaimer()
