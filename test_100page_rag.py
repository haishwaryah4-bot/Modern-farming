import sys
sys.stdout.reconfigure(encoding='utf-8')

from server import handle_chat_query

questions = [
    ("What is Kharif season?", True),
    ("What is soil testing?", True),
    ("How should irrigation be managed?", True),
    ("What are the important crop growth stages?", True),
    ("What precautions are recommended in farming?", True),
    ("How can modern technology help farmers?", True),
    ("What is the capital of France?", False),
]

all_passed = True
print("=" * 80)
print("VERIFYING 100-PAGE FARMING DATASET RAG PIPELINE")
print("=" * 80)

for q, expected_in_kb in questions:
    res = handle_chat_query(user_query=q)
    ans = res["answer"]
    citations = res.get("citations", [])
    refused = "I couldn't find this information in the provided dataset." in ans
    
    print("\n" + "-" * 70)
    print(f"QUERY: {q}")
    print(f"EXPECTED IN DATASET: {expected_in_kb}")
    print(f"RETRIEVED CITATIONS: {len(citations)}")
    for c in citations[:2]:
        print(f"  - Source: {c.get('source')} | Page: {c.get('page')} | Topic: {c.get('topic')}")
    print(f"REFUSED: {refused}")
    print(f"ANSWER EXCERPT:\n{ans[:300]}...")
    
    if expected_in_kb and refused:
        print("❌ FAILED: In-domain question was refused!")
        all_passed = False
    elif not expected_in_kb and not refused:
        print("❌ FAILED: Out-of-domain question was NOT refused!")
        all_passed = False
    else:
        print("✅ PASSED")

print("\n" + "=" * 80)
if all_passed:
    print("🌟 ALL 7 TESTS PASSED ACCORDING TO 100-PAGE RAG ARCHITECTURE SPECIFICATION!")
else:
    print("❌ SOME TESTS FAILED")
print("=" * 80)
