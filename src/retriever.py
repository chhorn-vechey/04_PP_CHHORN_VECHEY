"""
retriever.py
------------
Stage 5 of Naive RAG Pipeline: Retriever.
Takes a user question, computes its semantic embedding, and queries the persistent
vector database (ChromaDB) to retrieve the top-k most relevant chunks.
"""

from typing import List, Dict, Any, Optional

# pyrefly: ignore [missing-import]
from src.config import settings
# pyrefly: ignore [missing-import]
from src.embeddings import get_embedding
# pyrefly: ignore [missing-import]
from src.vector_store import get_or_create_collection, query_vector_store


class Retriever:
    """
    Handles query embedding and vector database lookup.
    """

    def __init__(
        self,
        collection_name: Optional[str] = None,
        persist_directory: Optional[str] = None
    ):
        target_collection = collection_name or settings.COLLECTION_NAME
        target_dir = persist_directory or settings.CHROMA_DIR
        self.collection = get_or_create_collection(
            collection_name=target_collection,
            persist_directory=target_dir
        )

    def retrieve(
        self,
        query: str,
        top_k: int = settings.DEFAULT_TOP_K,
        min_similarity: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Embeds the query and fetches the top-k nearest chunks from ChromaDB.

        Args:
            query (str): The user's question or search query.
            top_k (int): Number of chunks to retrieve.
            min_similarity (float, optional): If set, filters out chunks below this similarity.

        Returns:
            List[Dict[str, Any]]: List of matching chunk objects.
        """
        if not query or not query.strip():
            return []

        # Step 1: Turn query into embedding vector
        query_vector = get_embedding(query.strip())

        # Step 2: Query ChromaDB
        results = query_vector_store(self.collection, query_vector, top_k=top_k)

        # Step 3: Optional score filtering
        if min_similarity is not None:
            results = [r for r in results if r["similarity"] >= min_similarity]

        return results


# Global retriever instance helper for convenience
_default_retriever: Optional[Retriever] = None


def get_default_retriever() -> Retriever:
    global _default_retriever
    if _default_retriever is None:
        _default_retriever = Retriever()
    return _default_retriever


def retrieve_chunks(
    query: str,
    top_k: int = settings.DEFAULT_TOP_K,
    min_similarity: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Convenience function to retrieve chunks using the default retriever.
    """
    retriever = get_default_retriever()
    return retriever.retrieve(query, top_k=top_k, min_similarity=min_similarity)


if __name__ == "__main__":
    print("=" * 60)
    print("Stage 5: Retriever Test")
    print("=" * 60)

    test_query = "What are the server settings for company email?"
    print(f"Query: '{test_query}'\n")

    chunks = retrieve_chunks(test_query)
    for i, c in enumerate(chunks, 1):
        print(f"[{i}] Chunk: {c['chunk_id']} | Similarity: {c['similarity']}")
        print(f"    Source: {c['metadata']['filename']}")
        print(f"    Preview: {c['text'][:120]}...\n")
