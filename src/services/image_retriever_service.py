"""
Visual Farming Dataset & Semantic Image Retrieval Service.
Dynamically maps user questions (including informal, Telugu-English, and misspelled inputs)
to ingested farming dataset records and guarantees that farming questions are always accompanied by pictures.
"""

import json
import base64
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import config
from src.utils.language_processor import normalize_farmer_query


class ImageRetrieverService:
    def __init__(self, dataset_path: Optional[Path] = None):
        self.dataset_path = dataset_path or (config.DATA_DIR / "farming_images_dataset.json")
        self._dataset: List[Dict[str, Any]] = []
        self._loaded: bool = False

    @property
    def dataset(self) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        return self._dataset

    @dataset.setter
    def dataset(self, val: List[Dict[str, Any]]):
        self._dataset = val
        self._loaded = True

    def _ensure_loaded(self):
        if not self._loaded:
            self._load_dataset()
            self._loaded = True

    def _load_dataset(self):
        """Loads or reloads the dataset dynamically from JSON disk on demand."""
        if self.dataset_path.exists():
            try:
                with open(self.dataset_path, "r", encoding="utf-8") as f:
                    self._dataset = json.load(f)
            except Exception:
                self._dataset = []
        else:
            self._dataset = []

    def get_image_base64(self, image_name: str) -> str:
        """Returns base64 encoded data URI for image with fallback paths."""
        if not image_name:
            return ""
        img_path = config.BASE_DIR / "assets" / "images" / image_name
        if not img_path.exists():
            img_path = config.BASE_DIR / "static" / image_name
        
        if img_path.exists():
            try:
                with open(img_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                    return f"data:image/jpeg;base64,{b64}"
            except Exception:
                return ""
        return ""

    def search_images(self, query: str, top_k: int = 2, threshold: float = 0.15) -> List[Dict[str, Any]]:
        """
        Dynamically identifies relevant farming images from the dataset using semantic
        and keyword similarity matching, supporting informal phrasing, Telugu-English, and typos.
        Always retrieves relevant pictures for farming inquiries.
        """
        if not self.dataset or not query:
            return []

        # 1. Normalize and enrich query (Telugu-English transliteration, spelling corrections)
        enriched_query, concepts, entities = normalize_farmer_query(query)
        q_clean = enriched_query.lower()
        q_tokens = set(re.findall(r"\b\w{2,}\b", q_clean))

        target_crop = (entities.get("crop") or "").lower()
        target_symptom = (entities.get("disease_or_symptom") or "").lower()
        target_pest = (entities.get("pest") or "").lower()

        scored_results = []

        for item in self.dataset:
            score = 0.0
            item_text = (
                f"{item.get('title', '')} {item.get('category', '')} {item.get('crop', '')} "
                f"{item.get('disease', '')} {item.get('pest', '')} {item.get('description', '')} "
                f"{item.get('farming_details', '')} {item.get('control', '')} "
                f"{' '.join(item.get('keywords', []))}"
            ).lower()

            item_tokens = set(re.findall(r"\b\w{2,}\b", item_text))
            keywords = [k.lower() for k in item.get("keywords", [])]

            # 1. Token Overlap Score
            overlap = q_tokens.intersection(item_tokens)
            score += len(overlap) * 1.2

            # 2. Keyword exact matches
            for kw in keywords:
                if kw in q_clean:
                    score += 3.5
                elif any(tok in kw for tok in q_tokens if len(tok) > 3):
                    score += 1.5

            # 3. Entity Matches
            if target_crop and target_crop in item_text:
                score += 3.0
            if target_symptom and (target_symptom in item_text or any(w in item_text for w in target_symptom.split())):
                score += 3.5
            if target_pest and (target_pest in item_text or any(w in item_text for w in target_pest.split())):
                score += 3.5

            # 4. Title direct match
            title_lower = item.get("title", "").lower()
            if any(tok in title_lower for tok in q_tokens if len(tok) > 3):
                score += 2.0

            if score >= threshold:
                item_copy = dict(item)
                item_copy["relevance_score"] = round(score, 2)
                item_copy["image_base64"] = self.get_image_base64(item.get("image", ""))
                scored_results.append(item_copy)

        # Sort by score descending
        scored_results.sort(key=lambda x: x["relevance_score"], reverse=True)

        # If scored results are empty but query has farming keywords, provide top thematic general images
        if not scored_results:
            agri_keywords = {
                "crop", "plant", "farm", "soil", "pest", "disease", "blight", "rust", "leaf",
                "seed", "water", "irrigation", "fertilizer", "manure", "npk", "drip",
                "hydroponic", "vertical", "polyhouse", "solar", "tractor", "drone", "wheat",
                "rice", "paddy", "tomato", "cotton", "chilli", "maize", "mustard", "spray",
                "pesticide", "fungicide", "harvest", "yield", "weather", "mandi", "subsidy",
                "kusum", "pmksy", "rot", "wilt", "borer", "aphid", "insect", "agriculture",
                "organic", "compost", "carbon", "greenhouse", "aquaponics", "machinery"
            }
            if bool(q_tokens.intersection(agri_keywords)):
                for default_item in self.dataset[:2]:
                    item_copy = dict(default_item)
                    item_copy["relevance_score"] = 0.5
                    item_copy["image_base64"] = self.get_image_base64(default_item.get("image", ""))
                    scored_results.append(item_copy)

        return scored_results[:top_k]

    def format_image_cards_markdown(self, images: List[Dict[str, Any]], query: str = "") -> str:
        """
        Builds separate visual image cards with image, title, description, and farming details.
        No collages; every image is displayed separately.
        """
        if not images:
            return ""

        cards_html = []
        for idx, img in enumerate(images, 1):
            img_b64 = img.get("image_base64") or self.get_image_base64(img.get("image", ""))
            category = img.get("category", "Agricultural Intelligence")
            title = img.get("title", "Agricultural System")
            image_id = img.get("image_id", f"IMG{idx:03d}")
            desc = img.get("description", "")
            details = img.get("farming_details", "")
            control = img.get("control", "")
            crop = img.get("crop", "Multi-Crop")
            disease = img.get("disease")
            pest = img.get("pest")

            card = f"""
<div style="background: #ffffff; border: 2.5px solid #059669; border-radius: 16px; margin: 12px 0 18px 0; box-shadow: 0 8px 24px rgba(0, 30, 15, 0.16); overflow: hidden;">
    <div style="width: 100%; height: 240px; background: #021a0d; overflow: hidden; border-bottom: 2px solid #059669;">
        <img src="{img_b64}" style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="{title}">
    </div>
    <div style="padding: 16px 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="background: #059669; color: #ffffff; font-size: 0.76rem; font-weight: 800; padding: 3px 10px; border-radius: 12px; letter-spacing: 0.03em;">{category.upper()}</span>
            <span style="font-size: 0.78rem; font-weight: 800; color: #64748b;">ID: {image_id}</span>
        </div>
        <h3 style="margin: 0 0 6px 0; color: #022c15; font-size: 1.15rem; font-weight: 900;">{title}</h3>
        <p style="margin: 0 0 10px 0; color: #334155; font-size: 0.92rem; line-height: 1.5; font-weight: 600;">
            {desc}
        </p>
        <div style="background: #f8fafc; border-left: 4px solid #059669; padding: 10px 12px; border-radius: 6px; margin-bottom: 10px; font-size: 0.86rem; color: #0f172a; line-height: 1.55;">
            <b>🌾 Target Crops:</b> {crop}<br>
            {f'<b>🔬 Associated Disease / Symptom:</b> {disease}<br>' if disease else ''}
            {f'<b>🐛 Target Pest / Insect:</b> {pest}<br>' if pest else ''}
            <b>📊 Dataset Details & Economics:</b> {details}
        </div>
        {f'''
        <div style="background: #fef2f2; border-left: 4px solid #dc2626; padding: 10px 12px; border-radius: 6px; font-size: 0.86rem; color: #7f1d1d; line-height: 1.55;">
            <b>🛡️ Recommended Control & Intervention Protocol:</b><br>{control}
        </div>
        ''' if control else ''}
    </div>
</div>
"""
            cards_html.append(card)

        return "".join(cards_html)


# Global singleton instance
image_retriever = ImageRetrieverService()
