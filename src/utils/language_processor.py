"""
Multilingual, Transliteration & Regional Farmer Language Normalizer.
Translates Telugu (Unicode & Transliterated), Kannada (Unicode & Transliterated),
Hindi, and informal agricultural terms into semantic agronomic query concepts
for high-accuracy RAG retrieval.
"""

import re
from typing import Dict, Tuple, List, Set

# Regional & Transliterated Farmer Terms (Telugu, Kannada, Hindi, Dialects -> Agronomic English)
FARMER_VOCAB_MAP = {
    # Plant Anatomy & Crop parts
    "aaku": "leaf",
    "aakulu": "leaves",
    "yele": "leaf",
    "yelegallu": "leaves",
    "yeleya": "leaf",
    "komma": "branch",
    "veru": "root",
    "verulu": "roots",
    "beru": "root",
    "berugalu": "roots",
    "pootha": "flowering anthesis",
    "hoovu": "flower",
    "poovu": "flower",
    "kaya": "fruit pod",
    "kaayalu": "fruits pods",
    "kayi": "fruit pod",
    "panta": "crop agronomy",
    "bele": "crop agronomy",
    "mokka": "plant seedling",
    "gida": "plant seedling",
    "chetlu": "plants trees",
    "maragalu": "trees plants",
    "vithanalu": "seeds germination",
    "beeja": "seeds seed treatment",
    "beejagalu": "seeds",
    "beej": "seed",

    # Symptoms & Problems
    "pasupu": "yellowing chlorosis nutrient deficiency",
    "aridina": "yellowing chlorosis nutrient deficiency",
    "haladi": "yellowing chlorosis nitrogen deficiency",
    "yellow aytundi": "yellowing chlorosis",
    "yellowing": "yellowing chlorosis",
    "yallow": "yellowing chlorosis",
    "machalu": "spots lesions blight fungus",
    "macha": "spot lesion blight",
    "machhe": "spot lesion blight",
    "machhegalu": "spots lesions blight fungal",
    "kullipovadam": "rotting damping off",
    "kulla": "rot blight",
    "korakalu": "rotting fungal rot damping off",
    "vaadipotundi": "wilting fusarium wilt",
    "soraguvike": "wilting wilt disease",
    "mudatha": "leaf curl virus thrips",
    "madata": "leaf curl",
    "murutu": "leaf curl virus thrips",
    "yendipotundi": "drying withering drought stress",
    "onaguvudu": "drying withering dehydration",
    "chachipotundi": "dying withering necrosis",
    "problem": "disease damage issue pest",
    "samassye": "problem issue disease pest",

    # Pests, Insects & Parasites
    "purugu": "pest insect caterpillar bollworm",
    "purugulu": "pests insects caterpillars",
    "keeta": "pest insect caterpillar",
    "keetagalu": "pests insects caterpillars",
    "hula": "pest worm caterpillar insect",
    "hulagalu": "pests caterpillars insects",
    "puzhu": "pest caterpillar worm",
    "keeda": "pest insect",
    "chedda purugu": "harmful sucking pest aphid",
    "erra purugu": "red spider mite bollworm",
    "kempu hula": "red spider mite bollworm",
    "tella purugu": "whitefly sucking pest",
    "bili hula": "whitefly sucking pest",
    "pacha purugu": "green caterpillar leafhopper",
    "hasiru hula": "green caterpillar leafhopper",
    "doma": "hopper sucking pest jassid",
    "jigi hula": "leafhopper planthopper",
    "thrips": "thrips sucking pest",
    "aphids": "aphids sucking pest",

    # Inputs: Fertilizers, Water, Soil & Pesticides
    "mandu": "pesticide chemical fungicide spray",
    "mandulu": "pesticides fungicides sprays",
    "oushadha": "pesticide medicine chemical fungicide spray",
    "spray": "foliar spray pesticide application",
    "eruvulu": "fertilizer manure NPK fertigation",
    "eruvu": "fertilizer manure",
    "gobbaru": "fertilizer manure NPK FYM",
    "gobar": "farmyard manure compost FYM",
    "gomaya": "cow dung manure compost",
    "vermicompost": "vermicompost organic carbon",
    "neellu": "irrigation water watering schedule",
    "neeru": "irrigation water AWD drip",
    "paani": "water irrigation",
    "neeravari": "irrigation watering scheduling drip",
    "kattali": "irrigate apply water",
    "hakkabeku": "apply dose spray",
    "bhoomi": "soil soil health testing",
    "matti": "soil soil health testing pH",
    "mannu": "soil soil testing fertility",
    "zameen": "soil field",

    # --- NATIVE TELUGU UNICODE VOCABULARY ---
    "టమోటా": "tomato crop management yellow leaves",
    "టమాట": "tomato crop management",
    "వరి": "rice paddy AWD irrigation fertilizer split NPK",
    "వరి పంట": "rice paddy agronomy package of practices",
    "వరిలో": "rice paddy",
    "పత్తి": "cotton pest bollworm sucking pest management",
    "పత్తిలో": "cotton pest pink bollworm",
    "మిర్చి": "chilli leaf curl thrips virus management",
    "గోధుమ": "wheat CRI stage irrigation rust management",
    "మొక్కజొన్న": "maize fall armyworm management",
    "చెరకు": "sugarcane red rot fertigation",
    "వేరుశనగ": "groundnut tikka disease gypsum application",
    "సోయాబీన్": "soybean yellow mosaic rust",
    "ఆకులు": "leaves leaf foliage",
    "ఆకు": "leaf",
    "పసుపు": "yellowing chlorosis nitrogen deficiency",
    "మచ్చలు": "spots lesions blight leaf spot fungal",
    "ఎరువులు": "fertilizer NPK splits dosage application",
    "ఎరువుల": "fertilizer application",
    "నీరు": "irrigation water schedule AWD",
    "నీటి": "irrigation water management",
    "నీటి యాజమాన్యం": "irrigation water management AWD drip",
    "పురుగులు": "pests insects caterpillars sucking pests",
    "పురుగు": "pest caterpillar bollworm",
    "తెగులు": "disease blight rot fungal infection",
    "తెగుళ్ళు": "diseases fungi blights IPM",
    "చీడపీడలు": "pests and diseases integrated pest management IPM",
    "నివారణ": "control management remedy spray protocol",
    "రక్షణ": "precautions safety personal protective equipment",
    "జాగ్రత్తలు": "precautions safety farm procedures",
    "ఆధునిక": "modern precision smart agriculture technology",
    "సాంకేతికత": "technology drones IoT sensor precision",
    "పరికరాలు": "farming equipment machinery implements tractor rotavator",
    "పాడి": "dairy cattle livestock milk TMR silage",
    "పశువులు": "livestock cattle cow buffalo feeding silage",
    "మేత": "fodder green fodder silage nutrition",
    "విత్తనాలు": "seeds seed treatment priming",
    "నేల": "soil testing health card pH organic carbon",
    "ఖరీఫ్": "kharif monsoon season agronomy sowing",
    "రబీ": "rabi winter season wheat mustard gram",
    "దిగుబడి": "crop yield productivity maximization",
    "డ్రిప్": "drip micro-irrigation fertigation inline",

    # --- NATIVE KANNADA UNICODE VOCABULARY ---
    "ಟೊಮೆಟೊ": "tomato crop management yellow leaves",
    "ಟೊಮ್ಯಾಟೊ": "tomato crop management",
    "ಭತ್ತ": "rice paddy AWD irrigation fertilizer split NPK",
    "ಭತ್ತದ": "rice paddy agronomy package of practices",
    "ಭತ್ತದ ಬೆಳೆ": "rice paddy crop management",
    "ಹತ್ತಿ": "cotton pest bollworm sucking pest management",
    "ಹತ್ತಿಯಲ್ಲಿ": "cotton pest pink bollworm",
    "ಮೆಣಸಿನಕಾಯಿ": "chilli leaf curl thrips virus management",
    "ಗೋಧಿ": "wheat CRI stage irrigation rust management",
    "ಮೆಕ್ಕೆಜೋಳ": "maize fall armyworm management",
    "ಕಬ್ಬು": "sugarcane red rot fertigation",
    "ಕಡಲೆಕಾಯಿ": "groundnut tikka disease gypsum application",
    "ಸೋಯಾಬೀನ್": "soybean yellow mosaic rust",
    "ಎಲೆಗಳು": "leaves leaf foliage",
    "ಎಲೆ": "leaf",
    "ಹಳದಿ": "yellowing chlorosis nitrogen deficiency",
    "ಹಳದಿ ರೋಗ": "yellowing chlorosis nutrient deficiency",
    "ಮಚ್ಚೆಗಳು": "spots lesions blight leaf spot fungal",
    "ಗೊಬ್ಬರ": "fertilizer NPK splits dosage application",
    "ಗೊಬ್ಬರಗಳು": "fertilizers manure NPK FYM",
    "ರಸಗೊಬ್ಬರ": "chemical fertilizer NPK dosage",
    "ನೀರು": "irrigation water schedule AWD",
    "ನೀರಾವರಿ": "irrigation water management AWD drip",
    "ಹನಿ ನೀರಾವರಿ": "drip micro-irrigation fertigation inline",
    "ತುಂತುರು ನೀರಾವರಿ": "sprinkler micro-irrigation water saving",
    "ಕೀಟಗಳು": "pests insects caterpillars sucking pests",
    "ಕೀಟ": "pest insect caterpillar bollworm",
    "ಹುಳು": "pest caterpillar bollworm borer",
    "ಹುಳುಗಳು": "pests caterpillars borers",
    "ರೋಗ": "disease blight rot fungal infection",
    "ರೋಗಗಳು": "diseases fungi blights IPM",
    "ಪೀಡೆಗಳು": "pests and diseases integrated pest management IPM",
    "ನಿಯಂತ್ರಣ": "control management remedy spray protocol",
    "ಮುನ್ನೆಚ್ಚರಿಕೆ": "precautions safety personal protective equipment",
    "ರಕ್ಷಣೆ": "safety precautions PPE equipment",
    "ಆಧುನಿಕ": "modern precision smart agriculture technology",
    "ತಂತ್ರಜ್ಞಾನ": "technology drones IoT sensor precision",
    "ಯಂತ್ರೋಪಕರಣಗಳು": "farming equipment machinery implements tractor rotavator",
    "ಉಪಕರಣಗಳು": "farming tools equipment machinery",
    "ಹೈನುಗಾರಿಕೆ": "dairy cattle livestock milk TMR silage",
    "ಹಸು": "dairy cow cattle nutrition feed",
    "ದನಕರುಗಳು": "livestock cattle dairy management",
    "ಮೇವು": "fodder green fodder silage nutrition",
    "ಸೈಲೇಜ್": "silage making dairy green fodder fermentation",
    "ಬೀಜ": "seeds seed treatment priming",
    "ಬೀಜೋಪಚಾರ": "seed treatment bio-fertilizer fungicide",
    "ಮಣ್ಣು": "soil testing health card pH organic carbon",
    "ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ": "soil testing NPK nutrients amelioration",
    "ಖಾರಿಫ್": "kharif monsoon season agronomy sowing",
    "ರಬಿ": "rabi winter season wheat mustard gram",
    "ಇಳುವರಿ": "crop yield productivity maximization",
    "ಸಾವಯವ ಕೃಷಿ": "organic sustainable farming carbon enrichment",
    "ಕಳೆ": "weed management pre-emergence herbicide",
    "ಕಳೆನಾಶಕ": "weed control herbicide application"
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
    "bhatta": "rice",
    "mirchi": "chilli",
    "mirapa": "chilli",
    "cotton": "cotton",
    "prathi": "cotton",
    "kapas": "cotton",
    "hatti": "cotton",
    "makka": "maize",
    "jonnalu": "sorghum",
    "jola": "sorghum",
    "godhumalu": "wheat",
    "godhi": "wheat",
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


def is_telugu(text: str) -> bool:
    """Returns True if the text contains Telugu characters (Unicode U+0C00 to U+0C7F)."""
    if not text:
        return False
    return bool(re.search(r"[\u0C00-\u0C7F]", text))


def is_kannada(text: str) -> bool:
    """Returns True if the text contains Kannada characters (Unicode U+0C80 to U+0CFF)."""
    if not text:
        return False
    return bool(re.search(r"[\u0C80-\u0CFF]", text))


def detect_language(text: str) -> str:
    """Detects whether text is in Kannada ('kn'), Telugu ('te'), or English ('en')."""
    if is_kannada(text):
        return "kn"
    if is_telugu(text):
        return "te"
    return "en"


def normalize_farmer_query(query: str) -> Tuple[str, List[str], Dict[str, str]]:
    """
    Analyzes raw farmer query (informal, Telugu/Kannada Unicode/Transliterated, typos, short phrases)
    and produces:
    1. An enriched semantic English query for RAG retrieval.
    2. Extracted domain entities (Crop, Problem/Disease, Input/Tech).
    3. Suggested agronomic focus tags.
    """
    if not query:
        return "", [], {}

    raw_text = query.strip()
    raw_lower = raw_text.lower()

    # Extract terms from raw string directly using phrase mapping
    translated_concepts = []
    detected_entities = {
        "crop": None,
        "disease_or_symptom": None,
        "pest": None,
        "input_type": None,
        "technology": None,
    }

    # Detect Crop Mentions (English, Telugu & Kannada)
    crop_keywords = {
        "tomato": "Tomato",
        "ಟమోటా": "Tomato",
        "టమాట": "Tomato",
        "ಟೊಮೆಟೊ": "Tomato",
        "ಟೊಮ್ಯಾಟೊ": "Tomato",
        "rice": "Rice (Paddy)",
        "paddy": "Rice (Paddy)",
        "వరి": "Rice (Paddy)",
        "వరి పంట": "Rice (Paddy)",
        "భత్త": "Rice (Paddy)",
        "ಭತ್ತದ": "Rice (Paddy)",
        "wheat": "Wheat",
        "గోధుమ": "Wheat",
        "ಗೋಧಿ": "Wheat",
        "cotton": "Cotton",
        "పత్తి": "Cotton",
        "ಹತ್ತಿ": "Cotton",
        "chilli": "Chilli",
        "మిర్చి": "Chilli",
        "ಮೆಣಸಿನಕಾಯಿ": "Chilli",
        "maize": "Maize",
        "మొక్కజొన్న": "Maize",
        "ಮೆಕ್ಕೆಜೋಳ": "Maize",
        "soybean": "Soybean",
        "సోయాబీన్": "Soybean",
        "ಸೋಯಾಬೀನ್": "Soybean",
        "brinjal": "Brinjal",
        "వంకాయ": "Brinjal",
        "ಬದನೆಕಾಯಿ": "Brinjal",
        "sugarcane": "Sugarcane",
        "చెరకు": "Sugarcane",
        "ಕಬ್ಬು": "Sugarcane",
        "potato": "Potato",
        "బంగాళాదుంప": "Potato",
        "ಆಲೂಗಡ್ಡೆ": "Potato",
        "mustard": "Mustard",
        "ఆవాలు": "Mustard",
        "ಸಾಸಿವೆ": "Mustard",
        "groundnut": "Groundnut",
        "వేరుశనగ": "Groundnut",
        "ಕಡಲೆಕಾಯಿ": "Groundnut",
        "onion": "Onion",
        "ఉల్లి": "Onion",
        "ಈರುಳ್ಳಿ": "Onion",
        "vegetable": "Vegetables",
        "vegetables": "Vegetables",
        "కూరగాయలు": "Vegetables",
        "ತರಕಾರಿಗಳು": "Vegetables",
    }

    for k, name in crop_keywords.items():
        if k in raw_text or k in raw_lower:
            detected_entities["crop"] = name
            translated_concepts.append(name)
            break

    # Translate terms from dictionary (both phrases and single tokens)
    for phrase, english_term in FARMER_VOCAB_MAP.items():
        if phrase in raw_text or phrase in raw_lower:
            translated_concepts.append(english_term)
            if any(w in english_term for w in ["yellow", "blight", "curl", "rot", "spot"]):
                detected_entities["disease_or_symptom"] = english_term
            elif any(w in english_term for w in ["pest", "aphid", "caterpillar", "bollworm"]):
                detected_entities["pest"] = english_term
            elif any(w in english_term for w in ["fertilizer", "manure", "npk"]):
                detected_entities["input_type"] = "Fertilizer / Nutrient"
            elif any(w in english_term for w in ["irrigation", "water", "drip"]):
                detected_entities["input_type"] = "Irrigation / Water"
            elif any(w in english_term for w in ["equipment", "machinery", "technology", "drone"]):
                detected_entities["technology"] = english_term

    # Enriched query for semantic vector search
    enrichment = " ".join(set(translated_concepts))
    enriched_query = f"{raw_text} {enrichment}".strip() if enrichment else raw_text

    return enriched_query, translated_concepts, detected_entities
