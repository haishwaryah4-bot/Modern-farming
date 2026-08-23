"""
Soil Health & Nutrient Analysis Service.
Parses soil test reports (PDF/CSV/TXT/Manual), evaluates macro and micro nutrients
against scientific thresholds, computes Soil Health Index, and generates fertilizer prescriptions.
"""

import re
import csv
import io
from typing import Dict, Any, List, Optional


class SoilService:
    # Standard Agronomic Benchmarks
    BENCHMARKS = {
        "pH": {"low": 6.5, "high": 7.5, "unit": "pH scale", "name": "Soil Reaction (pH)"},
        "EC": {"low": 0.0, "high": 1.0, "unit": "dS/m", "name": "Electrical Conductivity"},
        "OC": {"low": 0.50, "high": 0.75, "unit": "%", "name": "Organic Carbon"},
        "N": {"low": 280.0, "high": 560.0, "unit": "kg/ha", "name": "Available Nitrogen (N)"},
        "P": {"low": 23.0, "high": 56.0, "unit": "kg/ha", "name": "Available Phosphorus (P2O5)"},
        "K": {"low": 140.0, "high": 280.0, "unit": "kg/ha", "name": "Available Potassium (K2O)"},
        "Zn": {"low": 0.6, "high": 1.2, "unit": "ppm", "name": "Available Zinc (Zn)"},
        "Fe": {"low": 4.5, "high": 9.0, "unit": "ppm", "name": "Available Iron (Fe)"},
        "B": {"low": 0.5, "high": 1.0, "unit": "ppm", "name": "Available Boron (B)"},
        "S": {"low": 10.0, "high": 20.0, "unit": "ppm", "name": "Available Sulfur (S)"},
    }

    def parse_soil_data_from_text(self, text: str) -> Dict[str, float]:
        """
        Extract numerical soil parameters from raw text or OCR outputs.
        """
        data = {}
        patterns = {
            "pH": r"pH\s*[:=\s]+([\d\.]+)",
            "EC": r"(?:EC|Electrical\s*Cond[\w\s]*)\s*[:=\s]+([\d\.]+)",
            "OC": r"(?:OC|Organic\s*Carbon)\s*[:=\s]+([\d\.]+)",
            "N": r"(?:Available\s*Nitrogen|\bN\b)\s*[:=\s]+([\d\.]+)",
            "P": r"(?:Available\s*Phosphorus|\bP2?O?5?\b)\s*[:=\s]+([\d\.]+)",
            "K": r"(?:Available\s*Potassium|\bK2?O?\b)\s*[:=\s]+([\d\.]+)",
            "Zn": r"(?:Zinc|\bZn\b)\s*[:=\s]+([\d\.]+)",
            "Fe": r"(?:Iron|\bFe\b)\s*[:=\s]+([\d\.]+)",
            "B": r"(?:Boron|\bB\b)\s*[:=\s]+([\d\.]+)",
            "S": r"(?:Sulfur|\bS\b)\s*[:=\s]+([\d\.]+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    data[key] = float(match.group(1))
                except ValueError:
                    pass
        return data

    def parse_soil_csv(self, file_content: str) -> Dict[str, float]:
        """
        Parse CSV soil report.
        """
        data = {}
        reader = csv.reader(io.StringIO(file_content))
        for row in reader:
            if len(row) >= 2:
                param, val = row[0].strip().lower(), row[1].strip()
                try:
                    num_val = float(re.findall(r"[\d\.]+", val)[0])
                    if "ph" in param:
                        data["pH"] = num_val
                    elif "ec" in param or "conductivity" in param:
                        data["EC"] = num_val
                    elif "carbon" in param or "oc" in param:
                        data["OC"] = num_val
                    elif "nitrogen" in param or param == "n":
                        data["N"] = num_val
                    elif "phosphorus" in param or "p2o5" in param or param == "p":
                        data["P"] = num_val
                    elif "potassium" in param or "k2o" in param or param == "k":
                        data["K"] = num_val
                    elif "zinc" in param or param == "zn":
                        data["Zn"] = num_val
                    elif "iron" in param or param == "fe":
                        data["Fe"] = num_val
                    elif "boron" in param or param == "b":
                        data["B"] = num_val
                    elif "sulfur" in param or param == "s":
                        data["S"] = num_val
                except (IndexError, ValueError):
                    continue
        return data

    def analyze_soil(self, values: Dict[str, float]) -> Dict[str, Any]:
        """
        Complete agronomic evaluation of soil nutrients with ratings,
        health score, and targeted fertilizer dosage.
        """
        evaluated_parameters = []
        score_components = []
        recommendations = []

        for key, b in self.BENCHMARKS.items():
            val = values.get(key)
            if val is None:
                continue

            status = "Optimal / Sufficient"
            status_class = "badge-optimal"

            if key == "pH":
                if val < 6.5:
                    status = "Acidic (Needs Lime)"
                    status_class = "badge-warning"
                    recommendations.append("Apply Agricultural Limestone (CaCO3) @ 1.5 - 2 tonnes/acre to neutralize acidity.")
                elif val > 7.5:
                    status = "Alkaline / Sodic"
                    status_class = "badge-warning"
                    recommendations.append("Apply Agricultural Gypsum (CaSO4.2H2O) @ 1 tonne/acre followed by green manuring.")
            elif key == "EC":
                if val > 1.0:
                    status = "High Salinity Risk"
                    status_class = "badge-danger"
                    recommendations.append("Provide good quality drainage leaching to flush excess soluble salts.")
            else:
                if val < b["low"]:
                    status = "Low / Deficient"
                    status_class = "badge-danger"
                    if key == "OC":
                        recommendations.append("Apply 5-8 tonnes/acre Farm Yard Manure (FYM) or Vermicompost to restore biological carbon.")
                    elif key == "N":
                        recommendations.append("Increase basal and vegetative Urea top-dressing by 25% (total 70-80 kg Urea/acre in splits).")
                    elif key == "P":
                        recommendations.append("Apply Single Super Phosphate (SSP) @ 100 kg/acre or DAP @ 50 kg/acre with PSB biofertilizer.")
                    elif key == "K":
                        recommendations.append("Apply Muriate of Potash (MOP) @ 30 kg/acre to improve crop vigor and drought tolerance.")
                    elif key == "Zn":
                        recommendations.append("Soil application of Zinc Sulfate (21% Zn) @ 10 kg/acre at the time of final land preparation.")
                    elif key == "B":
                        recommendations.append("Foliar application of Solubor (Boron 20%) @ 1g/liter during pre-flowering stage.")
                    elif key == "S":
                        recommendations.append("Apply elemental sulfur or gypsum @ 15 kg/acre to stimulate amino acid synthesis.")
                elif val > b["high"]:
                    status = "High / Excess"
                    status_class = "badge-optimal"
                    if key == "N":
                        recommendations.append("Reduce nitrogenous fertilizer by 20% to avoid excessive vegetative growth and pest vulnerability.")
                    elif key == "K":
                        recommendations.append("Withhold potash application for current season.")

            # Component scoring
            if "Deficient" in status or "Danger" in status_class or "Acidic" in status:
                score_components.append(50)
            elif "Optimal" in status or "Sufficient" in status or "Medium" in status:
                score_components.append(100)
            else:
                score_components.append(75)

            evaluated_parameters.append({
                "param_key": key,
                "name": b["name"],
                "value": val,
                "unit": b["unit"],
                "status": status,
                "status_class": status_class,
                "benchmark_range": f"{b['low']} - {b['high']} {b['unit']}",
            })

        soil_health_index = int(sum(score_components) / len(score_components)) if score_components else 70

        return {
            "soil_health_index": soil_health_index,
            "overall_status": "Healthy / Well-Balanced" if soil_health_index >= 80 else ("Moderate / Needs Amelioration" if soil_health_index >= 60 else "Degraded / Severely Deficient"),
            "parameters": evaluated_parameters,
            "recommendations": recommendations,
        }


soil_service = SoilService()
