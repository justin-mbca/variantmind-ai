from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

API_KEY = "changeme"  # Replace with secure value in production
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def api_key_auth(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API Key")
