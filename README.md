# GovTrace AI

**GovTrace AI** is a personal AI governance and observability project designed to explore how runtime AI behavior can be converted into measurable governance evidence.

The long-term objective is to build a continuous AI governance platform that combines **LLM observability, risk assessment, automated evaluation, human review, and compliance mapping** across frameworks such as:

* NIST AI Risk Management Framework
* ISO/IEC 42001
* EU AI Act

The project is being developed incrementally. The current version represents **Milestone M1: Observable RAG**.

---

## Project Vision

Traditional AI governance often depends on static documents, questionnaires, spreadsheets, and periodic assessments.

GovTrace AI explores a different approach:

> **Governance-as-Observability**

Instead of only documenting how an AI system is expected to behave, GovTrace captures evidence from how the system actually behaves during runtime.

The intended future architecture is:

```text
AI Application
      ↓
Runtime Observability
      ↓
Automated Evaluation
      ↓
Risk Detection
      ↓
Governance Evidence
      ↓
Framework Mapping
      ↓
Human Review
      ↓
Mitigation
```

---

## Current Milestone — M1

M1 establishes the technical foundation required for future governance and risk-management capabilities.

### M1.1 — Development Environment

Completed setup for:

* Python
* Virtual environment
* Project structure
* Dependency management
* Environment variable management

### M1.2 — Gemini LLM Integration

GovTrace currently uses the **Google Gemini API** through LangChain.

The LLM provider is abstracted through a dedicated module so that other providers can be integrated later without redesigning the application.

```text
GovTrace
   ↓
LangChain
   ↓
Gemini
```

### M1.3 — RAG Knowledge Base

GovTrace implements a local Retrieval-Augmented Generation pipeline.

Current components:

* LangChain
* Chroma vector database
* Hugging Face sentence-transformer embeddings
* Local governance documents
* Gemini answer generation

Current flow:

```text
User Question
      ↓
Local Vector Search
      ↓
Relevant Evidence
      ↓
Gemini
      ↓
Evidence-Grounded Answer
```

The first knowledge source currently contains introductory information about the **NIST AI Risk Management Framework**.

---

## M1.4 — Langfuse Observability

GovTrace uses **Langfuse** to capture runtime information about AI interactions.

Current traces include:

* User query
* Evidence retrieval
* Retrieved chunks
* Source documents
* LLM generation
* Model execution
* Application metadata

Example trace:

```text
govtrace-rag-query
│
├── chroma-evidence-retrieval
│
└── govtrace-answer-generation
```

This observability layer is intended to become a source of governance evidence in later milestones.

---

## M1.5 — Automated Groundedness Evaluation

GovTrace evaluates whether an AI-generated answer is supported by the retrieved evidence.

The evaluator returns:

```text
Groundedness score: 0.00 – 1.00
Threshold: 0.80
Result: PASS / REVIEW
```

Example:

```text
Groundedness: 0.96
Threshold: 0.80
Result: PASS
```

The LLM produces the evaluation score, while the final PASS/REVIEW decision is determined by application logic.

```python
passed = groundedness_score >= 0.80
```

This design prevents the model from independently deciding governance policy.

---

# Architecture

Current M1 architecture:

```text
                        User
                         │
                         ▼
                    GovTrace AI
                         │
                         ▼
                     LangChain
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       Chroma Vector DB          Gemini API
              │                     │
              ▼                     ▼
       Local Embeddings           Answer
              │                     │
              └──────────┬──────────┘
                         ▼
                       Langfuse
                         │
                         ▼
                 Groundedness Judge
                         │
                         ▼
                  PASS / REVIEW
```

---

# Technology Stack

| Layer                  | Technology                             |
| ---------------------- | -------------------------------------- |
| Language               | Python                                 |
| LLM                    | Google Gemini                          |
| AI Framework           | LangChain                              |
| Vector Database        | Chroma                                 |
| Embeddings             | sentence-transformers/all-MiniLM-L6-v2 |
| Observability          | Langfuse                               |
| Validation             | Pydantic                               |
| Environment Management | python-dotenv                          |
| UI                     | Streamlit planned/current development  |
| Version Control        | Git / GitHub                           |

---

# Project Structure

```text
govtrace-ai/
│
├── app/
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── groundedness.py
│   │
│   ├── observability/
│   │   ├── __init__.py
│   │   └── langfuse_client.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── ingest.py
│   │   └── service.py
│   │
│   ├── __init__.py
│   ├── config.py
│   └── llm.py
│
├── data/
│   └── knowledge/
│       └── nist_ai_rmf.txt
│
├── scripts/
│   ├── __init__.py
│   ├── build_index.py
│   ├── test_llm.py
│   ├── test_rag.py
│   └── test_evaluation.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-lock.txt
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/FarhanMuhib/govtrace-ai.git
cd govtrace-ai
```

---

## 2. Create a Virtual Environment

Windows:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory.

Example:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model

LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

Never commit the `.env` file.

The repository includes `.env.example` as a safe reference.

---

# Build the Knowledge Index

Before running RAG queries:

```powershell
python -m scripts.build_index
```

Expected result:

```text
Documents loaded: 1
Chunks created: 3
Index created: Chunks: 3
```

The generated Chroma database is stored locally and should not be committed to Git.

---

# Test Gemini Connection

```powershell
python -m scripts.test_llm
```

Expected result:

```text
GovTrace Gemini connection successful.
```

---

# Test RAG

```powershell
python -m scripts.test_rag
```

Example:

```text
ANSWER
----------------

The four core functions of the NIST AI RMF are:

1. GOVERN
2. MAP
3. MEASURE
4. MANAGE

SOURCES
----------------

nist_ai_rmf.txt
```

---

# Test Automated Evaluation

```powershell
python -m scripts.test_evaluation
```

Example:

```text
EVALUATION
----------------

Groundedness: 0.96
Threshold: 0.80
Result: PASS
```

---

# Security

The following files and directories should never be committed:

```text
.env
.venv/
data/chroma/
__pycache__/
.vscode/
```

API credentials must always remain outside source control.

For development, only public or synthetic data should be used.

Do not send confidential, production, medical, financial, customer, or personally sensitive data to external model providers without appropriate governance and contractual controls.

---

# Current Limitations

GovTrace M1 is an experimental development milestone.

Current limitations include:

* Only one governance knowledge source is currently indexed
* Groundedness is the only automated evaluator
* Risk management is not yet implemented
* Framework compliance is not automatically determined
* ISO/IEC 42001 mapping is not yet implemented
* EU AI Act mapping is not yet implemented
* Human approval workflows are not yet implemented
* Production authentication is not implemented
* No production deployment is currently provided

GovTrace should not currently be used as a legal compliance certification system.

---

# Roadmap

## M1 — Observable RAG

* [x] Development environment
* [x] Gemini integration
* [x] RAG knowledge base
* [x] Langfuse tracing
* [x] Automated groundedness evaluation

## M2 — AI Risk Engine

Planned capabilities:

* Risk identification
* Likelihood scoring
* Impact scoring
* Inherent risk calculation
* Residual risk calculation
* Severity classification
* Risk register
* Evidence-to-risk relationships
* Human review requirements

## M3 — NIST AI RMF Mapping

Planned mapping:

```text
GOVERN
MAP
MEASURE
MANAGE
```

Runtime evidence and risk records will be mapped to relevant NIST AI RMF outcomes.

## M4 — Evidence Engine

Planned capabilities:

* Evidence records
* Evidence source tracking
* Evidence timestamps
* Evidence freshness
* Confidence scoring
* Control-to-evidence mapping

## M5 — Human-in-the-Loop Governance

Planned use of LangGraph for:

* Approval workflows
* Escalation
* Risk acceptance
* Human validation
* Mitigation review

## M6 — Grafana and OpenTelemetry

Planned observability layer:

* Governance dashboards
* AI risk dashboards
* Operational metrics
* Alerts
* Model-quality drift
* Incident signals

## M7 — Governance Digital Twin

Each AI system will have a live governance representation containing:

```text
AI System
├── Models
├── Data
├── Prompts
├── Tools
├── Risks
├── Controls
├── Evidence
├── Incidents
└── Framework Mapping
```

## M8 — Governance / Compliance Drift

GovTrace will detect when changes to:

* Models
* Prompts
* Knowledge bases
* Tools
* Data
* System configuration

create new governance risks or invalidate previous evidence.

## M9 — EU AI Act Mapping

Planned capabilities include:

* AI system screening
* Role identification
* Potential risk-category assessment
* Evidence mapping
* Transparency controls
* Human-oversight evidence

## M10 — ISO/IEC 42001 Mapping

Planned capabilities:

* AI management system evidence
* Governance controls
* Risk-management evidence
* Monitoring
* Continual improvement
* Audit-support workflows

## M11 — CI/CD Governance Gate

Future AI releases may be evaluated before deployment.

Example:

```text
New AI Release
      ↓
GovTrace Evaluation
      ↓
Risk Analysis
      ↓
PASS
or
HUMAN REVIEW REQUIRED
```

## M12 — Production Deployment

Planned production architecture may include:

* FastAPI
* PostgreSQL
* LangGraph
* OpenTelemetry
* Grafana
* Docker
* Role-based access control
* Production dashboard

---

# Research Direction

GovTrace also explores the research question:

> **Can runtime AI observability be transformed into continuous and auditable evidence for AI governance and risk-management frameworks?**

Future experiments may compare traditional periodic governance assessments with continuous governance observability based on:

* Evidence freshness
* Risk detection latency
* Traceability
* Human review effort
* Evaluation reliability
* Governance drift detection

---

# Project Principle

GovTrace follows one central design principle:

> **An AI system should not be considered trustworthy because an LLM says it is trustworthy. Governance decisions should be supported by traceable evidence, deterministic controls, measurable risk signals, and appropriate human review.**

---

# Status

**Current Version:** M1
**Project Status:** Active Development
**Current Focus:** Observable RAG and automated evaluation
**Next Milestone:** M2 — AI Risk Engine

---

## Author

**Farhan Muhib**

GitHub: `FarhanMuhib`

---

## Disclaimer

GovTrace AI is currently a personal research and engineering project.

It does not provide legal advice, regulatory certification, formal ISO certification, or official compliance determinations.

Human review and qualified legal, regulatory, security, and governance expertise remain necessary for real-world high-impact deployments.
