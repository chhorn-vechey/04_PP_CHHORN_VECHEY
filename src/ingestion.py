"""
ingestion.py
------------
Stage 1 of Naive RAG Pipeline: Ingestion.
Loads raw text documents (.txt and .md) from the specified data directory.
"""

import os
from typing import List, Dict, Any

# pyrefly: ignore [missing-import]
from src.config import settings


def load_documents(data_dir: str = settings.DATA_DIR) -> List[Dict[str, Any]]:
    """
    Scans the given directory and loads all .txt and .md documents.

    Args:
        data_dir (str): Path to the directory containing documents.

    Returns:
        List[Dict[str, Any]]: A list of document dictionaries, each containing:
            - 'doc_id': Unique identifier (filename)
            - 'filename': Name of the file
            - 'content': Full text content of the document
            - 'metadata': Metadata dictionary with file path, character length, etc.
    """
    documents = []

    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")

    supported_extensions = (".txt", ".md")
    files = sorted(os.listdir(data_dir))

    for file_name in files:
        if file_name.lower().endswith(supported_extensions):
            file_path = os.path.join(data_dir, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                if not content:
                    print(f"[Warning] Skipping empty file: {file_name}")
                    continue

                doc_entry = {
                    "doc_id": file_name,
                    "filename": file_name,
                    "content": content,
                    "metadata": {
                        "source": file_path,
                        "filename": file_name,
                        "char_count": len(content),
                        "word_count": len(content.split())
                    }
                }
                documents.append(doc_entry)
            except Exception as e:
                print(f"[Error] Failed to read {file_path}: {e}")

    return documents


if __name__ == "__main__":
    print("=" * 60)
    print("Stage 1: Document Ingestion Test")
    print("=" * 60)
    
    docs = load_documents(settings.DATA_DIR)
    print(f"Successfully loaded {len(docs)} document(s) from '{settings.DATA_DIR}':\n")
    
    for idx, doc in enumerate(docs, 1):
        meta = doc["metadata"]
        print(f"{idx}. Filename: {doc['filename']}")
        print(f"   Character Count: {meta['char_count']}")
        print(f"   Word Count     : {meta['word_count']}")
        preview = doc['content'][:120].replace('\n', ' ')
        print(f"   Snippet        : {preview}...\n")
