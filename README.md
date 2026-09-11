# RAG Fundamentals - Week 5 Homework: Chat with Documents App

**Student / Folder:** `04_PP_CHHORN_VECHEY`  
**Course:** HRD Advanced Course - Artificial Intelligence  
**Due Date:** 11-09-2026 - 11:59pm  

---

## Project Overview

This project is a local **Chat with Documents** app using Naive RAG (Retrieval-Augmented Generation). It reads text documents, cuts them into small pieces, turns them into numbers (vectors), saves them in a local vector database, and lets you ask questions in the terminal. The local AI model answers questions using only the information in your documents.

The app works in two main parts:
1. **Offline Setup (Getting files ready):**  
   Read text files -> Cut into small pieces -> Turn pieces into vectors -> Save into database.
2. **Online Chat (Answering questions):**  
   User asks question -> Find the best matching pieces -> Send question and pieces to AI -> AI prints grounded answer.

---

## Project Structure

```
04_PP_CHHORN_VECHEY/
│
├── data/
│   └── raw/                            # 3 original IT support text files
│       ├── 001_Setting_Up_a_Mobile_Device_for_Company_Email.txt
│       ├── 002_Resetting_a_Forgotten_PIN.txt
│       └── 003_Configuring_VPN_Access_for_Remote_Workers.txt
│
├── chroma_db/                          # Local vector database (created on run, ignored by git)
│
├── src/                                # Main application package
│   ├── __init__.py                     # Package setup & clean exports
│   ├── config.py                       # Settings file (models, paths, chunk sizes)
│   ├── ollama_client.py                # Bridge to talk to local Ollama
│   ├── ingestion.py                    # Step 1: Loads text files from data/raw/
│   ├── chunking.py                     # Step 2: Splits text into small pieces
│   ├── embeddings.py                   # Step 3: Turns text pieces into vectors
│   ├── vector_store.py                 # Step 4: Saves vectors into ChromaDB
│   ├── retriever.py                    # Step 5: Finds best matching chunks for a question
│   ├── generator.py                    # Step 6: Assembles prompt & gets grounded answer
│   └── pipeline.py                     # Step 7: Connects retriever and generator together
│
├── scripts/
│   └── demo_vector_check.py            # Standalone check to test vector search (Step 4)
│
├── main.py                             # Step 8: Terminal chat window to talk with documents
├── pyproject.toml                      # Poetry package file
├── requirements.txt                    # Pip package file
├── .gitignore                          # Tells git to ignore cache and database files
├── README.md                           # Project guide and instructions
├── test_log.md                         # Log of 5 test questions, found chunks, and answers
└── reflection.md                       # Short reflection on what worked and what was hard
```

---

## Tools Used

| Tool | Name | What It Does |
| :--- | :--- | :--- |
| **Local AI Model** | `llama3.2` | Runs locally with Ollama. Reads the found text pieces and writes the answer. |
| **Embedding Model** | `nomic-embed-text` | Runs locally with Ollama. Turns text into a list of 768 numbers to capture meaning. |
| **Vector Database** | **ChromaDB** | Runs locally on disk at `./chroma_db`. Stores vectors and searches them fast. |
| **Language** | **Python 3.13** | Clean Python code using standard libraries. |

---

## Chunking Strategy (How We Split Text)

- **Strategy used:** Paragraph and line-aware splitting with overlap (`src/chunking.py`).
  - Chunk size: **450 characters**
  - Chunk overlap: **60 characters** (with word-boundary snapping)
- **Why we chose this:**
  Our documents are IT support guides with numbered steps (like "Step 1: Go to settings"). If we just cut text by a fixed character number, sentences and step numbers get cut in half. Splitting by paragraphs and line breaks keeps full steps together. The 60-character overlap makes sure no important words are missed between two pieces.
- **Comparison (Bonus Challenge 1):**
  We also tested simple character cutting (`split_text_fixed`). Running `python -m src.chunking` shows that paragraph splitting makes 23 clean pieces, while simple fixed cutting makes 19 broken pieces.

---

## How to Run the App

### 1. Setup Models & Packages
Make sure Ollama is open and you have downloaded the two models:
```bash
ollama serve
ollama pull llama3.2
ollama pull nomic-embed-text
```

Install the required Python packages:
```bash
# Using pip:
pip install -r requirements.txt

# Or using Poetry:
poetry install
```

### 2. Test Pipeline Stages Step-by-Step
You can test each stage individually to see how each step works:
```bash
python -m src.ingestion     # Step 1: Tests loading documents from data/raw/
python -m src.chunking      # Step 2: Tests text splitting & compares strategies
python -m src.embeddings    # Step 3: Tests vector embedding generation
python -m src.vector_store  # Step 4: Indexes documents into ChromaDB
```

### 3. Run Standalone Vector Check (Homework Step 4)
Before opening the chat app, test the vector search by itself:
```bash
python scripts/demo_vector_check.py
```
This script embeds a test question, searches ChromaDB, and prints the top 3 matching chunks to prove the offline steps work.  
*(Note: If the database is not indexed yet, the script will automatically index it for you!)*

### 4. Run the Chat App (Homework Step 6)
Start the terminal chat app:
```bash
python main.py
```

**Commands inside the chat:**
- Type your question and press **Enter** to chat.
- Type `exit` or `quit` to close the app.
- Type `/reindex` to reload all documents into ChromaDB.
- Type `/help` to see help instructions.
- Type `/toggle-sources` to turn chunk previews on or off.

---

## Bonus Challenges Completed

| # | Bonus Challenge | Where in Code | What Was Done |
|:-:|:---|:---|:---|
| **1** | **Compare two text splitting methods** | `src/chunking.py` | Compares paragraph splitting (23 clean chunks) with simple character cutting (19 broken chunks). |
| **2** | **Print found chunks before the answer** | `main.py` | Shows the source file name, chunk ID, similarity score, and text excerpt on screen before printing the answer. |
| **3** | **Say "I could not find this..." if no match** | `src/generator.py` | If a question is not in the documents (like baking a cake), the app refuses to guess and answers: *"I could not find this in your documents."* |

---

## Tests and Reflection
- See **`test_log.md`** for the 5 test questions (4 on-topic questions and 1 off-topic question).
- See **`reflection.md`** for the short written reflection (261 words).
