@router.get("/logs", dependencies=[Depends(api_key_auth)])
def get_logs(n: int = 100):
    """Return the last n lines from the audit log (admin use)."""
    log_path = os.path.join(os.path.dirname(__file__), '../../logs/api_audit.log')
    if not os.path.exists(log_path):
        return {"logs": []}
    with open(log_path, "r") as f:
        lines = f.readlines()[-n:]
    return {"logs": lines}
import shap
# ---
# Model inference integration
#
import xgboost as xgb
import os
import pandas as pd

# Load model at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../models/xgb_model.json')
MODEL = xgb.Booster()
MODEL.load_model(MODEL_PATH)

DRIVER_GENES = {"TP53", "BRAF", "EGFR", "KRAS", "ALK", "PIK3CA", "NRAS", "IDH1", "PTEN", "CDKN2A", "MET", "ERBB2", "FGFR3", "KIT", "RET"}
HOTSPOT_MUTATIONS = {"TP53": ["p.R175H"], "BRAF": ["p.V600E"]}

def engineer_features_for_api(variant):
    # Minimal feature engineering for API input
    features = {}
    features["hotspot_flag"] = int(variant.protein_change in HOTSPOT_MUTATIONS.get(variant.gene, []))
    features["driver_gene_flag"] = int(variant.gene in DRIVER_GENES)
    features["tmb"] = float(variant.tmb)
    # Tumor type encoding (static for demo)
    tumor_types = ["lung_adenocarcinoma", "colorectal_cancer", "neuroblastoma", "melanoma", "breast_cancer", "thyroid_cancer", "glioma", "endometrial_cancer", "pancreatic_cancer", "bladder_cancer", "gastrointestinal_stromal_tumor", "medullary_thyroid_cancer"]
    features["tumor_type_encoded"] = tumor_types.index(variant.tumor_type) if variant.tumor_type in tumor_types else -1
    return features
# ---
# API Response Documentation
#
# The /api/variant/score endpoint accepts a JSON payload describing a variant and returns a structured response with:
#   - actionability_score (int): Simulated score for clinical actionability
#   - resistance_probability (float): Simulated probability of drug resistance
#   - model_version (str): Version of the scoring model
#   - annotation (dict): Simulated annotation (e.g., OncoKB level, COSMIC frequency, clinical impact)
#
# Example request body:
# {
#   "gene": "TP53",
#   "transcript": "NM_000546.5",
#   "protein_change": "p.R175H",
#   "genome_build": "GRCh38",
#   "tumor_type": "lung_adenocarcinoma",
#   "tmb": 12.5,
#   "prior_therapy_count": 2
# }
#
# Example response:
# {
#   "actionability_score": 87,
#   "resistance_probability": 0.12,
#   "model_version": "1.0.0",
#   "annotation": {
#     "oncokb_level": "2A",
#     "cosmic_frequency": 0.034,
#     "clinical_impact": "Likely actionable in lung cancer"
#   }
# }
#
# This endpoint is used for programmatic scoring and annotation of variants.
# ---
from fastapi import APIRouter, Depends, HTTPException, Request
import logging
from datetime import datetime
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), '../../logs/api_audit.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
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

from annotation.annotator import annotate_variant

@router.post("/score", dependencies=[Depends(api_key_auth)])
async def score_variant(variant: VariantInput, request: Request):
    # Step 1: Annotate the variant
    annotation = annotate_variant(variant.dict())
    # Step 2: Feature engineering
    features = engineer_features_for_api(variant)
    X = pd.DataFrame([features])
    dmatrix = xgb.DMatrix(X)
    # Step 3: Model inference
    actionability_score = int(MODEL.predict(dmatrix)[0])
    # Step 4: SHAP explanation
    explainer = shap.TreeExplainer(MODEL)
    shap_values = explainer.shap_values(dmatrix)
    top_features = []
    for i, col in enumerate(X.columns):
        top_features.append({"feature": col, "shap_value": float(shap_values[0][i])})
    top_features = sorted(top_features, key=lambda x: abs(x["shap_value"]), reverse=True)
    # Step 5: Simulate resistance probability
    resistance_probability = round(0.1 + 0.02 * features["tmb"], 2)

    # --- Audit Trail Logging ---
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "client_host": request.client.host if request.client else None,
        "input": variant.dict(),
        "features": features,
        "actionability_score": actionability_score,
        "resistance_probability": resistance_probability,
        "annotation": annotation,
        "top_features": top_features[:5]
    }
    logging.info(f"API_CALL: {log_entry}")

    return {
        "actionability_score": actionability_score,
        "resistance_probability": resistance_probability,
        "model_version": "1.0.0",
        "annotation": annotation,
        "top_features": top_features[:5]
    }
