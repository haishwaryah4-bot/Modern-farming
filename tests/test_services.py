"""
Tests for Domain Services: Weather, Market, Crop Advisory, Disease, and LLM.
"""

from src.services.weather_service import weather_service
from src.services.market_service import market_service
from src.services.crop_advisory_service import crop_advisory_service
from src.services.disease_service import disease_service
from src.services.soil_service import soil_service
from src.services.llm_service import llm_client


def test_weather_service():
    cw = weather_service.get_current_weather("Ludhiana, Punjab")
    assert 10 <= cw["temperature_c"] <= 50
    assert "icon" in cw

    fc = weather_service.get_7day_forecast("Ludhiana, Punjab")
    assert len(fc) == 7


def test_market_service():
    summary = market_service.get_crop_market_summary("Wheat")
    assert summary["modal_price"] > 0
    assert summary["min_price"] <= summary["max_price"]

    history = market_service.generate_price_history_series("Wheat", days=14)
    assert len(history) == 14


def test_crop_advisory_service():
    advisory = crop_advisory_service.get_advisory(
        crop="Rice (Paddy)",
        growth_stage="Tillering / Branching",
        soil_type="Alluvial Soil",
    )
    assert "irrigation_advice" in advisory
    assert "fertilizer_dosage" in advisory


def test_disease_service():
    assert len(disease_service.catalog) > 0
    assert len(disease_service.get_all_diseases()) > 0
    first = disease_service.catalog[0]
    assert "disease_name" in first
    assert "symptoms" in first
    assert "treatments" in first

    diag = disease_service.diagnose_image(filename="sample_leaf_blast.jpg", crop_hint="Rice (Paddy)")
    assert "disease_name" in diag
    assert diag["confidence_score"] > 0.8
    assert len(diag["treatment_suggestions"]) > 0


def test_soil_analysis_service():
    test_values = {"pH": 7.8, "EC": 0.42, "OC": 0.41, "N": 210.5, "P": 18.2, "K": 310.0, "Zn": 0.48}
    res = soil_service.analyze_soil(test_values)
    assert 0 <= res["soil_health_index"] <= 100
    assert len(res["parameters"]) == len(test_values)
    assert len(res["recommendations"]) > 0
