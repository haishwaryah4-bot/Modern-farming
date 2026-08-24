import sys
sys.stdout.reconfigure(encoding='utf-8')

from server import handle_chat_query

test_cases = [
    ("Modern Farming Technologies", "What is precision agriculture?"),
    ("Farming Procedures", "What are the standard farming procedures for land preparation?"),
    ("Irrigation", "How should irrigation be managed?"),
    ("Fertilization", "What is automated fertigation?"),
    ("Pest and Disease Management", "What is integrated pest management?"),
    ("Crop Management", "What are the important crop growth stages?"),
    ("Livestock Farming", "What are the best practices for dairy cattle and livestock farming?"),
    ("Sustainability", "How does sustainable farming improve soil carbon?"),
    ("Farming Equipment", "What modern farming equipment and machinery are used?"),
    ("Seasonal Activities", "What is Kharif season?"),
    ("Out-of-Domain Guardrail", "What is the capital of France?"),
]

print("=" * 80)
print("TESTING ALL 10 REQUIRED MODERN FARMING RAG DOMAINS")
print("=" * 80)

all_passed = True
for domain, q in test_cases:
    res = handle_chat_query(q)
    ans = res["answer"]
    citations = res.get("citations", [])
    is_refusal = "I couldn't find this information in the provided dataset." in ans
    
    if domain == "Out-of-Domain Guardrail":
        passed = is_refusal
    else:
        passed = not is_refusal and len(citations) > 0

    print(f"\n[{'✅ PASS' if passed else '❌ FAIL'}] Domain: {domain}")
    print(f"  Question: {q}")
    print(f"  Citations: {len(citations)}")
    for c in citations[:2]:
        print(f"    • {c.get('source')} (Page {c.get('page')} - {c.get('topic')})")
    
    if not passed:
        all_passed = False
        print(f"  Answer snippet: {ans[:150]}...")

print("\n" + "=" * 80)
if all_passed:
    print("🎉 ALL 10 REQUIRED FARMING DOMAINS + OUT-OF-DOMAIN GUARDRAILS VERIFIED 100% PASSING!")
else:
    print("❌ SOME DOMAIN TESTS FAILED")
print("=" * 80)
