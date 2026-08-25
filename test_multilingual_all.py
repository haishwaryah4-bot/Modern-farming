import sys
sys.stdout.reconfigure(encoding='utf-8')

from server import handle_chat_query

test_suite = [
    ("Kannada - Greeting", "ನಮಸ್ಕಾರ"),
    ("Kannada - Tomato Yellow Leaves", "ಟೊಮೆಟೊ ಎಲೆಗಳು ಹಳದಿಯಾಗುತ್ತಿವೆ, ಏನು ಮಾಡಬೇಕು?"),
    ("Kannada - Rice Fertilizer & Water", "ಭತ್ತದ ಬೆಳೆಗೆ ಗೊಬ್ಬರ ಮತ್ತು ನೀರಾವರಿ ನಿರ್ವಹಣೆ ಹೇಗೆ ಮಾಡಬೇಕು?"),
    ("Kannada - Cotton Pink Bollworm", "ಹತ್ತಿಯಲ್ಲಿ ಗುಲಾಬಿ ಕಾಯಿಕೊರಕ ಮತ್ತು ರಸಹೀರುವ ಕೀಟಗಳ ನಿಯಂತ್ರಣ ಹೇಗೆ?"),
    ("Kannada - Dairy & Silage", "ಹೈನು ಹಸುಗಳಿಗೆ ಸೈಲೇಜ್ ತಯಾರಿಕೆ ಹೇಗೆ ಮಾಡಬೇಕು?"),
    ("Kannada - Transliterated", "Tomato yele haladi aagthide em madbeku?"),
    ("Kannada - Out of domain", "ಫ್ರಾನ್ಸ್ ದೇಶದ ರಾಜಧಾನಿ ಯಾವುದು?"),
    
    ("Telugu - Greeting", "నమస్కారం"),
    ("Telugu - Tomato Yellow Leaves", "టమోటా ఆకులు పసుపు రంగులోకి మారుతున్నాయి ఏమి చేయాలి?"),
    ("Telugu - Rice Agronomy", "వరి పంటకు ఎరువుల మోతాదు మరియు నీటి యాజమాన్యం ఎలా ఉండాలి?"),
    ("Telugu - Cotton Pink Bollworm", "పత్తిలో గులాబీ రంగు పురుగు నివారణ ఏమిటి?"),
    ("Telugu - Out of domain", "ఫ్రాన్స్ రాజధాని ఏమిటి?"),

    ("English - Greeting", "Hello, who are you?"),
    ("English - Precision Agriculture", "What is precision agriculture?"),
    ("English - Out of domain", "What is the capital of France?"),
]

print("=" * 80)
print("TESTING MULTILINGUAL TRILINGUAL PLATFORM (ENGLISH, TELUGU, KANNADA)")
print("=" * 80)

all_passed = True

for category, q in test_suite:
    res = handle_chat_query(q)
    ans = res["answer"]
    citations = res.get("citations", [])

    if "Out of domain" in category:
        passed = ("ಲಭ್ಯವಿಲ್ಲ" in ans or "లభించలేదు" in ans or "couldn't find" in ans)
    elif "Greeting" in category:
        passed = ("ನಮಸ್ಕಾರ" in ans or "నమస్కారం" in ans or "AgriSense" in ans or "Hello" in ans)
    else:
        passed = len(citations) > 0 and ("ಉತ್ತರ" in ans or "సమాధానం" in ans or "Answer" in ans)

    print(f"\n[{'✅ PASS' if passed else '❌ FAIL'}] {category}")
    print(f"  Query: {q}")
    print(f"  Citations: {len(citations)}")
    for c in citations[:2]:
        print(f"    • {c.get('source')} (Page {c.get('page')} - {c.get('topic')})")
    print(f"  Answer Snippet:\n  {ans[:160]}...")

    if not passed:
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("🎉 ALL ENGLISH, TELUGU & KANNADA TEST CASES PASSED 100%!")
else:
    print("❌ SOME TEST CASES FAILED")
print("=" * 80)
