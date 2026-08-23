"""
Tests for AgriSense AI Agent, 8 Tool Invocations, and Multi-Step Execution Scenarios.
"""

from src.agents.tools import (
    TOOL_REGISTRY,
    tool_rag_knowledge_search,
    tool_farm_profile_analyzer,
    tool_crop_advisory_planner,
    tool_soil_report_analyzer,
    tool_irrigation_recommendation,
    tool_pest_disease_risk_assessment,
    tool_modern_technology_recommendation,
    tool_weather_market_placeholder,
)
from src.agents.agent_core import ai_agent


def test_agent_tools_registry():
    assert len(TOOL_REGISTRY) >= 8
    assert "rag_knowledge_search" in TOOL_REGISTRY
    assert "farm_profile_analyzer" in TOOL_REGISTRY
    assert "crop_advisory_planner" in TOOL_REGISTRY
    assert "soil_report_analyzer" in TOOL_REGISTRY
    assert "irrigation_recommendation" in TOOL_REGISTRY
    assert "pest_disease_risk_assessment" in TOOL_REGISTRY
    assert "modern_technology_recommendation" in TOOL_REGISTRY
    assert "weather_market_placeholder" in TOOL_REGISTRY


def test_tool_irrigation_recommendation():
    res = tool_irrigation_recommendation(crop="Rice (Paddy)", growth_stage="Tillering")
    assert res["method"] == "Alternate Wetting and Drying (AWD)"
    assert "daily_et0_mm" in res
    assert "citation" in res


def test_tool_pest_disease_risk_assessment():
    res = tool_pest_disease_risk_assessment(crop="Rice (Paddy)", symptoms="blast lesions on leaves", humidity_pct=80)
    assert res["risk_level"] == "High"
    assert len(res["curative_treatments"]) > 0


def test_tool_modern_technology_recommendation():
    res = tool_modern_technology_recommendation(crop="Tomato", farm_size_acres=4.0)
    assert len(res["recommended_technologies"]) >= 2
    assert "Drip" in res["recommended_technologies"][0]["tech"]


def test_scenario_rice_poor_drainage():
    query = "I am growing rice in Kharif season. My field has poor drainage and high humidity. Give me an action plan."
    res = ai_agent.plan_and_execute(query)
    assert len(res["plan_steps"]) >= 4
    assert len(res["tools_invoked"]) >= 2
    assert "answer" in res


def test_scenario_tomato_flowering():
    query = "Recommend an irrigation and fertigation approach for tomato at flowering stage."
    res = ai_agent.plan_and_execute(query)
    assert len(res["plan_steps"]) >= 4
    assert "answer" in res


def test_scenario_small_farm_tech():
    query = "Which modern technologies from the knowledge base are suitable for a small farm with limited water?"
    res = ai_agent.plan_and_execute(query)
    assert len(res["plan_steps"]) >= 3
    assert "modern_technology_recommendation" in res["tools_invoked"]
    assert "answer" in res


def test_image_retrieval_service():
    from src.services.image_retriever_service import image_retriever
    assert len(image_retriever.dataset) >= 15

    # Test 1: Hydroponic query
    imgs_hydro = image_retriever.search_images("What is hydroponic farming?", top_k=2)
    assert len(imgs_hydro) > 0
    assert any("hydroponic" in img["image"].lower() for img in imgs_hydro)

    # Test 2: Pesticide & Pest query
    imgs_pest = image_retriever.search_images("Show me pesticides used for crops.", top_k=2)
    assert len(imgs_pest) > 0
    assert any(img["image_id"] in ["IMG002", "IMG003"] for img in imgs_pest)

    # Test 3: Smart Irrigation query
    imgs_irr = image_retriever.search_images("Show me examples of smart irrigation.", top_k=2)
    assert len(imgs_irr) > 0
    assert any("drip" in img["image"].lower() or "solar" in img["image"].lower() for img in imgs_irr)

    # Test 4: Agent integration
    agent_res = ai_agent.plan_and_execute("What is hydroponic farming?")
    assert "IMG004" in agent_res["answer"]
    assert "Hydroponic NFT" in agent_res["answer"]
