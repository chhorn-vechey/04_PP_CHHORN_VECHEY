"""
main.py
-------
Stage 8: Interactive Terminal Chat Interface for Baseline Naive RAG App.
Runs an interactive conversation loop in the terminal:
- Accepts user questions
- Retrieves grounded chunks from ChromaDB
- Prints retrieved chunk sources & similarity scores (Bonus Challenge)
- Generates answer strictly grounded in documents via Ollama 'llama3.2'
- Lets user type 'exit' or 'quit' to end session
"""

from src.config import settings
from src.pipeline import RAGPipeline, setup_rag_system


def print_banner():
    banner = f"""
================================================================================
          RAG FUNDAMENTALS - CHAT WITH DOCUMENTS (WEEK 5 HOMEWORK)
================================================================================
 Model (LLM)      : {settings.LLM_MODEL} (Local via Ollama)
 Embedding Model  : {settings.EMBEDDING_MODEL} (Local via Ollama)
 Vector Database  : ChromaDB (Persistent at {settings.CHROMA_DIR})
 Documents Source : {settings.DATA_DIR}
--------------------------------------------------------------------------------
 Commands:
   - Type your question and press Enter to chat.
   - Type 'exit' or 'quit' to exit the application.
   - Type '/reindex' to reload and re-chunk documents into ChromaDB.
   - Type '/help' to display this information again.
================================================================================
"""
    print(banner)


def main():
    print_banner()

    print("[Init] Initializing Knowledge Base and RAG Pipeline...")
    pipeline = RAGPipeline(data_dir=settings.DATA_DIR)
    print("[Init] Ready! You can now start asking questions.\n")

    show_sources = True

    while True:
        try:
            user_input = input("\nUser > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

        if not user_input:
            continue

        # Command handling
        cmd = user_input.lower()
        if cmd in ("exit", "quit", "q"):
            print("\nThank you for using the RAG Assistant. Goodbye!")
            break

        if cmd in ("/help", "help"):
            print_banner()
            continue

        if cmd == "/reindex":
            print(f"[Action] Re-indexing documents from '{settings.DATA_DIR}'...")
            setup_rag_system(data_dir=settings.DATA_DIR, force_reindex=True)
            print("[Action] Re-indexing complete!")
            continue

        if cmd == "/toggle-sources":
            show_sources = not show_sources
            print(f"[Setting] Source citation preview set to: {show_sources}")
            continue

        # Execute RAG query
        print("\n[Thinking] Searching documents and generating grounded answer...")
        result = pipeline.query(user_input, top_k=settings.DEFAULT_TOP_K)
        chunks = result["retrieved_chunks"]
        answer = result["answer"]

        # Bonus Challenge: Print retrieved chunks to screen before printing the answer
        if show_sources and chunks:
            print("\n" + "-" * 75)
            print("  RETRIEVED CONTEXT CHUNKS (Grounded Evidence):")
            print("-" * 75)
            for idx, c in enumerate(chunks, 1):
                doc_name = c.get("metadata", {}).get("filename", "unknown")
                chunk_id = c.get("chunk_id", "N/A")
                sim = c.get("similarity", 0.0)
                snippet = c.get("text", "").replace("\n", " ")[:140]
                print(f"  [{idx}] Source: {doc_name} | ID: {chunk_id} | Similarity: {sim:.4f}")
                print(f"      Excerpt: \"{snippet}...\"\n")
            print("-" * 75)

        # Print final generated answer
        print(f"\nAssistant:\n{answer}\n")


if __name__ == "__main__":
    main()
