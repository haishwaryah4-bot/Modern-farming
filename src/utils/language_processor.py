"""
Multilingual, Transliteration & Informal Farmer Language Normalizer.
Translates Telugu-English mixed terms, regional vocabulary, spelling errors,
and informal farmer phrases into semantic agronomic query concepts.
"""

import re
from typing import Dict, Tuple, List, Set

# Regional & Transliterated Farmer Terms (Telugu, Hindi, Dialects -> Agronomic English)
FARMER_VOCAB_MAP = {
    # Plant Anatomy & Crop parts
    "aaku": "leaf",
    "aakulu": "leaves",
    "komma": "branch",
    "veru": "root",
    "verulu": "roots",
    "pootha": "flowering",
    "poovu": "flower",
    "kaya": "fruit",
    "kaayalu": "fruits",
    "panta": "crop",
    "mokka": "plant",
    "mokkalu": "plants",
    "chetlu": "trees plants",
    "vithanalu": "seeds",
    "vithanam": "seed",
    "beej": "seed",

    # Symptoms & Problems
    "pasupu": "yellowing chlorosis",
    "yellow aytundi": "yellowing chlorosis",
    "yellowing": "yellowing chlorosis",
    "yallow": "yellowing chlorosis",
    "machalu": "spots lesions blight",
    "macha": "spot lesion blight",
    "kullipovadam": "rotting damping off",
    "kulla": "rot blight",
    "kullipothundi": "rotting damping off",
    "vaadipotundi": "wilting wilt",
    "vadipovadam": "wilting",
    "mudatha": "leaf curl virus",
    "madata": "leaf curl",
    "yendipotundi": "drying withering",
    "chachipotundi": "dying withering",
    "problem": "disease damage issue",

    # Pests, Insects & Parasites
    "purugu": "pest insect caterpillar",
    "purugulu": "pests insects caterpillars",
    "puzhu": "pest caterpillar worm",
    "keeda": "pest insect",
    "chedda purugu": "harmful sucking pest aphid",
    "peka purugu": "aphid sucking pest",
    "erra purugu": "red spider mite bollworm",
    "tella purugu": "whitefly sucking pest",
    "pacha purugu": "green caterpillar leafhopper",
    "doma": "hopper sucking pest jassid",
    "tella doma": "whitefly",
    "pacha doma": "green leafhopper",
    "thrips": "thrips sucking pest",
    "aphids": "aphids sucking pest",

    # Inputs: Fertilizers, Water, Soil & Pesticides
    "mandu": "pesticide chemical fungicide spray",
    "mandulu": "pesticides fungicides sprays",
    "mandoo": "pesticide spray",
    "dawai": "pesticide medicine",
    "dava": "pesticide medicine",
    "spray": "foliar spray pesticide application",
    "eruvulu": "fertilizer manure NPK",
    "eruvu": "fertilizer manure",
    "gobar": "farmyard manure compost FYM",
    "penta": "farmyard manure compost FYM",
    "vermicompost": "vermicompost organic carbon",
    "neellu": "irrigation water watering",
    "neeru": "irrigation water",
    "paani": "water irrigation",
    "kattali": "irrigate apply water",
    "petali": "apply dose",
    "veyali": "apply fertilizer spray",
    "bhoomi": "soil soil health",
    "matti": "soil soil health",
    "zameen": "soil field",

    # Interrogatives & Common Phrases
    "enduku": "why reason cause",
    "em": "what diagnosis",
    "emi": "what diagnosis",
    "ela": "how method procedure",
    "eppudu": "when timing schedule",
    "yentha": "how much dosage rate",
    "yela": "how procedure",
    "cheppandi": "explain recommend advice",
    "chudu": "inspect diagnose",
    "em problem": "what is the disease or pest issue",
}

# Common Spelling Corrections & Typo Normalizations
SPELLING_CORRECTIONS = {
    "tomoto": "tomato",
    "tomatos": "tomato",
    "tamata": "tomato",
    "tamato": "tomato",
    "tamatar": "tomato",
    "paddy": "rice",
    "dhaan": "rice",
    "vadlu": "rice",
    "mirchi": "chilli",
    "mirapa": "chilli",
    "cotton": "cotton",
    "prathi": "cotton",
    "kapas": "cotton",
    "makka": "maize",
    "jonnalu": "sorghum",
    "godhumalu": "wheat",
    "gehu": "wheat",
    "pestiside": "pesticide",
    "pesticids": "pesticides",
    "pestcide": "pesticide",
    "fungiside": "fungicide",
    "fertlizer": "fertilizer",
    "fertilisr": "fertilizer",
    "irigation": "irrigation",
    "erigation": "irrigation",
    "hydraponic": "hydroponic",
    "hidroponic": "hydroponic",
    "hydroponik": "hydroponic",
    "verticle": "vertical",
    "vertikal": "vertical",
    "polyhous": "polyhouse",
    "poli house": "polyhouse",
    "greenhous": "greenhouse",
    "solor": "solar",
    "dron": "drone",
    "aweed": "AWD",
    "npk": "NPK",
}


def normalize_farmer_query(query: str) -> Tuple[str, List[str], Dict[str, str]]:
    """
    Analyzes raw farmer query (informal, Telugu-English, typos, short phrases)
    and produces:
    1. An enriched semantic English query for RAG retrieval.
    2. Extracted domain entities (Crop, Problem/Disease, Input/Tech).
    3. Suggested agronomic focus tags.
    """
    if not query:
        return "", [], {}

    raw_lower = query.lower().strip()
    # Tokenize preserving alphanumeric words
    tokens = re.findall(r"\b[a-zA-Z0-9_\-']+\b", raw_lower)

    # 1. Spelling correction & phrase substitution
    normalized_tokens = []
    for t in tokens:
        corrected = SPELLING_CORRECTIONS.get(t, t)
        normalized_tokens.append(corrected)

    working_text = " ".join(normalized_tokens)

    # 2. Regional & Telugu-English term translation
    translated_concepts = []
    detected_entities = {
        "crop": None,
        "disease_or_symptom": None,
        "pest": None,
        "input_type": None,
        "technology": None,
    }

    # Detect Crop Mentions
    crop_keywords = {
        "tomato": "Tomato",
        "rice": "Rice (Paddy)",
        "paddy": "Rice (Paddy)",
        "wheat": "Wheat",
        "cotton": "Cotton",
        "chilli": "Chilli",
        "maize": "Maize",
        "soybean": "Soybean",
        "brinjal": "Brinjal",
        "sugarcane": "Sugarcane",
        "potato": "Potato",
        "mustard": "Mustard",
        "onion": "Onion",
        "vegetable": "Vegetables",
        "vegetables": "Vegetables",
    }
    for k, name in crop_keywords.items():
        if k in working_text:
            detected_entities["crop"] = name
            translated_concepts.append(name)
            break

    # Translate terms
    for phrase, english_term in FARMER_VOCAB_MAP.items():
        if phrase in working_text:
            translated_concepts.append(english_term)
            if "yellow" in english_term or "blight" in english_term or "curl" in english_term or "rot" in english_term:
                detected_entities["disease_or_symptom"] = english_term
            elif "pest" in english_term or "aphid" in english_term or "caterpillar" in english_term:
                detected_entities["pest"] = english_term
            elif "fertilizer" in english_term or "manure" in english_term:
                detected_entities["input_type"] = "Fertilizer / Nutrient"
            elif "irrigation" in english_term:
                detected_entities["input_type"] = "Irrigation / Water"

    # Enriched query for semantic vector search
    enrichment = " ".join(set(translated_concepts))
    enriched_query = f"{working_text} {enrichment}".strip()

    return enriched_query, translated_concepts, detected_entities
