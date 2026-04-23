# RAG Customer Support Assistant (LangGraph + HITL)

This project implements a production-style **Retrieval-Augmented Generation (RAG)** customer support assistant that delivers accurate, context-aware, and scalable support responses using AI.

It combines **document retrieval**, **workflow orchestration**, **intent-based routing**, and **Human-in-the-Loop (HITL)** escalation for real-world enterprise customer support automation.

---

## 🚀 Features

* PDF ingestion pipeline
* Text chunking + embedding generation
* ChromaDB vector storage
* LangGraph workflow orchestration
* Intent-based routing
* Human-in-the-Loop (HITL) escalation
* Groq LLM integration for final response generation
* CLI chat mode
* Streamlit web app
* Debug insights (intent, confidence, route, sources)

---

## 📌 Why This Project Exists

Customer support teams need fast and reliable responses, but traditional systems face many problems:

* Static FAQ bots miss document context
* LLM-only bots hallucinate without grounding
* Sensitive or complex issues need human intervention
* Not every customer query should be answered automatically

### ✅ Solution

This project combines:

* Retrieval-Augmented Generation (RAG)
* Controlled workflow automation
* Human escalation policy

This creates a smarter, safer, and more accurate support assistant.

---

## 🏗️ System Architecture

### Ingestion Flow

PDF Documents → Text Extraction → Chunking → Embeddings → ChromaDB

### Query Flow

User Query → Retrieve Relevant Chunks → Detect Intent → Decide Route

### Routing Options

#### ✅ auto_answer

* Uses retrieved context
* Sends grounded prompt to Groq LLM
* Generates final AI response

#### 👨‍💻 escalate

* Low confidence / sensitive query
* Human agent reviews case
* Human response returned as final output

---

## ⚙️ Quick Start (Windows PowerShell + venv)

### Step 1: Create venv and install packages

```powershell
cd d:\Final
.\scripts\setup_venv.ps1
```

### Step 2: Configure environment

```powershell
Copy-Item .env.example .env
```

Edit `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Optional:

* Model settings
* Temperature
* Retrieval tuning parameters

### Step 3: Generate sample PDF knowledge base

```powershell
.\.venv\Scripts\Activate.ps1
python scripts\generate_sample_kb_pdf.py
```

This creates:

```text
data/customer_support_kb.pdf
```

### Step 4: Ingest PDF into ChromaDB

```powershell
python app.py ingest --pdf data/customer_support_kb.pdf --reset
```

### Step 5: Ask one question

```powershell
python app.py ask "How can I reset my password?"
```

### Step 6: Interactive chat mode

```powershell
python app.py chat
```

If escalation is needed, the system will prompt for a human response.

### Step 7: Run Streamlit web app

```powershell
streamlit run streamlit_app.py
```

---

## 🌐 Streamlit Features

* Upload or select PDF knowledge base
* Sidebar ingestion controls
* Customer support chat interface
* Debug details for intent, route, confidence, and sources
* HITL text area for escalated responses

### Note

Includes:

```text
.streamlit/config.toml
```

With:

```toml
fileWatcherType = "none"
```

Prevents noisy optional torchvision tracebacks from transformers.

---

## 📄 Build Deliverable PDFs

```powershell
python scripts\build_pdfs.py
```

Generates:

```text
docs/HLD.pdf
docs/LLD.pdf
docs/Technical_Documentation.pdf
```

---

## ✅ Validate Implementation

### Run Unit Tests

```powershell
pytest -q
```

### Run Crosscheck

```powershell
python scripts\crosscheck.py
```

---

## 📂 Project Structure

```text
.
|-- app.py
|-- streamlit_app.py
|-- .streamlit/
|   `-- config.toml
|-- requirements.txt
|-- .env.example
|-- src/
|   `-- rag_support/
|       |-- config.py
|       |-- ingest.py
|       |-- retrieval.py
|       |-- routing.py
|       |-- workflow.py
|       |-- hitl.py
|       |-- cli.py
|       |-- prompts.py
|       `-- schemas.py
|-- scripts/
|   |-- setup_venv.ps1
|   |-- generate_sample_kb_pdf.py
|   |-- build_pdfs.py
|   `-- crosscheck.py
|-- docs/
|   |-- HLD.md
|   |-- LLD.md
|   `-- TECHNICAL_DOCUMENTATION.md
|-- data/
|   `-- customer_support_kb.pdf
`-- tests/
    `-- test_routing.py
```

---

## 🔄 Runtime Behavior Summary

### Ingestion Pipeline

PDF → Chunks → Embeddings → Chroma Collection

### Query Pipeline

User Query
↓
Retrieve Top-K Chunks + Score
↓
Detect Intent
↓
Decide Route

### Final Routes

* auto_answer → AI generated grounded response
* escalate → Human reviewed response

---

## 🛠️ Tech Stack

* Python
* LangGraph
* LangChain
* ChromaDB
* Groq API
* Streamlit
* Vector Search
* RAG Architecture

---

## 📌 Example Use Cases

* Password reset support
* Billing queries
* Refund requests
* Subscription help
* Product troubleshooting
* Human escalation handling

---

## 📈 Key Learnings

* Built end-to-end production RAG pipeline
* Implemented workflow-based AI routing
* Reduced hallucinations using grounded retrieval
* Added Human-in-the-Loop safety layer
* Built deployable AI support assistant

---

## 👨‍💻 Developed By

**Someshwar Waghmode**
Generative AI Developer | AI Engineer

---

## ⭐ If you like this project, give it a star!
