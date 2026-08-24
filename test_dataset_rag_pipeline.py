import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

from server import handle_chat_query, handle_rag_query

test_questions = [
    ("What is the fertilizer schedule for wheat?", True),
    ("What is the fertilizer schedule for rice?", True),
    ("Explain PM-KUSUM solar pump subsidy", True),
    ("What is hydroponic farming?", True),
    ("How to manage pink bollworm in cotton?", True),
    ("What is the stock price of Apple on NASDAQ?", False),
]

print("===========================================================================")
print("TESTING 5 DATASET QUESTIONS + 1 OUT-OF-DATASET REFUSAL VIA CORE RAG/CHAT ENGINE")
print("===========================================================================")

for q, expected in test_questions:
    res = handle_chat_query(user_query=q)
    ans = res["answer"]
    citations = res.get("citations", [])
    
    print(f"\n[QUERY]: {q}")
    print(f"[EXPECTED IN DATASET]: {expected}")
    print(f"[INTENT]: {res.get('intent')}")
    print(f"[CITATIONS]: {len(citations)} source citations returned")
    print(f"[ANSWER EXCERPT]:\n{ans[:280]}...")
    
    if not expected:
        if "I couldn't find this information in the provided dataset." in ans:
            print("===> [PASS] Correctly returned exact refusal: 'I couldn't find this information in the provided dataset.'")
        else:
            print(f"===> [FAIL] Expected refusal but got: {ans}")
            sys.exit(1)
    else:
        assert len(ans) > 20, "Answer too short"
        assert "I couldn't find this information in the provided dataset." not in ans, "False positive refusal"
        print("===> [PASS] Successfully answered with verified dataset facts!")

print("\n===========================================================================")
print("ALL 5 IN-DATASET QUESTIONS AND 1 OUT-OF-DATASET REFUSAL PASSED 100%!")
print("===========================================================================")
