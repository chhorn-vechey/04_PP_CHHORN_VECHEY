"""
config.py
---------
Centralized configuration management for RAG Fundamentals Homework.
Supports overrides via environment variables.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Ollama Local Service Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2")

    # ChromaDB Vector Database Configuration
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "./chroma_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "homework_docs")

    # Chunking Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "450"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "60"))

    # RAG Generation & Guardrails
    RELEVANCE_THRESHOLD: float = float(os.getenv("RELEVANCE_THRESHOLD", "0.40"))
    DEFAULT_TOP_K: int = int(os.getenv("DEFAULT_TOP_K", "3"))

    # Document Directory
    DATA_DIR: str = os.getenv("DATA_DIR", "data/raw")


# Global singleton settings instance
settings = Settings()
