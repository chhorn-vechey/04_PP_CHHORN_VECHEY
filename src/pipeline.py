"""
pipeline.py
-----------
Stage 7 of Naive RAG Pipeline: Pipeline Orchestrator.
Connects the offline pipeline (Ingest -> Chunk -> Embed -> Store) and the
online pipeline (Question -> Retrieve -> Generate -> Grounded Answer).
"""

from typing import Dict, Any, Optional

# pyrefly: ignore [missing-import]
from src.config import settings
# pyrefly: ignore [missing-import]
from src.ingestion import load_documents
# pyrefly: ignore [missing-import]
from src.chunking import chunk_all_documents
# pyrefly: ignore [missing-import]
from src.embeddings import get_embeddings_batch
# pyrefly: ignore [missing-import]
from src.vector_store import (
    get_or_create_collection,
    add_chunks_to_vector_store,
    count_documents,
    reset_collection
)
# pyrefly: ignore [missing-import]
from src.retriever import Retriever, get_default_retriever
# pyrefly: ignore [missing-import]
from src.generator import generate_answer


def setup_rag_system(
    data_dir: str = settings.DATA_DIR,
    force_reindex: bool = False,
    chunk_size: int = settings.CHUNK_SIZE,
    chunk_overlap: int = settings.CHUNK_OVERLAP
) -> int:
    """
    Ensures the vector database is populated with chunks and embeddings from the data directory.

    Args:
        data_dir (str): Folder containing raw documents.
        force_reindex (bool): If True, clears existing DB and re-indexes all files.
        chunk_size (int): Max characters per chunk.
        chunk_overlap (int): Overlap characters.

    Returns:
        int: Total number of chunks in the database.
    """
    collection = get_or_create_collection()
    existing_count = count_documents(collection)

    if existing_count > 0 and not force_reindex:
        return existing_count

    if force_reindex and existing_count > 0:
        print("[Pipeline] Re-indexing requested. Resetting vector database...")
        collection = reset_collection()

    print("[Pipeline] Setting up offline RAG pipeline...")
    # 1. Ingest
    documents = load_documents(data_dir)
    if not documents:
        print(f"[Pipeline Warning] No documents found in '{data_dir}'.")
        return 0

    print(f"[Pipeline] Loaded {len(documents)} document(s) from '{data_dir}'.")

    # 2. Chunk
    chunks = chunk_all_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        strategy="recursive"
    )
    print(f"[Pipeline] Created {len(chunks)} text chunks.")

    # 3. Embed
    texts = [c["text"] for c in chunks]
    print(f"[Pipeline] Generating vector embeddings using Ollama 'nomic-embed-text'...")
    vectors = get_embeddings_batch(texts)

    # 4. Store
    add_chunks_to_vector_store(collection, chunks, vectors)
    total_stored = count_documents(collection)
    print(f"[Pipeline] Offline setup complete. {total_stored} chunks indexed.")
    return total_stored


class RAGPipeline:
    """
    End-to-end RAG system exposing an easy-to-use query interface.
    """

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or settings.DATA_DIR
        setup_rag_system(data_dir=self.data_dir)
        self.retriever = get_default_retriever()

    def query(self, question: str, top_k: int = settings.DEFAULT_TOP_K) -> Dict[str, Any]:
        """
        Executes the online RAG pipeline:
        1. Query -> Retriever -> Relevant chunks
        2. Chunks + Question -> Generator -> Grounded answer

        Returns:
            Dict[str, Any] containing 'question', 'answer', and 'retrieved_chunks'.
        """
        clean_question = question.strip()
        if not clean_question:
            return {
                "question": question,
                "answer": "Please provide a valid question.",
                "retrieved_chunks": []
            }

        # Step 1: Retrieve relevant chunks
        chunks = self.retriever.retrieve(clean_question, top_k=top_k)

        # Step 2: Generate grounded answer
        answer = generate_answer(clean_question, chunks)

        return {
            "question": clean_question,
            "answer": answer,
            "retrieved_chunks": chunks
        }


# Global pipeline instance
_default_pipeline: Optional[RAGPipeline] = None


def get_pipeline(data_dir: Optional[str] = None) -> RAGPipeline:
    global _default_pipeline
    if _default_pipeline is None:
        _default_pipeline = RAGPipeline(data_dir=data_dir or settings.DATA_DIR)
    return _default_pipeline


def query_rag(question: str, top_k: int = settings.DEFAULT_TOP_K) -> Dict[str, Any]:
    """
    Convenience function to query the RAG pipeline.
    """
    pipe = get_pipeline()
    return pipe.query(question, top_k=top_k)


if __name__ == "__main__":
    print("=" * 60)
    print("Stage 7: End-to-End Pipeline Test")
    print("=" * 60)

    test_q = "How do I connect to the company VPN and what is the server address?"
    print(f"User Query: {test_q}\n")

    result = query_rag(test_q)
    
    print("-" * 60)
    print(f"Retrieved Chunks Count: {len(result['retrieved_chunks'])}")
    for i, c in enumerate(result["retrieved_chunks"], 1):
        print(f"  [Chunk {i}] ID: {c['chunk_id']} | Sim: {c['similarity']}")
    print("-" * 60)
    print("Generated Grounded Answer:")
    print(result["answer"])
    print("=" * 60)
