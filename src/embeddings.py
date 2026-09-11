"""
embeddings.py
-------------
Stage 3 of Naive RAG Pipeline: Vector Embeddings.
Converts text chunks and query strings into high-dimensional vector representations
using Ollama's local embedding model ('nomic-embed-text').
"""

from typing import List, Optional

# pyrefly: ignore [missing-import]
from src.config import settings
# pyrefly: ignore [missing-import]
from src.ollama_client import default_client

DEFAULT_EMBEDDING_MODEL = settings.EMBEDDING_MODEL


def get_embedding(text: str, model: Optional[str] = None) -> List[float]:
    """
    Computes a vector embedding for a single text string using nomic-embed-text.

    Args:
        text (str): The text content to embed.
        model (str, optional): The Ollama embedding model name.

    Returns:
        List[float]: A 768-dimensional float vector representation.
    """
    target_model = model or DEFAULT_EMBEDDING_MODEL
    return default_client.get_embedding(text, model=target_model)


def get_embeddings_batch(
    texts: List[str],
    model: Optional[str] = None,
    show_progress: bool = True
) -> List[List[float]]:
    """
    Generates embeddings for a batch of text strings.

    Args:
        texts (List[str]): List of strings to embed.
        model (str, optional): Ollama embedding model name.
        show_progress (bool): Whether to print progress information.

    Returns:
        List[List[float]]: List of vector embeddings.
    """
    target_model = model or DEFAULT_EMBEDDING_MODEL
    embeddings = []
    total = len(texts)

    for i, text in enumerate(texts, 1):
        if show_progress and (i == 1 or i % 5 == 0 or i == total):
            print(f"   [Embedding] Processing chunk {i}/{total}...")
        emb = get_embedding(text, model=target_model)
        embeddings.append(emb)

    return embeddings


if __name__ == "__main__":
    print("=" * 60)
    print("Stage 3: Local Embedding Generation Test")
    print("=" * 60)
    print(f"Target Model: {DEFAULT_EMBEDDING_MODEL}")
    
    sample_text = "How do I reset my forgotten PIN on the intranet portal?"
    print(f"Sample input: '{sample_text}'")
    
    vec = get_embedding(sample_text)
    print(f"Generated vector dimension: {len(vec)}")
    print(f"First 5 vector values: {[round(v, 4) for v in vec[:5]]}")
    print("Embeddings module is ready and functional!\n")
