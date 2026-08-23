"""
Global configuration for AgriSense AI - Smart Farming Advisory Platform.
Loads environment variables and establishes application-wide constants.
Provides resilient type parsing so empty/whitespace environment variables on Vercel never cause ValueError.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# Helper functions to safely parse environment variables with robust fallbacks
def _get_env_int(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None or not str(val).strip():
        return default
    try:
        return int(str(val).strip())
    except (ValueError, TypeError):
        return default


def _get_env_float(key: str, default: float) -> float:
    val = os.getenv(key)
    if val is None or not str(val).strip():
        return default
    try:
        return float(str(val).strip())
    except (ValueError, TypeError):
        return default


def _get_env_str(key: str, default: str = "") -> str:
    val = os.getenv(key)
    if val is None or not str(val).strip():
        return default
    return str(val).strip()


# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_DOCS_DIR = DATA_DIR / "sample_docs"
ASSETS_DIR = BASE_DIR / "assets"

# On read-only serverless environments like Vercel, use /tmp for uploads
UPLOADS_DIR = BASE_DIR / "uploads"
try:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
except (OSError, PermissionError):
    UPLOADS_DIR = Path("/tmp/uploads")
    try:
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

# Ensure directories exist safely without throwing errors on read-only environments
for d in [DATA_DIR, SAMPLE_DOCS_DIR, ASSETS_DIR]:
    try:
        d.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError):
        pass

# LLM API configuration
OPENAI_API_KEY = _get_env_str("OPENAI_API_KEY", "")
OPENAI_MODEL = _get_env_str("OPENAI_MODEL", "gpt-4o-mini")
GROQ_API_KEY = _get_env_str("GROQ_API_KEY", "")
GROQ_MODEL = _get_env_str("GROQ_MODEL", "llama-3.1-70b-versatile")
OPENWEATHER_API_KEY = _get_env_str("OPENWEATHER_API_KEY", "")

# Project Branding
PROJECT_NAME = "AgriSense AI - Smart Farming Advisory Platform"
APP_SUBTITLE = "Source-Grounded Precision Agriculture & Knowledge-Driven Farm Copilot"

# Default India-Focused Farm Profile
DEFAULT_FARM_PROFILE = {
    "farmer_name": "Rajesh Sharma",
    "farm_name": "Surya Agro Farms",
    "state": "Punjab",
    "district": "Ludhiana",
    "location": "Ludhiana, Punjab",
    "farm_size_acres": 15.0,
    "selected_crop": "Rice (Paddy)",
    "crop_variety": "PR-126 / Pusa Basmati 1509",
    "season": "Kharif",
    "growth_stage": "Tillering / Branching",
    "soil_type": "Alluvial Clay Loam",
    "irrigation_method": "Alternate Wetting and Drying (AWD) + Tube well",
    "recent_weather": "Warm & Humid (31°C, 72% RH, Scattered Showers)",
    "pest_observations": "Minor leaf folding observed on 5% border tillers; no severe blast lesions.",
    "water_status": "Adequate canal supply + solar tube well backup",
    "soil_status": "Nitrogen deficient (210 kg/ha), Zinc deficient (0.48 ppm), pH 7.8",
}

# The 13 Core Crops from the Knowledge Base
SUPPORTED_CROPS = [
    "Rice (Paddy)",
    "Wheat",
    "Maize (Corn)",
    "Cotton",
    "Soybean",
    "Groundnut",
    "Pigeonpea (Arhar/Tur)",
    "Chickpea (Gram)",
    "Mustard",
    "Potato",
    "Tomato",
    "Chilli",
    "Brinjal",
]

# Growth Stages
GROWTH_STAGES = [
    "Land Preparation & Basal Sowing",
    "Seedling / Nursery Stage",
    "Vegetative Growth",
    "Tillering / Branching",
    "Flowering & Panicle Initiation",
    "Grain / Fruit Development",
    "Maturity & Pre-Harvest",
]

# Soil Types
SOIL_TYPES = [
    "Alluvial Soil",
    "Black (Vertisol) Soil",
    "Red & Yellow Soil",
    "Laterite Soil",
    "Sandy Loam",
    "Clay Loam",
    "Saline / Alkaline Soil",
]

# Cropping Seasons
SEASONS = [
    "Kharif (Monsoon / Autumn)",
    "Rabi (Winter / Spring)",
    "Zaid (Summer)",
    "Perennial",
]

# Indian States & Major Agricultural Districts
INDIAN_STATES_DISTRICTS = {
    "Punjab": ["Ludhiana", "Amritsar", "Bathinda", "Jalandhar", "Patiala", "Ferozepur"],
    "Haryana": ["Karnal", "Hisar", "Ambala", "Sirsa", "Kurukshetra", "Rohtak"],
    "Madhya Pradesh": ["Indore", "Ujjain", "Bhopal", "Jabalpur", "Hoshangabad", "Dewas"],
    "Maharashtra": ["Nashik", "Pune", "Nagpur", "Latur", "Aurangabad", "Kolhapur"],
    "Gujarat": ["Rajkot", "Junagadh", "Ahmedabad", "Surat", "Bhavnagar", "Mehsana"],
    "Uttar Pradesh": ["Varanasi", "Agra", "Meerut", "Lucknow", "Bareilly", "Gorakhpur"],
    "Rajasthan": ["Kota", "Bikaner", "Sri Ganganagar", "Jaipur", "Bharatpur", "Jodhpur"],
    "Andhra Pradesh": ["Guntur", "Krishna", "Kurnool", "West Godavari", "Chittoor"],
    "Telangana": ["Warangal", "Karimnagar", "Nizamabad", "Khammam", "Nalgonda"],
    "Karnataka": ["Belagavi", "Kolar", "Dharwad", "Mysuru", "Shivamogga", "Ballari"],
    "Tamil Nadu": ["Thanjavur", "Coimbatore", "Madurai", "Erode", "Tiruchirappalli"],
    "West Bengal": ["Burdwan", "Hooghly", "Murshidabad", "Nadia", "Bankura"],
}

# Modern Technologies
MODERN_TECHNOLOGIES = [
    "Drip Irrigation & Fertigation",
    "Soil Moisture Capacitance Probes (IoT)",
    "Automated On-Farm Weather Stations (AWS)",
    "Agricultural Spraying & Multispectral Drones (UAV)",
    "Satellite Remote Sensing & NDVI Mapping",
    "Computer Vision Disease & Weed Detection",
    "Climate-Controlled Polyhouses & Greenhouses",
    "Commercial Hydroponic Systems (NFT/Bato)",
    "Solar Agricultural Pumps (PM-KUSUM)",
    "Smart IoT Grain Silos & Cold Chain Storage",
]

# Vector & RAG Parameters (Robust fallbacks for empty Vercel environment variables)
RAG_CHUNK_SIZE = _get_env_int("RAG_CHUNK_SIZE", 600)
RAG_CHUNK_OVERLAP = _get_env_int("RAG_CHUNK_OVERLAP", 100)
RAG_TOP_K = _get_env_int("RAG_TOP_K", 4)
RAG_HYBRID_ALPHA = _get_env_float("RAG_HYBRID_ALPHA", 0.55)
