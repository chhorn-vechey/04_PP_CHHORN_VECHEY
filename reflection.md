# Reflection: Building a Baseline Naive RAG Application

**Author:** Chhorn Vechey  
**Course:** HRD Advanced Course - Artificial Intelligence (Week 5 Homework)  
**Topic:** Naive RAG Fundamentals - Chat with Documents  

---

### What Worked Well
Building the pipeline step by step worked very well. Loading the documents from the folder and saving them into ChromaDB was fast and smooth. Using Ollama locally to run nomic-embed-text worked reliably. When I tested questions about VPN access, PIN resets, and company email setup, ChromaDB found the right text sections every time. Also, sending the found text to Llama 3.2 worked great. By telling the model to answer only using the provided text, it gave short, clear, and correct answers without making things up.

### What Was Harder Than Expected
The hardest part for me was splitting the documents into smaller chunks. At first, I tried cutting the text by simple character count. But because our documents have step-by-step guides and bullet points, simple cutting broke sentences and numbered steps in half. For example, a step number ended up in one chunk while the instruction was in another chunk. To fix this, I switched to splitting by paragraphs and lines with a 60-character overlap. This kept full instructions together, but finding the right chunk size took some testing.

### Ideas for Improvement Using Advanced RAG Techniques
One idea to improve this app in the future is adding Re-ranking. Right now, ChromaDB searches very fast by comparing vector numbers, but sometimes the first result is not the most helpful one. By adding a re-ranker model after retrieval, the system can look at the top results more closely and re-order them so the best matching paragraph is always at the top before sending it to the language model.
