"""
Crop Advisory Service delivering tailored recommendations for sowing,
irrigation, fertilizer splits, and disease prevention across growth stages.
"""

import json
from typing import Dict, Any, Optional
import config


class CropAdvisoryService:
    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file or (config.DATA_DIR / "crop_database.json")
        self._database = {}
        self._load_database()

    def _load_database(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                self._database = json.load(f)
        except Exception:
            self._database = {}

    def get_advisory(
        self,
        crop: str,
        growth_stage: str,
        soil_type: str = "Alluvial Soil",
        season: str = "Kharif (Monsoon)",
        location: str = "Ludhiana, Punjab",
    ) -> Dict[str, Any]:
        """
        Generate contextual crop advisory combining database rules with field parameters.
        """
        crop_data = self._database.get(crop)
        if not crop_data:
            # General fallback template
            return {
                "crop": crop,
                "growth_stage": growth_stage,
                "soil_type": soil_type,
                "season": season,
                "location": location,
                "optimal_ph": "6.0 - 7.5",
                "water_requirement_mm": "500 - 800",
                "irrigation_advice": "Maintain 50% field capacity moisture in the root zone.",
                "fertilizer_dosage": "Apply balanced NPK 4:2:1 based on local soil test values.",
                "disease_prevention": "Scout weekly for fungal leaf spots and sucking pests.",
                "operational_actions": "Weed management and adequate furrow drainage.",
                "caution": "Recommendations are informational and subject to localized soil moisture and weather conditions.",
            }

        stage_info = crop_data.get("stages", {}).get(
            growth_stage,
            {
                "irrigation": "Maintain optimal root zone moisture.",
                "fertilizer": "Follow state agricultural university split schedule.",
                "pests_diseases": "Monitor for common seasonal pathogens.",
                "action": "Ensure field sanitation and timely scouting.",
            },
        )

        npk = crop_data.get("npk_ratio_kg_acre", {"N": 50, "P": 25, "K": 20})

        return {
            "crop": crop,
            "growth_stage": growth_stage,
            "soil_type": soil_type,
            "season": season,
            "location": location,
            "optimal_ph": crop_data.get("optimal_ph", "6.0 - 7.5"),
            "water_requirement_mm": crop_data.get("water_requirement_mm", "600 - 900"),
            "growth_duration_days": crop_data.get("growth_duration_days", "120 - 150"),
            "base_npk_per_acre": f"N: {npk.get('N')} kg, P2O5: {npk.get('P')} kg, K2O: {npk.get('K')} kg",
            "irrigation_advice": stage_info.get("irrigation"),
            "fertilizer_dosage": stage_info.get("fertilizer"),
            "disease_prevention": stage_info.get("pests_diseases"),
            "operational_actions": stage_info.get("action"),
            "caution": "Recommendations are informational. Always verify with your local district Krishi Vigyan Kendra (KVK) or extension officer.",
        }


crop_advisory_service = CropAdvisoryService()
