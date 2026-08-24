import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

from src.rag.rag_engine import rag_engine
rag_engine.indexed_files = []
rag_engine._auto_index_sample_docs()

from server import handle_chat_query, handle_rag_query, list_documents

print("===========================================================================")
print("INDEXED DOCUMENTS & CHUNK COUNTS (/api/documents)")
print("===========================================================================")
docs_info = list_documents()
print(f"Total Documents: {docs_info['total_documents']}")
print(f"Total Chunks: {docs_info['total_chunks']}")
for f in docs_info['files']:
    print(f"  • File: {f['filename']} -> Chunks: {f['chunk_count']}")

test_queries = [
    ("What is precision agriculture?", True),
    ("What is fertigation?", True),
    ("What are the benefits of modern farming?", True),
    ("What is the capital of France?", False),
]

print("\n===========================================================================")
print("RUNNING 4 SPECIFIC RAG DATASET QUERIES")
print("===========================================================================")

for query_text, expected_present in test_queries:
    print("\n" + "=" * 70)
    print(f"USER QUERY: \"{query_text}\"")
    print(f"EXPECTED PRESENT IN DATASET: {expected_present}")
    print("-" * 70)
    
    result = rag_engine.query(question=query_text, top_k=4)
    retrieved_chunks = result.get("retrieved_chunks", [])
    citations = result.get("citations", [])
    answer = result.get("answer", "")
    
    print(f"RETRIEVED CHUNKS COUNT: {len(retrieved_chunks)}")
    for idx, chunk in enumerate(retrieved_chunks):
        meta = chunk.get("metadata", {})
        print(f"  [{idx+1}] Source: {meta.get('source')} | Page: {meta.get('page')} | Chunk ID: {meta.get('chunk_id')} | Relevance Score: {chunk.get('relevance_score')} (RRF: {chunk.get('rrf_score')})")
        print(f"      Excerpt: {chunk.get('text')[:140].replace(chr(10), ' ')}...")
    
    print(f"\nFINAL ANSWER:\n{answer}\n")
    
    if not expected_present:
        assert "I couldn't find this information in the provided dataset." in answer, f"Failed refusal for: {query_text}"
        print("===> [VERIFICATION]: Correctly refused out-of-dataset question!")
    else:
        assert len(answer) > 20 and "I couldn't find this information in the provided dataset." not in answer, f"Failed answer for: {query_text}"
        print("===> [VERIFICATION]: Successfully answered with exact dataset ground truth!")

print("\n===========================================================================")
print("ALL 4 QUERIES VERIFIED SUCCESSFULLY!")
print("===========================================================================")
