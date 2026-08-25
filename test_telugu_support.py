import sys
sys.stdout.reconfigure(encoding='utf-8')

from server import handle_chat_query

test_cases = [
    ("Telugu - Rice Agronomy", "వరి పంటకు ఎరువుల మోతాదు మరియు నీటి యాజమాన్యం ఎలా ఉండాలి?"),
    ("Telugu - Tomato Yellow Leaves", "టమోటా ఆకులు పసుపు రంగులోకి మారుతున్నాయి ఏమి చేయాలి?"),
    ("Telugu - Cotton Pink Bollworm", "పత్తిలో గులాబీ రంగు పురుగు నివారణ ఏమిటి?"),
    ("Telugu - Transliterated", "Tomato aaku yellow aytundi em mandu kottali?"),
    ("Telugu - Greeting", "నమస్కారం"),
    ("English - Precision Farming", "What is precision agriculture?"),
    ("Telugu - Out of domain", "ఫ్రాన్స్ రాజధాని ఏమిటి?"),
]

print("=" * 80)
print("TESTING BILINGUAL ENGLISH & TELUGU RAG PLATFORM SUPPORT")
print("=" * 80)

all_passed = True
for name, q in test_cases:
    res = handle_chat_query(q)
    ans = res["answer"]
    citations = res.get("citations", [])
    
    if name == "Telugu - Out of domain":
        passed = ("లభించలేదు" in ans or "couldn't find" in ans)
    elif name == "Telugu - Greeting":
        passed = ("నమస్కారం" in ans or "AgriSense" in ans)
    else:
        passed = len(citations) > 0 and ("సమాధానం" in ans or "Answer" in ans)

    print(f"\n[{'✅ PASS' if passed else '❌ FAIL'}] {name}")
    print(f"  Question: {q}")
    print(f"  Citations: {len(citations)}")
    for c in citations[:2]:
        print(f"    • {c.get('source')} (Page {c.get('page')} - {c.get('topic')})")
    
    print(f"  Answer Excerpt:\n  {ans[:200]}...")

    if not passed:
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("🎉 ALL ENGLISH & TELUGU BILINGUAL RAG QUERIES VERIFIED 100% PASSING!")
else:
    print("❌ SOME TEST CASES FAILED")
print("=" * 80)
