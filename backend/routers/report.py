from fastapi import APIRouter, Depends
from backend.security import api_key_auth

router = APIRouter()

@router.get("/tumor-board", dependencies=[Depends(api_key_auth)])
def tumor_board_report():
    # Placeholder: generate and return report
    return {"report": "<h2>Variant Report</h2>..."}
