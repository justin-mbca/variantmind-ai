"""
FastAPI app for VariantMind AI: Variant Actionability Scoring System
"""
from fastapi import FastAPI
from backend.routers import variant, report


app = FastAPI(title="VariantMind AI", version="1.0.0")

app.include_router(variant.router, prefix="/api/variant", tags=["variant"])
app.include_router(report.router, prefix="/api/report", tags=["report"])

if __name__ == "__main__":
	import uvicorn
	uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
