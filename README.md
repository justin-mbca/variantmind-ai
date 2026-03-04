# Project Goals

VariantMind AI is an MVP for a clinical genomic variant actionability scoring system. The goal is to provide a modular, explainable, and secure platform for:
- Ingesting and normalizing VCF-like variant data
- Annotating variants with simulated clinical evidence (OncoKB/COSMIC)
- Engineering features for ML-based actionability and resistance scoring
- Providing explainable AI outputs (SHAP)
- Generating structured clinical reports for tumor boards
- Ensuring auditability and regulatory readiness (FDA SaMD)

## Overall Workflow

1. User submits variant data (VCF-like JSON) via API or dashboard.
2. System annotates variant (OncoKB/COSMIC simulation).
3. Features are engineered for ML scoring.
4. ML model (XGBoost) predicts actionability and resistance, with SHAP explanations.
5. LLM/agent layer generates clinical reports and summarizes evidence.
6. Evidence is retrieved from online databases and literature.
7. Human-in-the-loop (HITL) review: clinicians review, approve, or comment on results and evidence in the GUI.
8. All actions and outputs are logged for audit and compliance.

# Architecture Diagram

```mermaid
flowchart TD

	 A["User / API Client"] -->|VCF-like Variant JSON| B["Variant Ingestion API"]

	 B --> C["Annotation Layer<br>OncoKB / COSMIC Simulation"]
	 C --> D["Feature Engineering<br>Variant Features"]
	 D --> E["ML Scoring Engine<br>XGBoost + SHAP"]

	 E --> F["Actionability Score<br>Resistance Probability<br>SHAP Explanations"]

	 C --> G["Evidence Retrieval<br>Literature and Databases"]

	 F --> H["LLM / Agent AI Layer"]
	 G --> H

	 H --> I["LLM-powered Report Generation<br>Evidence Summarization<br>Triage Automation"]

	 I --> O["Evidence Retrieval<br>Online DB and Article Search"]
	 O --> N["Human-in-the-Loop Review<br>Evidence Display in GUI"]

	 N --> J["Audit Logging and Traceability"]
	 N --> K["Frontend Dashboard - React"]
	 N --> L["API Output - JSON or HTML Report"]

	 J -.->|Logs| M["PostgreSQL Database"]
	 B -.->|Store Variant| M
	 C -.->|Store Annotation| M

	 style H fill:#f9f,stroke:#333,stroke-width:2px
	 style E fill:#bbf,stroke:#333,stroke-width:2px
	 style M fill:#bfb,stroke:#333,stroke-width:2px
	 style N fill:#ffd,stroke:#333,stroke-width:2px
	 style O fill:#eef,stroke:#333,stroke-width:2px
```

# Step-by-Step Implementation Plan & Roadmap

Track progress and follow this checklist during development:

1. **Core API & Data Flow**
	- Finalize FastAPI backend for variant ingestion, annotation, scoring, and reporting.
	- Integrate annotation, feature engineering, ML scoring, SHAP, and report generation in `/api/variant/score`.

2. **Annotation & Feature Engineering**
	- Expand annotation logic (simulate or connect to real sources).
	- Implement feature engineering in a dedicated module.

3. **ML Model Integration**
	- Train and save an XGBoost model.
	- Update model loading, scoring, and SHAP in `ml/model.py`.
	- Integrate predictions and explanations into API responses.

4. **Evidence Retrieval**
	- Implement evidence retrieval (databases, literature, APIs).
	- Connect evidence to scoring/reporting pipeline.

5. **LLM/Agent AI Layer**
	- Add endpoints for LLM-powered report generation and evidence summarization.
	- Integrate agent logic for batch triage and automation.

6. **Human-in-the-Loop (HITL) & GUI**
	- Build React frontend for clinician review/approval.
	- Display evidence and model explanations in GUI.
	- Log all human interventions for audit/feedback.

7. **Database & Audit Logging**
	- Finalize PostgreSQL schema and SQLAlchemy models.
	- Implement audit logging for predictions, reports, and human actions.

8. **Security & Compliance**
	- Harden API key authentication.
	- Prepare for regulatory requirements (traceability, audit, privacy).

9. **Testing & CI**
	- Expand test coverage (unit, integration, end-to-end).
	- Set up CI for automated testing and linting.

10. **Documentation & Deployment**
	- Keep README and code docs up to date.
	- Dockerize backend and frontend for deployment.

## LLM, Agent AI & Evidence Integration Roadmap

We will incrementally enhance VariantMind AI to include Large Language Model (LLM), agent AI, and evidence retrieval/display capabilities for advanced clinical genomics workflows. Planned features include:

1. **LLM-Powered Clinical Report Generation**
	 - Use an LLM to generate natural language variant/tumor board reports from structured data.
	 - New endpoint: `/api/report/llm`.

2. **LLM-Based Evidence Summarization**
	 - Summarize literature or database evidence for a variant using an LLM.

3. **Agent AI for Variant Triage**
	 - Implement an agent to automate annotation, scoring, and prioritization of variant batches.
	 - New endpoint: `/api/agent/triage`.

4. **Retrieval-Augmented Generation (RAG)**
	 - Use a vector database to enable LLM-powered Q&A and evidence retrieval for variants.

5. **Prompt Engineering & Customization**
	 - Provide and allow customization of prompt templates for clinical scenarios.

6. **Audit & Traceability**
	 - Log all LLM/agent interactions for regulatory compliance.

7. **Frontend Integration**
	 - Display LLM-generated reports and agent results in the React dashboard.

8. **Evidence Retrieval and Display in GUI**
	 - Integrate automated evidence search (databases, articles) and display in the HITL review interface.

We will implement these features step by step, updating this README and the codebase as we progress.

## Example Input (API)
```json
{
	"gene": "TP53",
	"transcript": "NM_000546.5",
	"protein_change": "p.R175H",
	"genome_build": "GRCh38",
	"tumor_type": "lung_adenocarcinoma",
	"tmb": 12.5,
	"prior_therapy_count": 2
}
```

## Example Output (API)
```json
{
	"actionability_score": 87,
	"resistance_probability": 0.12,
	"model_version": "1.0.0",
	"top_features": [
		{"feature": "hotspot_flag", "shap_value": 0.32},
		{"feature": "driver_gene_flag", "shap_value": 0.21},
		{"feature": "tmb", "shap_value": 0.18},
		{"feature": "truncating_flag", "shap_value": 0.12},
		{"feature": "tumor_type_encoded", "shap_value": 0.09}
	],
	"annotation": {
		"oncokb_level": "2A",
		"cosmic_frequency": 0.034,
		"clinical_impact": "Likely actionable in lung cancer"
	},
	"report": {
		"summary": "TP53 p.R175H is a known hotspot mutation with high actionability in lung adenocarcinoma.",
		"html": "<h2>Variant Report</h2>..."
	},
	"audit_log": {
		"timestamp": "2026-03-04T12:34:56Z",
		"input_variant": { /* original input */ },
		"model_version": "1.0.0",
		"prediction_id": "abc123"
	}
}
```

## Tech Stack
- Backend: Python (FastAPI)
- ML: XGBoost + SHAP
- Data: PostgreSQL
- Frontend: React (dashboard)
- Cloud-ready (Dockerized)

## Key Features
- VCF-like variant ingestion API
- Annotation layer (OncoKB/COSMIC simulation)
- Variant-centric feature engineering
- AI scoring engine (actionability, resistance)
- SHAP explainability
- Tumor board report generator (JSON/HTML)
- Audit logging (regulatory readiness)
- API key authentication

## Quickstart
See detailed instructions in each module folder.

VariantMind AI is an MVP for a clinical genomic variant actionability scoring system. The goal is to provide a modular, explainable, and secure platform for:
- Ingesting and normalizing VCF-like variant data
- Annotating variants with simulated clinical evidence (OncoKB/COSMIC)
- Engineering features for ML-based actionability and resistance scoring
- Providing explainable AI outputs (SHAP)
- Generating structured clinical reports for tumor boards
- Ensuring auditability and regulatory readiness (FDA SaMD)

### Example Input (API)
```json
{
	"gene": "TP53",
	"transcript": "NM_000546.5",
	"protein_change": "p.R175H",
	"genome_build": "GRCh38",
	"tumor_type": "lung_adenocarcinoma",
	"tmb": 12.5,
	"prior_therapy_count": 2
}
```

### Example Output (API)
```json
{
	"actionability_score": 87,
	"resistance_probability": 0.12,
	"model_version": "1.0.0",
	"top_features": [
		{"feature": "hotspot_flag", "shap_value": 0.32},
		{"feature": "driver_gene_flag", "shap_value": 0.21},
		{"feature": "tmb", "shap_value": 0.18},
		{"feature": "truncating_flag", "shap_value": 0.12},
		{"feature": "tumor_type_encoded", "shap_value": 0.09}
	],
	"annotation": {
		"oncokb_level": "2A",
		"cosmic_frequency": 0.034,
		"clinical_impact": "Likely actionable in lung cancer"
	},
	"report": {
		"summary": "TP53 p.R175H is a known hotspot mutation with high actionability in lung adenocarcinoma.",
		"html": "<h2>Variant Report</h2>..."
	},
	"audit_log": {
		"timestamp": "2026-03-04T12:34:56Z",
		"input_variant": { /* original input */ },
		"model_version": "1.0.0",
		"prediction_id": "abc123"
	}
}
```

# VariantMind AI

A production-ready MVP for a clinical genomic variant actionability scoring system. Modular, explainable, secure, and designed for future FDA Software-as-Medical-Device compliance.

## Tech Stack
- Backend: Python (FastAPI)
- ML: XGBoost + SHAP
- Data: PostgreSQL
- Frontend: React (dashboard)
- Cloud-ready (Dockerized)

## Key Features
- VCF-like variant ingestion API
- Annotation layer (OncoKB/COSMIC simulation)
- Variant-centric feature engineering
- AI scoring engine (actionability, resistance)
- SHAP explainability
- Tumor board report generator (JSON/HTML)
- Audit logging (regulatory readiness)
- API key authentication

## Quickstart
See detailed instructions in each module folder.
