# Project Goals

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
