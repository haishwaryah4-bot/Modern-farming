"""
Automated Test Runner for AgriSense AI Platform.
Runs all unit and integration tests across RAG, 8 Agent Tools, Scenarios, and Services.
"""

import sys
from pathlib import Path

# Ensure root is on path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Import test functions
from tests.test_rag import (
    test_document_loader_txt,
    test_document_loader_csv,
    test_text_splitter,
    test_hybrid_retrieval_and_rrf,
    test_minilm_embeddings,
    test_rag_engine_query,
)
from tests.test_agent import (
    test_agent_tools_registry,
    test_tool_irrigation_recommendation,
    test_tool_pest_disease_risk_assessment,
    test_tool_modern_technology_recommendation,
    test_scenario_rice_poor_drainage,
    test_scenario_tomato_flowering,
    test_scenario_small_farm_tech,
    test_image_retrieval_service,
)
from tests.test_services import (
    test_weather_service,
    test_market_service,
    test_crop_advisory_service,
    test_disease_service,
    test_soil_analysis_service,
)
from tests.test_api import (
    test_api_health,
    test_api_chat_endpoint,
    test_api_rag_query,
    test_api_list_documents,
)


def run_all_tests():
    print("=" * 75)
    print("RUNNING AGRISENSE AI PLATFORM COMPREHENSIVE TEST SUITE")
    print("=" * 75)

    tests = [
        ("Document Loader (Multi-Page Farming Dataset TXT)", test_document_loader_txt),
        ("Document Loader (Schemes CSV)", test_document_loader_csv),
        ("Text Splitter & Chunking with Page Metadata", test_text_splitter),
        ("Transformer Embeddings (sentence-transformers/all-MiniLM-L6-v2 384-dim)", test_minilm_embeddings),
        ("Hybrid Retrieval (Dense Vector + BM25 + Re-Ranking)", test_hybrid_retrieval_and_rrf),
        ("Grounded RAG Engine & Page Citations", test_rag_engine_query),
        ("Agent Tools Registry (8 Typed Tools)", test_agent_tools_registry),
        ("Tool: Irrigation Recommendation (AWD/ET0)", test_tool_irrigation_recommendation),
        ("Tool: Pest & Disease Risk Assessment", test_tool_pest_disease_risk_assessment),
        ("Tool: Modern Technology Recommendation", test_tool_modern_technology_recommendation),
        ("Scenario: Rice Kharif Poor Drainage & Humidity", test_scenario_rice_poor_drainage),
        ("Scenario: Tomato Flowering Irrigation & Fertigation", test_scenario_tomato_flowering),
        ("Scenario: Small Farm Limited Water Technologies", test_scenario_small_farm_tech),
        ("Visual Dataset Image Retrieval & Card Formatting", test_image_retrieval_service),
        ("Weather Domain Service", test_weather_service),
        ("Market Domain Service", test_market_service),
        ("Crop Advisory Domain Service", test_crop_advisory_service),
        ("Disease CV Diagnostic Service", test_disease_service),
        ("Soil Health Index & Amelioration", test_soil_analysis_service),
        ("FastAPI /api/health Endpoint", test_api_health),
        ("FastAPI /api/chat Agent Endpoint", test_api_chat_endpoint),
        ("FastAPI /api/rag/query Hybrid Endpoint", test_api_rag_query),
        ("FastAPI /api/documents List Endpoint", test_api_list_documents),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name} -> {e}")
            failed += 1

    print("=" * 75)
    print(f"RESULTS: {passed} Passed, {failed} Failed out of {len(tests)} tests.")
    print("=" * 75)

    if failed > 0:
        sys.exit(1)
    else:
        print("ALL AGRISENSE AI PLATFORM MODULES & PIPELINES VERIFIED SUCCESSFULLY!")


if __name__ == "__main__":
    run_all_tests()
