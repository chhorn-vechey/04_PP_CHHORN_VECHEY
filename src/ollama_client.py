"""
ollama_client.py
----------------
Unified, resilient client for communicating with local Ollama service.
Handles both vector embeddings and LLM chat completions with automatic
fallback from official SDK to direct HTTP REST calls.
"""

import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

# pyrefly: ignore [missing-import]
from src.config import settings

try:
    import ollama
    HAS_OLLAMA_PKG = True
except ImportError:
    HAS_OLLAMA_PKG = False


class OllamaClient:
    """
    Encapsulates interaction with local Ollama server for embeddings and chat.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")

    def _post(self, endpoint: str, payload: Dict[str, Any], timeout: int = 60) -> Dict[str, Any]:
        """Internal helper for REST API calls to Ollama with unified error handling."""
        req = urllib.request.Request(
            f"{self.base_url}{endpoint}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Failed to communicate with Ollama at {self.base_url}. "
                f"Please verify Ollama is running ('ollama serve'). Error: {e}"
            )

    def get_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """Generates vector embeddings for the provided text."""
        target_model = model or settings.EMBEDDING_MODEL
        cleaned_text = text.strip() or " "

        if HAS_OLLAMA_PKG:
            try:
                res = ollama.embeddings(model=target_model, prompt=cleaned_text)
                if "embedding" in res:
                    return res["embedding"]
            except Exception:
                pass

        data = self._post("/api/embeddings", {"model": target_model, "prompt": cleaned_text})
        return data["embedding"]

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.1
    ) -> str:
        """Sends chat messages to Ollama and returns the assistant's response string."""
        target_model = model or settings.LLM_MODEL

        if HAS_OLLAMA_PKG:
            try:
                res = ollama.chat(
                    model=target_model,
                    messages=messages,
                    options={"temperature": temperature}
                )
                return res["message"]["content"].strip()
            except Exception:
                pass

        payload = {
            "model": target_model,
            "messages": messages,
            "options": {"temperature": temperature},
            "stream": False
        }
        data = self._post("/api/chat", payload, timeout=120)
        return data["message"]["content"].strip()


# Default shared client instance
default_client = OllamaClient()
