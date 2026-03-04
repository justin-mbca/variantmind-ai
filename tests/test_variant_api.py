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
    assert "actionability_score" in response.json()
