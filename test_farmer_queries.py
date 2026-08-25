import sys
sys.stdout.reconfigure(encoding='utf-8')

from server import handle_chat_query

test_queries = [
    "what is wheat fertilizer schedule?",
    "tomato leaf curl disease treatment",
    "how to grow rice?",
    "what is drip irrigation?",
    "how much subsidy for solar pump?",
    "cotton pink bollworm control",
    "paddy fertilizer schedule",
    "tell me about modern farming",
    "rice npk ratio",
    "chilli thrips control",
    "What is precision agriculture?",
    "What is fertigation?",
    "What are the benefits of modern farming?"
]

for q in test_queries:
    res = handle_chat_query(user_query=q)
    ans = res["answer"]
    is_refused = "I couldn't find this information in the provided dataset." in ans
    print("=" * 60)
    print(f"QUERY: {q}")
    print(f"REFUSED: {is_refused}")
    print(f"ANSWER:\n{ans[:200]}...")
    if is_refused:
        print(f"WARNING: '{q}' was refused unexpectedly!")
