"""
Text Splitter with Chunk Overlap and Metadata Preservation.
"""

from typing import List, Dict, Any
import re


class TextSplitter:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes raw document dictionaries and splits text into chunks with metadata.
        """
        chunks = []
        for doc in documents:
            text = doc.get("text", "")
            meta = doc.get("metadata", {})
            doc_chunks = self.split_text(text)

            for idx, c in enumerate(doc_chunks):
                chunk_meta = meta.copy()
                chunk_meta["chunk_id"] = f"{meta.get('source', 'doc')}_p{meta.get('page', 1)}_c{idx+1}"
                chunk_meta["chunk_index"] = idx + 1
                chunks.append({"text": c, "metadata": chunk_meta})
        return chunks

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []

        # Split on paragraph or double newlines first
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunks = []
        current = ""

        for p in paragraphs:
            if len(current) + len(p) <= self.chunk_size:
                current = f"{current}\n\n{p}".strip()
            else:
                if current:
                    chunks.append(current)
                if len(p) > self.chunk_size:
                    # Break long paragraph by sentences
                    sentences = re.split(r"(?<=[.!?])\s+", p)
                    sub = ""
                    for s in sentences:
                        if len(sub) + len(s) <= self.chunk_size:
                            sub = f"{sub} {s}".strip()
                        else:
                            if sub:
                                chunks.append(sub)
                            sub = s
                    if sub:
                        chunks.append(sub)
                    current = ""
                else:
                    current = p

        if current:
            chunks.append(current)

        return chunks if chunks else [text]
