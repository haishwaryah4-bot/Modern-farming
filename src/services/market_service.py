"""
Market Service for commodity price tracking, mandi comparisons,
historical price simulation, and price alerts.
"""

import os
import csv
from typing import Dict, Any, List, Optional
import random
import config


class MarketService:
    def __init__(self, data_file: Optional[str] = None):
        self.data_file = data_file or (config.DATA_DIR / "market_prices.csv")
        self._cache: List[Dict[str, Any]] = []
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self._cache = [row for row in reader]

    def get_all_prices(self) -> List[Dict[str, Any]]:
        return self._cache

    def get_crop_market_summary(self, crop: str) -> Dict[str, Any]:
        """
        Get price statistics and mandi comparisons for a specific crop.
        """
        records = [r for r in self._cache if crop.lower() in r["Crop"].lower()]
        if not records:
            # Fallback default
            return {
                "crop": crop,
                "modal_price": 2400,
                "min_price": 2200,
                "max_price": 2550,
                "msp": 2275,
                "trend": "Stable",
                "mandis": [],
                "weekly_change_pct": 0.0,
            }

        modal_prices = [float(r["Modal_Price_Quintal"]) for r in records]
        avg_modal = sum(modal_prices) / len(modal_prices)
        msp = float(records[0].get("MSP_Quintal", avg_modal * 0.9))

        return {
            "crop": crop,
            "modal_price": round(avg_modal, 2),
            "min_price": min(float(r["Min_Price_Quintal"]) for r in records),
            "max_price": max(float(r["Max_Price_Quintal"]) for r in records),
            "msp": msp,
            "trend": records[0].get("Price_Trend", "Stable"),
            "mandis": records,
            "weekly_change_pct": records[0].get("Weekly_Change_Pct", "+1.2"),
        }

    def generate_price_history_series(self, crop: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Generate 30-day historical daily price trend for interactive charts.
        """
        summary = self.get_crop_market_summary(crop)
        base = summary["modal_price"]
        history = []

        import datetime
        today = datetime.date.today()

        random.seed(abs(hash(crop)) % 1000)
        current = base - (days * 3)

        for i in range(days):
            date_val = today - datetime.timedelta(days=(days - 1 - i))
            drift = random.uniform(-18.0, 24.0)
            current = max(base * 0.8, min(base * 1.25, current + drift))
            history.append({
                "date": date_val.strftime("%Y-%m-%d"),
                "modal_price": round(current, 1),
                "msp": summary["msp"],
                "upper_band": round(current * 1.05, 1),
                "lower_band": round(current * 0.95, 1),
            })
        return history


market_service = MarketService()
