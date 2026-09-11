"""
generator.py
------------
Stage 6 of Naive RAG Pipeline: Generator.
Builds a grounded prompt combining retrieved context chunks and the user's question,
sends it to the local LLM (Ollama 'llama3.2'), and returns the grounded answer.

Features:
- Strict hallucination prevention (answers ONLY using provided context).
- Bonus check: If context is irrelevant or empty, returns "I could not find this in your documents."
"""

from typing import List, Dict, Any, Optional

# pyrefly: ignore [missing-import]
from src.config import settings
# pyrefly: ignore [missing-import]
from src.ollama_client import default_client

DEFAULT_LLM_MODEL = settings.LLM_MODEL
RELEVANCE_THRESHOLD = settings.RELEVANCE_THRESHOLD


def format_context(retrieved_chunks: List[Dict[str, Any]]) -> str:
    """
    Formats retrieved chunks into a clean, labeled context block.
    """
    if not retrieved_chunks:
        return "No relevant context found."

    context_parts = []
    for idx, chunk in enumerate(retrieved_chunks, 1):
        filename = chunk.get("metadata", {}).get("filename", "document")
        chunk_id = chunk.get("chunk_id", f"chunk_{idx}")
        text = chunk.get("text", "").strip()
        context_parts.append(f"[Document Excerpt #{idx} | Source: {filename} | ID: {chunk_id}]\n{text}")

    return "\n\n".join(context_parts)


def call_llm(
    prompt: str,
    system_prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.1
) -> str:
    """
    Calls the local Ollama LLM with a system and user prompt.
    """
    target_model = model or DEFAULT_LLM_MODEL
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    return default_client.chat_completion(messages, model=target_model, temperature=temperature)


def generate_answer(
    query: str,
    retrieved_chunks: List[Dict[str, Any]],
    model: Optional[str] = None,
    strict_check: bool = True
) -> str:
    """
    Generates an answer grounded strictly in the retrieved chunks.

    Args:
        query (str): The user question.
        retrieved_chunks (List[Dict[str, Any]]): Retrieved chunks from vector search.
        model (str, optional): Ollama LLM model name (default from settings).
        strict_check (bool): If True, validates similarity scores before calling LLM.

    Returns:
        str: Grounded answer from the model.
    """
    target_model = model or DEFAULT_LLM_MODEL

    # Bonus Challenge: Check if retrieved chunks are relevant enough
    if strict_check:
        if not retrieved_chunks:
            return "I could not find this in your documents."
        
        max_sim = max((c.get("similarity", 0.0) for c in retrieved_chunks), default=0.0)
        if max_sim < RELEVANCE_THRESHOLD:
            return "I could not find this in your documents."

    formatted_context = format_context(retrieved_chunks)

    system_prompt = (
        "You are an accurate, grounded technical assistant. "
        "Your task is to answer the user's question based strictly and exclusively on the "
        "provided document excerpts. "
        "\nSTRICT RULES:\n"
        "1. Answer ONLY using the facts directly stated in the context excerpts below.\n"
        "2. Do NOT use outside knowledge, speculate, or make assumptions.\n"
        "3. If the context does not contain the answer, or if the question cannot be answered "
        "from the excerpts, you MUST answer: 'I could not find this in your documents.'\n"
        "4. Keep your answer concise, clear, and faithful to the documents."
    )

    user_prompt = (
        f"Context from documents:\n"
        f"---------------------\n"
        f"{formatted_context}\n"
        f"---------------------\n\n"
        f"Question: {query}\n\n"
        f"Grounded Answer:"
    )

    answer = call_llm(user_prompt, system_prompt, model=target_model)
    return answer


if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    from src.retriever import retrieve_chunks

    print("=" * 60)
    print("Stage 6: Grounded Generator Test")
    print("=" * 60)

    # Test 1: In-document question
    q1 = "What are the requirements for setting a new PIN?"
    print(f"\nQuestion 1: '{q1}'")
    chunks1 = retrieve_chunks(q1)
    ans1 = generate_answer(q1, chunks1)
    print(f"Answer 1:\n{ans1}\n")

    # Test 2: Out-of-document question
    q2 = "What is the capital of France?"
    print(f"Question 2: '{q2}' (Out of domain)")
    chunks2 = retrieve_chunks(q2)
    ans2 = generate_answer(q2, chunks2)
    print(f"Answer 2:\n{ans2}\n")
