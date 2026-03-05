from fastapi.testclient import TestClient
from backend.main import app

def test_score_variant():
    client = TestClient(app)
    response = client.post("/api/variant/score", json={
        "gene": "TP53",
        "transcript": "NM_000546.5",
        "protein_change": "p.R175H",
        "genome_build": "GRCh38",
        "tumor_type": "lung_adenocarcinoma",
        "tmb": 12.5,
        "prior_therapy_count": 2
    }, headers={"X-API-Key": "changeme"})
    assert response.status_code == 200
    resp = response.json()
    # Check all expected keys
    expected_keys = {"actionability_score", "resistance_probability", "model_version", "annotation"}
    assert expected_keys.issubset(resp.keys())
    # Check value types
    assert isinstance(resp["actionability_score"], int)
    assert isinstance(resp["resistance_probability"], float)
    assert isinstance(resp["model_version"], str)
    assert isinstance(resp["annotation"], dict)

    # Check actual response content (matches backend/routers/variant.py placeholder)
    assert resp["actionability_score"] == 87
    assert abs(resp["resistance_probability"] - 0.12) < 1e-6
    assert resp["model_version"] == "1.0.0"
    # Annotation should match simulated output from annotate_variant
    annotation = resp["annotation"]
    assert annotation["oncokb_level"] == "2A"
    assert abs(annotation["cosmic_frequency"] - 0.034) < 1e-6
    assert annotation["clinical_impact"] == "Likely actionable in lung cancer"
