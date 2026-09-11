"""
Source package for 04_PP_CHHORN_VECHEY Naive RAG application.
"""

# pyrefly: ignore [missing-import]
from src.config import settings
# pyrefly: ignore [missing-import]
from src.ollama_client import OllamaClient, default_client
# pyrefly: ignore [missing-import]
from src.ingestion import load_documents
# pyrefly: ignore [missing-import]
from src.chunking import (
    split_text_recursive,
    split_text_fixed,
    chunk_document,
    chunk_all_documents,
)
# pyrefly: ignore [missing-import]
from src.embeddings import get_embedding, get_embeddings_batch
# pyrefly: ignore [missing-import]
from src.vector_store import (
    get_chroma_client,
    get_or_create_collection,
    add_chunks_to_vector_store,
    query_vector_store,
    count_documents,
)
# pyrefly: ignore [missing-import]
from src.retriever import Retriever, retrieve_chunks, get_default_retriever
# pyrefly: ignore [missing-import]
from src.generator import generate_answer, format_context
# pyrefly: ignore [missing-import]
from src.pipeline import RAGPipeline, setup_rag_system, query_rag

__version__ = "1.0.0"

__all__ = [
    "settings",
    "OllamaClient",
    "default_client",
    "load_documents",
    "split_text_recursive",
    "split_text_fixed",
    "chunk_document",
    "chunk_all_documents",
    "get_embedding",
    "get_embeddings_batch",
    "get_chroma_client",
    "get_or_create_collection",
    "add_chunks_to_vector_store",
    "query_vector_store",
    "count_documents",
    "Retriever",
    "retrieve_chunks",
    "get_default_retriever",
    "generate_answer",
    "format_context",
    "RAGPipeline",
    "setup_rag_system",
    "query_rag",
]
