from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.security import api_key_auth

class VariantInput(BaseModel):
    gene: str
    transcript: str
    protein_change: str
    genome_build: str
    tumor_type: str
    tmb: float
    prior_therapy_count: int

router = APIRouter()

@router.post("/score", dependencies=[Depends(api_key_auth)])
def score_variant(variant: VariantInput):
    # Placeholder: integrate annotation, ML, SHAP, reporting
    return {"actionability_score": 87, "resistance_probability": 0.12, "model_version": "1.0.0"}
