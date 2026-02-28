
<div align="center">
  <img src="images/AIREPipeline.png" alt="AIRE Pipeline" width="700"/>
  
  <h1 style="font-size:2.5em; color:#0078D4; margin-top:0.5em;">AIRE: AI-Driven SOAR Pipeline</h1>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python"/>
    <img src="https://img.shields.io/badge/FastAPI-Open%20Source-green?logo=fastapi"/>
    <img src="https://img.shields.io/badge/Azure%20OpenAI-Integrated-blueviolet?logo=microsoftazure"/>
    <img src="https://img.shields.io/badge/Prometheus-Monitoring-orange?logo=prometheus"/>
    <img src="https://img.shields.io/badge/Elasticsearch-Search-yellow?logo=elasticsearch"/>
    <img src="https://img.shields.io/badge/License-Apache%202.0-brightgreen"/>
  </p>
</div>

---

<div align="center">
  <b style="font-size:1.3em; color:#444;">Enterprise-Grade, Modular, Multi-Agent SOAR for AI-Driven Security Automation</b>
</div>

---

## 🚀 Overview

AIRE (AI-Driven Incident Response Engine) is a next-generation, modular SOAR pipeline built for enterprise security automation. Powered by Python, FastAPI, Azure OpenAI, and advanced agent frameworks, AIRE orchestrates intelligent, scalable, and secure incident response workflows.

---

## 🌟 Key Features

- **Multi-Agent Architecture**: Modular agents for classification, knowledge base, notifications, and more
- **RAG-Enabled**: Retrieval-Augmented Generation for contextual, accurate responses
- **Prometheus Monitoring**: Real-time metrics and health checks
- **Elasticsearch & Kibana**: Advanced search and visualization
- **Azure AI Search**: Enterprise-grade search capabilities
- **Secure & Open Source**: Designed for extensibility and security

---

## 🏗️ Architecture & Workflow

<div align="center">
  <img src="images/SOAR5.png" alt="SOAR Architecture" width="650"/>
</div>

---

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/aire_project.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Azure OpenAI & Cognitive Search
#    Edit azure_openai_config.py with your credentials

# 4. (Optional) Create & upload Azure Search index
python create_and_upload_index.py

# 5. Start the FastAPI server
uvicorn fast_api_app:app --reload

# 6. Send events to the pipeline
#    POST to http://localhost:8000/ingest with your event JSON
```

---

## 📁 Directory Structure

```bash
aire_project/
├── .env                    # Environment variables (credentials, keys)
├── app.py                  # (Optional) UI or legacy entrypoint
├── fast_api_app.py         # FastAPI event ingestion & pipeline entrypoint
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── agents/                 # Modular agent definitions
│   ├── critic_agent.py         # CriticAgent: reviews, critiques, and triggers final email notification
│   ├── detection_agent.py      # DetectionAgent: triage and risk scoring
│   ├── investigation_agent.py  # InvestigationAgent: deep analysis
│   ├── response_agent.py       # ResponseAgent: suggests response (no email)
│   └── __init__.py
│
├── core/                   # Core pipeline logic and orchestration
│   ├── detection.py            # Main detection logic: loads baselines, applies rules, calculates risk/confidence
│   ├── models.py                # Event/incident data models
│   ├── pipeline.py              # Pipeline utilities
│   ├── planner.py               # Orchestrates detection, risk scoring, and agent workflow
│   ├── response_engine.py       # (Optional) Response logic
│   ├── risk_engine.py           # Risk scoring logic
│   ├── storage.py               # Incident/event storage helpers
│   ├── team_pipeline.py         # Multi-agent investigation/response logic (email sent only after CriticAgent approval)
│   └── __init__.py
│
├── firewall/               # Input validation, sanitization, injection detection
│   ├── injection_detector.py   # Detects prompt injection attempts
│   ├── sanitizer.py            # Cleans/sanitizes text fields
│   ├── schema.py               # Event schema/structure
│   ├── validator.py            # Event validation & cleaning
│   └── __pycache__/
│
├── tools/                  # System tools (e.g., email, knowledge base)
│   ├── disable_user.py         # Example: disables user accounts
│   ├── elasticsearch_sample.py # ES tool sample
│   ├── log_action.py           # Logs actions to system
│   ├── send_email.py           # Email sending utility (used only after CriticAgent approval)
│   ├── test_send_email.py      # Email test script
│   └── __pycache__/
│
├── utility/                # Logging, LLM config, prompts
│   ├── elasticsearch_logger.py # ES logging integration
│   ├── llm_config.py           # LLM configuration
│   ├── logger.py               # Centralized logging setup
│   ├── prompts.py              # Prompt templates for agents
│   └── __init__.py
│
├── data/                   # Baseline profiles, event/incident storage
│   ├── baseline_profiles.json     # Baseline profiles for detection
│   ├── events.json              # Event storage
│   ├── incidents.json           # Incident storage
│   └── knowledge_base.json      # Knowledge base for agents
│
├── config/                 # Azure/OpenAI config files
│   ├── azure_openai_config.py
│   └── __init__.py
│
├── policies/               # Policy files
│   ├── agentic_ai_policy.txt
│   ├── cloud_security_baseline.txt
│   ├── incident_response_policy.txt
│   ├── llm_usage_policy.txt
│   ├── privileged_access_policy.txt
│
├── rag/                    # RAG utilities
│   ├── azure_search_utils.py
│   ├── create_and_upload_index.py
│   ├── embedding_utils.py
│   └── __init__.py
│
├── tests/                  # Test scripts and files
│   ├── agent_test.py
│   └── __init__.py
│
├── ui/                     # UI templates and static files
│   ├── static/
│   └── templates/
│
├── event.json              # Sample event file
├── __archive/              # Archive/legacy files
├── __pycache__/            # Python cache
└── .venv/                  # Python virtual environment
```

---

## 🖼️ Visuals & Workflow

<div align="center">
  <img src="images/AIREPipeline.png" alt="AIRE Security Event Pipeline" width="600"/>
  <br/>
  <img src="images/AzureStorageBlob1.png" alt="Azure Storage Blob" width="350"/>
  <img src="images/AzureStorageRAG4.png" alt="Azure Storage RAG" width="350"/>
  <br/>
  <img src="images/SOAR5.gif" alt="SOAR HTML UI" width="350"/>
  <img src="images/ES3.gif" alt="Kibana Dashboard" width="350"/>
  <br/>
  <img src="images/Mail2.png" alt="Email Notification" width="350"/>
  <img src="images/Prometheus.gif" alt="Prometheus Dashboard" width="350"/>
</div>

---

## 🔒 Security Workflow

1. **Firewall Validation**: Event schema validation, sanitization, and prompt injection detection. Unsafe events are rejected.
2. **Detection & Risk Scoring**: Baseline profiles, deterministic rules, risk scoring, and findings extraction.
3. **RAG Context Retrieval**: Azure Cognitive Search + OpenAI embeddings for dynamic, explainable context.
4. **Multi-Agent Investigation**: DetectionAgent, InvestigationAgent, ResponseAgent, CriticAgent (only CriticAgent sends final email notification).
5. **Logging & Metrics**: Centralized logging (Kibana/ELK), Prometheus metrics.
6. **Response**: Automated/manual response as needed.

---

## 🛠️ Customization & Extensibility

- Add new detection rules in `core/detection.py` or `risk_engine.py`
- Add/modify agents in `agents/` for new logic
- Tune firewall validation in `firewall/validator.py`, `schema.py`, or `sanitizer.py`
- Integrate more tools via `tools/`
- Change RAG retrieval logic in `azure_search_utils.py`
- Update embedding logic in `embedding_utils.py`

---

## 🤝 Contributing

We welcome contributions! Fork the repo, submit pull requests, and help us build the future of AI-driven security automation.

---

## 📜 License

Apache License 2.0

---

**Developed by Intisam Ahmed**

All rights reserved.
