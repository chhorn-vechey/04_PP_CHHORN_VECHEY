"""
chunking.py
-----------
Stage 2 of Naive RAG Pipeline: Text Splitting / Chunking.
Splits loaded documents into smaller, semantically coherent chunks with overlap.

Strategy Used:
    - Recursive / Paragraph-aware Splitting with Overlap (Primary):
      Splits on natural boundaries (double newlines, single newlines, sentences)
      to avoid cutting sentences or numbered steps in half.
    - Fixed-size Character Chunking (Secondary / Comparison):
      Splits purely by character length with fixed sliding overlap.
"""

from typing import List, Dict, Any, Optional

# pyrefly: ignore [missing-import]
from src.config import settings


def split_text_recursive(
    text: str,
    chunk_size: int = settings.CHUNK_SIZE,
    chunk_overlap: int = settings.CHUNK_OVERLAP,
    separators: Optional[List[str]] = None
) -> List[str]:
    """
    Splits text recursively by trying higher-level delimiters first
    (\\n\\n, \\n, '. ', ' ') to preserve semantic coherence.

    Args:
        text (str): Input text string.
        chunk_size (int): Maximum target character length for each chunk.
        chunk_overlap (int): Number of characters to overlap between consecutive chunks.
        separators (Optional[List[str]]): List of separators to try in order.

    Returns:
        List[str]: List of text chunk strings.
    """
    if separators is None:
        separators = ["\n\n", "\n", ". ", " "]

    chunks = []
    
    # Base case: text is already within target size
    if len(text) <= chunk_size:
        cleaned = text.strip()
        return [cleaned] if cleaned else []

    # Find the first separator present in text
    chosen_sep = None
    for sep in separators:
        if sep in text:
            chosen_sep = sep
            break

    # If no separator found, do hard character slice
    if chosen_sep is None:
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += max(1, chunk_size - chunk_overlap)
        return chunks

    # Split using the chosen separator
    splits = text.split(chosen_sep)
    current_chunk = ""
    next_separators = separators[separators.index(chosen_sep) + 1:]

    for split in splits:
        candidate = f"{current_chunk}{chosen_sep}{split}" if current_chunk else split
        
        if len(candidate) <= chunk_size:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                
                # Create overlap buffer from the end of current_chunk, snapping to word boundary
                if chunk_overlap > 0 and len(current_chunk) > chunk_overlap:
                    raw_overlap = current_chunk[-chunk_overlap:]
                    first_space = raw_overlap.find(" ")
                    if first_space != -1 and first_space < len(raw_overlap) - 1:
                        overlap_seed = raw_overlap[first_space + 1:].strip()
                    else:
                        overlap_seed = raw_overlap.strip()
                    current_chunk = f"{overlap_seed}{chosen_sep}{split}" if overlap_seed else split
                else:
                    current_chunk = split
            else:
                # Individual segment is longer than chunk_size, recurse with finer separators
                if next_separators:
                    sub_chunks = split_text_recursive(split, chunk_size, chunk_overlap, next_separators)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(split.strip())
                current_chunk = ""

    if current_chunk and current_chunk.strip():
        chunks.append(current_chunk.strip())

    return [c for c in chunks if c]


def split_text_fixed(
    text: str,
    chunk_size: int = 400,
    chunk_overlap: int = 50
) -> List[str]:
    """
    Alternative simple fixed-size character chunking with sliding window.
    Provided for comparison (Bonus Challenge).
    """
    chunks = []
    start = 0
    step = max(1, chunk_size - chunk_overlap)

    while start < len(text):
        end = min(start + chunk_size, len(text))
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end == len(text):
            break
        start += step

    return chunks


def chunk_document(
    doc: Dict[str, Any],
    chunk_size: int = settings.CHUNK_SIZE,
    chunk_overlap: int = settings.CHUNK_OVERLAP,
    strategy: str = "recursive"
) -> List[Dict[str, Any]]:
    """
    Takes a single document dict from ingestion and returns structured chunk dictionaries.

    Args:
        doc (Dict[str, Any]): Loaded document dict from ingestion.py.
        chunk_size (int): Target maximum characters per chunk.
        chunk_overlap (int): Overlap character count.
        strategy (str): 'recursive' or 'fixed'.

    Returns:
        List[Dict[str, Any]]: Chunks with unique IDs and metadata.
    """
    content = doc["content"]
    doc_id = doc["doc_id"]
    filename = doc["filename"]

    if strategy == "fixed":
        raw_chunks = split_text_fixed(content, chunk_size, chunk_overlap)
    else:
        raw_chunks = split_text_recursive(content, chunk_size, chunk_overlap)

    chunk_objects = []
    for idx, raw_text in enumerate(raw_chunks):
        chunk_id = f"{filename}#c{idx:02d}"
        chunk_objects.append({
            "chunk_id": chunk_id,
            "text": raw_text,
            "metadata": {
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "filename": filename,
                "chunk_index": idx,
                "strategy": strategy,
                "char_count": len(raw_text)
            }
        })

    return chunk_objects


def chunk_all_documents(
    documents: List[Dict[str, Any]],
    chunk_size: int = settings.CHUNK_SIZE,
    chunk_overlap: int = settings.CHUNK_OVERLAP,
    strategy: str = "recursive"
) -> List[Dict[str, Any]]:
    """
    Chunks an entire list of loaded documents.
    """
    return [
        chunk
        for doc in documents
        for chunk in chunk_document(doc, chunk_size=chunk_size, chunk_overlap=chunk_overlap, strategy=strategy)
    ]


if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    from src.ingestion import load_documents

    print("=" * 60)
    print("Stage 2: Chunking & Text Splitting Test")
    print("=" * 60)

    docs = load_documents(settings.DATA_DIR)
    recursive_chunks = chunk_all_documents(docs, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP, strategy="recursive")
    fixed_chunks = chunk_all_documents(docs, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP, strategy="fixed")

    print(f"Total documents: {len(docs)}")
    print(f"Strategy: Recursive Paragraph-Aware  -> Generated {len(recursive_chunks)} chunks")
    print(f"Strategy: Fixed Character Slicing    -> Generated {len(fixed_chunks)} chunks\n")

    print("Sample Chunks (Recursive Strategy):")
    for c in recursive_chunks[:3]:
        print(f" - [{c['chunk_id']}] ({c['metadata']['char_count']} chars):")
        print(f"   {c['text'][:140]}...\n")
