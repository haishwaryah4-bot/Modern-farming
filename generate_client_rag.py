import json

with open('data/embedded_kb.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)

chunks_json = json.dumps(chunks, ensure_ascii=False)

js_content = f"""// AgriSense AI - Client-Side Resilient RAG Engine (Zero-Downtime Knowledge Base)
const EMBEDDED_CHUNKS = {chunks_json};

const AGRI_STOPWORDS = new Set([
  'what', 'is', 'the', 'of', 'in', 'and', 'to', 'for', 'are', 'a', 'an', 'how', 'why', 'can',
  'should', 'do', 'does', 'with', 'from', 'at', 'by', 'this', 'that', 'these', 'those', 'it',
  'its', 'or', 'as', 'on', 'be', 'tell', 'me', 'about', 'explain', 'give', 'detail', 'details'
]);

const AGRI_DOMAIN_KEYWORDS = new Set([
  'crop', 'crops', 'plant', 'plants', 'farm', 'farming', 'soil', 'pest', 'pests', 'disease', 'diseases',
  'blight', 'rust', 'leaf', 'leaves', 'seed', 'seeds', 'water', 'irrigation', 'fertigation', 'fertilizer',
  'fertilizers', 'manure', 'npk', 'drip', 'hydroponic', 'hydroponics', 'vertical', 'polyhouse', 'greenhouse',
  'solar', 'tractor', 'drone', 'drones', 'wheat', 'rice', 'paddy', 'tomato', 'tomatoes', 'cotton', 'chilli',
  'maize', 'corn', 'mustard', 'spray', 'pesticide', 'pesticides', 'fungicide', 'fungicides', 'harvest',
  'yield', 'weather', 'mandi', 'msp', 'subsidy', 'kusum', 'pmksy', 'rot', 'wilt', 'borer', 'aphid',
  'aphids', 'insect', 'insects', 'agriculture', 'organic', 'compost', 'carbon', 'precision', 'benefit',
  'benefits', 'sprinkler', 'agritech', 'modern', 'potash', 'nitrogen', 'phosphorus', 'zinc', 'iron',
  'drainage', 'humidity', 'loam', 'clay', 'salinity', 'alkaline', 'acidic', 'gypsum', 'pyrite', 'lime',
  'awd', 'alternate', 'wetting', 'drying', 'root', 'roots', 'stem', 'pod', 'grain', 'sowing', 'transplanting',
  'tillering', 'flowering', 'bph', 'planthopper', 'armyworm', 'pink', 'bollworm', 'whitefly', 'thrips',
  'imidacloprid', 'mancozeb', 'chlorantraniliprole', 'tricyclazole', 'hexaconazole', 'urea', 'dap', 'mop'
]);

function tokenizeQuery(q) {{
  return (q || '').toLowerCase()
    .replace(/[^a-z0-9\\s]/g, ' ')
    .split(/\\s+/)
    .filter(w => w.length > 2 && !AGRI_STOPWORDS.has(w));
}}

function runClientRAG(question, imageData) {{
  const q = (question || '').trim();
  const qLower = q.toLowerCase();
  
  // Greetings
  if (['hi', 'hello', 'hey', 'namaste', 'help'].includes(qLower.replace(/[^a-z]/g, ''))) {{
    return {{
      answer: '**Answer:**\\nHello! I am your **AgriSense AI Assistant**.\\n\\n**Details:**\\nI search verified Modern Farming datasets covering precision agriculture, crop management, AWD rice, fertigation, pest & disease control, soil health, and PM-KUSUM subsidies.\\n\\n**What to do:**\\n- Try asking: *\"What is precision agriculture?\"*, *\"What is fertigation?\"*, or *\"What are the benefits of modern farming?\"*',
      citations: [{{ source: 'Modern Farming Dataset', page: 'Verified Knowledge Base', topic: 'Agronomic Guidance' }}],
      intent: 'Greeting'
    }};
  }}

  const tokens = tokenizeQuery(q);
  const isAgriRelated = tokens.some(t => AGRI_DOMAIN_KEYWORDS.has(t)) || Boolean(imageData);

  // Strict Out-of-Domain Refusal
  if (!isAgriRelated && tokens.length > 0) {{
    return {{
      answer: "I couldn't find this information in the provided dataset.",
      citations: [],
      intent: 'Out of Domain Query'
    }};
  }}

  // Score Chunks
  const scored = [];
  for (const c of EMBEDDED_CHUNKS) {{
    const textLower = c.text.toLowerCase();
    const topicLower = (c.topic || '').toLowerCase();
    let score = 0;

    for (const t of tokens) {{
      if (textLower.includes(t)) score += 2.0;
      if (topicLower.includes(t)) score += 4.0;
    }}

    if (score > 0) {{
      scored.push({{ chunk: c, score }});
    }}
  }}

  scored.sort((a, b) => b.score - a.score);
  const topChunks = scored.slice(0, 4).map(s => s.chunk);

  if (topChunks.length === 0) {{
    return {{
      answer: "I couldn't find this information in the provided dataset.",
      citations: [],
      intent: 'Out of Domain Query'
    }};
  }}

  // Extract lines
  const lines = [];
  const citations = [];
  for (const c of topChunks) {{
    citations.push({{ source: c.source, page: c.page, topic: c.topic }});
    for (const rawLine of c.text.split('\\n')) {{
      const l = rawLine.trim();
      if (l.length > 20 && !l.startsWith('PAGE ') && !l.startsWith('Document:') && !l.startsWith('---')) {{
        lines.push(l);
      }}
    }}
  }}

  // Select key answers
  const primaryAns = lines.slice(0, 2).join(' ').replace(/^[-*•\\d.\\s]+/, '');
  const details = lines.slice(2, 5).map(l => '- ' + l.replace(/^[-*•\\d.\\s]+/, '')).join('\\n');
  const action = lines.slice(5, 8).map(l => '- ' + l.replace(/^[-*•\\d.\\s]+/, '')).join('\\n');

  const citeText = citations.slice(0, 2).map(c => `${{c.source}} (Page ${{c.page}})`).join(', ');

  let finalAnswer = `**Answer:**\\n${{primaryAns || 'Based on the verified Modern Farming dataset, follow standard agronomic protocol.'}}\\n\\n`;
  if (details) {{
    finalAnswer += `**Details / Key Principles:**\\n${{details}}\\n\\n`;
  }}
  if (action) {{
    finalAnswer += `**What to do:**\\n${{action}}\\n\\n`;
  }}
  finalAnswer += `📄 *Verified Knowledge Source: ${{citeText || 'Modern Farming Dataset'}}*`;

  return {{
    answer: finalAnswer,
    citations: citations,
    intent: 'Modern Farming RAG'
  }};
}}

if (typeof window !== 'undefined') {{
  window.runClientRAG = runClientRAG;
}}
"""

with open('static/client_rag.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated static/client_rag.js with {len(chunks)} chunks!")
