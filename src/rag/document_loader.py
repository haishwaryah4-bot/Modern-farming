"""
Multi-Format Document Loader.
Extracts text and metadata from PDF, DOCX, TXT, and CSV files.
"""

import os
import csv
from typing import List, Dict, Any
from pathlib import Path


class DocumentLoader:
    @staticmethod
    def load_file(file_path: str, default_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Load document and return list of page/record dictionaries:
        [{'text': str, 'metadata': {'source': str, 'page': int, 'crop': str, ...}}]
        """
        path = Path(file_path)
        if not path.exists():
            return []

        ext = path.suffix.lower()
        meta = default_metadata.copy() if default_metadata else {}
        meta["source"] = path.name
        meta["file_path"] = str(path)

        if ext == ".txt":
            return DocumentLoader._load_txt(path, meta)
        elif ext in [".csv", ".tsv"]:
            return DocumentLoader._load_csv(path, meta)
        elif ext in [".xlsx", ".xls"]:
            return DocumentLoader._load_excel(path, meta)
        elif ext == ".pdf":
            return DocumentLoader._load_pdf(path, meta)
        elif ext in [".docx", ".doc"]:
            return DocumentLoader._load_docx(path, meta)
        else:
            return DocumentLoader._load_txt(path, meta)

    @staticmethod
    def _load_txt(path: Path, meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Check if file has multi-page markers like --- [PAGE X] ---
            import re
            if "--- [PAGE" in content:
                page_blocks = re.split(r"--- \[PAGE\s*(\d+)\] ---", content)
                docs = []
                # First element before first page marker may be empty
                i = 1
                while i < len(page_blocks):
                    page_num = int(page_blocks[i])
                    page_text = page_blocks[i + 1].strip()
                    
                    p_meta = meta.copy()
                    p_meta["page"] = page_num
                    p_meta["topic"] = DocumentLoader._extract_field(page_text, "Topic") or "General Agronomy"
                    p_meta["crop"] = DocumentLoader._extract_field(page_text, "Crop") or "General"
                    p_meta["season"] = DocumentLoader._extract_field(page_text, "Season") or "All Seasons"
                    p_meta["region"] = DocumentLoader._extract_field(page_text, "Region") or "Pan-India"
                    p_meta["doc_type"] = DocumentLoader._extract_field(page_text, "Category") or "Agronomic Dataset"
                    p_meta["source"] = "Farming Dataset"

                    # Strip metadata headers from text body so chunks contain pure agronomic guidance
                    clean_body_lines = []
                    for l in page_text.split("\n"):
                        if any(l.strip().startswith(k) for k in ["Document:", "Page:", "Topic:", "Crop:", "Season:", "Region:", "Category:"]):
                            continue
                        clean_body_lines.append(l)
                    cleaned_body = "\n".join(clean_body_lines).strip()

                    docs.append({"text": cleaned_body or page_text, "metadata": p_meta})
                    i += 2
                return docs

            # Extract header metadata if single document
            crop = DocumentLoader._extract_field(content, "Crop")
            geography = DocumentLoader._extract_field(content, "Geography")
            doc_type = DocumentLoader._extract_field(content, "Category")
            year = DocumentLoader._extract_field(content, "Year")

            item_meta = meta.copy()
            if crop: item_meta["crop"] = crop
            if geography: item_meta["geography"] = geography
            if doc_type: item_meta["doc_type"] = doc_type
            if year: item_meta["year"] = year
            item_meta["page"] = 1

            clean_body_lines = []
            for l in content.split("\n"):
                if any(l.strip().startswith(k) for k in ["Title:", "Category:", "Crop:", "Geography:", "Year:", "Language:", "Author:"]):
                    continue
                clean_body_lines.append(l)
            cleaned_content = "\n".join(clean_body_lines).strip()

            return [{"text": cleaned_content or content, "metadata": item_meta}]
        except Exception:
            return []

    @staticmethod
    def _load_csv(path: Path, meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        docs = []
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader):
                    row_text = " | ".join([f"{k}: {v}" for k, v in row.items() if v])
                    row_meta = meta.copy()
                    row_meta["page"] = idx + 1
                    row_meta["doc_type"] = row.get("Category", "Data Table")
                    row_meta["crop"] = row.get("Crop", "General")
                    row_meta["geography"] = row.get("Geography", "Pan-India")
                    row_meta["year"] = row.get("Year", "2024")
                    docs.append({"text": row_text, "metadata": row_meta})
        except Exception:
            pass
        return docs

    @staticmethod
    def _load_excel(path: Path, meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        docs = []
        try:
            import pandas as pd
            excel_file = pd.ExcelFile(str(path))
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                for idx, row in df.iterrows():
                    row_dict = row.dropna().to_dict()
                    row_text = f"Sheet: {sheet_name} | " + " | ".join([f"{k}: {v}" for k, v in row_dict.items()])
                    row_meta = meta.copy()
                    row_meta["page"] = idx + 1
                    row_meta["section"] = sheet_name
                    row_meta["doc_type"] = "Excel Data Table"
                    docs.append({"text": row_text, "metadata": row_meta})
        except Exception:
            pass
        return docs

    @staticmethod
    def _load_pdf(path: Path, meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        docs = []
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    page_meta = meta.copy()
                    page_meta["page"] = idx + 1
                    docs.append({"text": text, "metadata": page_meta})
        except Exception:
            # Fallback if binary read
            with open(path, "rb") as f:
                raw = f.read().decode("latin1", errors="ignore")
                docs.append({"text": raw[:4000], "metadata": {**meta, "page": 1}})
        return docs

    @staticmethod
    def _load_docx(path: Path, meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        docs = []
        try:
            import docx
            doc = docx.Document(str(path))
            full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            docs.append({"text": full_text, "metadata": {**meta, "page": 1}})
        except Exception:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                docs.append({"text": f.read(), "metadata": {**meta, "page": 1}})
        return docs

    @staticmethod
    def _extract_field(text: str, field_name: str) -> str:
        import re
        m = re.search(rf"^{field_name}:\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
        return m.group(1).strip() if m else ""
