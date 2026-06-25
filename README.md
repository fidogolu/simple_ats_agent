# 🧩 Simple ATS Pipeline Template

> A modular, secure, and extensible boilerplate for building LLM-powered document processing applications with RAG, structured output, and full observability.

---

## 📌 Description

**Document Analysis Pipeline** is a production-ready template that demonstrates a **modular pipeline architecture** for document analysis using AI/LLM technologies. It anonymizes PII before any processing, uses semantic search to extract the most relevant document excerpts, and generates structured reports via a local LLM.

This template is designed to be **technology-agnostic** — all business-specific logic has been abstracted away, leaving behind a clean, reusable foundation that showcases modern Python backend patterns.

---

## 🧠 Architecture

```
[Document + Context Query]
       │
       ▼
[Node 1 — Extraction]
  • Text extraction (PDF / DOCX)
  • PII anonymization (llm-guard)
  • Prompt injection detection
      │
      ▼
[Node 2 — Retrieval]
  • Chunking (RecursiveCharacterTextSplitter)
  • Vectorization (HuggingFace Embeddings)
  • Similarity search (Chroma)
      │
      ▼
[Node 3 — Analysis]
  • Structured LLM call (llama.cpp / OpenAI-compatible)
  • Output: AnalysisResult (Pydantic)
      │
      ▼
[Final Report]
  • Score A / Score B / Score C
  • Missing items & suggestions
```

---

## 🧰 Technologies

| Component | Technology |
|---|---|
| **LLM** | llama.cpp (OpenAI-compatible API) |
| **RAG** | Chroma + HuggingFace Embeddings |
| **Orchestration** | LangGraph |
| **UI** | Gradio 6 |
| **Security** | llm-guard (PII anonymization + prompt injection detection) |
| **Package manager** | uv |
| **Observability** | Langfuse |

---

## 📁 Project Structure

```
document-analysis-pipeline/
├── config/
│   ├── assets/                # Static assets (logos, banners)
│   └── prompts/
│       └── instructions.txt   # LLM prompt template
├── models/
│   └── schemas.py             # Pydantic + TypedDict schemas
├── nodes/
│   ├── extraction.py          # Node 1: text extraction + PII anonymization
│   ├── retrieval.py           # Node 2: vectorization + similarity search
│   └── analysis.py            # Node 3: structured LLM report generation
├── tests/
│   └── test_nodes.py          # Unit tests (pytest)
├── utils/
│   ├── __init__.py
│   ├── cache_cleaner.py       # Temp folder cleanup after each session
│   ├── logger.py              # Centralized logger
│   └── preprocessing.py       # Text utilities
├── graph.py                   # LangGraph orchestration
├── app.py                     # Gradio entry point
├── pyproject.toml             # Dependencies + pytest config
├── .env.example               # Environment variables template
├── logs/                      # Application logs (runtime)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10–3.13
- [uv](https://docs.astral.sh/uv/) package manager
- A running llama.cpp server (or any OpenAI-compatible API)
- NVIDIA GPU recommended (CUDA 12.8+)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/document-analysis-pipeline.git
cd document-analysis-pipeline

# Install dependencies
uv sync
```

### Configuration

Copy `.env.example` to `.env` and fill in your values:

```dotenv
# LLM
OPENAI_BASE_URL="http://localhost:8000"
OPENAI_API_KEY="sk-no-key-required"
OPENAI_DEFAULT_MODEL="your-model-name"
GEN_TEMPERATURE="0.0"
GEN_MAX_TOKENS="2048"

# Langfuse observability
LANGFUSE_PUBLIC_KEY="your_public_key"
LANGFUSE_SECRET_KEY="your_secret_key"
LANGFUSE_HOST="https://cloud.langfuse.com"

# Gradio
GRADIO_TEMP_DIR="./temp_data"

# Logging
LOG_LEVEL="INFO"
```

### Run

```bash
uv run app.py
```

Then open: [http://localhost:8080](http://localhost:8080)

---

## 🔒 Privacy & Security

- **PII anonymization**: names, emails, phone numbers and URLs are anonymized by `llm-guard` before any LLM call
- **Prompt injection detection**: all inputs are scanned before processing
- **Local-first**: the LLM runs locally via llama.cpp — no data is sent to external APIs
- **Temporary files**: uploads are stored in `/temp_data/` and cleaned after each session via `cache_cleaner.py`

---

## 🧪 Tests

```bash
uv run pytest tests/ -v
```

Tests cover:
- `extraction_node`: text extraction, PII blocking, unsupported formats
- `retrieval_node`: empty inputs, valid retrieval, exception handling
- `analysis_node`: error string passthrough, LLM failure, valid structured output

All heavy models (llm-guard, HuggingFace) are mocked for fast unit tests (~6 seconds).

---

## 📊 Example Output

```
📊 Score A: 65/100
🎯 Score B: 45/100
📝 Score C: 70/100

🌍 Language / Sections: Clear and professional. Well-structured sections.
🏷️ Title: Title does not align with the target context.
👤 Name/Surname: Present but anonymized before analysis.
📞 Contact: Missing from the provided excerpt.
📍 Mobility: No explicit mention of geographic mobility.
💼 Experience: Strong background, partially aligned with the offer.
🔁 Repetitions: None detected.
✏️ Spelling Errors: None detected.
🔑 Keywords: Present: security, audit. Missing: customer success, SaaS.
📈 Numeric Results: Certifications and years mentioned.

❌ Missing Items: customer success manager, post-sales journey, strategic accounts

✅ Corrections: None

💡 Suggestions:
  - Align the title with the target context.
  - Highlight relevant experience.
  - Add geographic mobility if applicable.
  - Quantify impact with metrics where possible.
```

---

## 📜 License

MIT License — See the [`LICENSE`](LICENSE.md) file for details.
