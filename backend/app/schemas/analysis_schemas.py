from pydantic import BaseModel
from typing import Optional, Dict, Any

class AnalysisRequest(BaseModel):
    symbol: str

class AnalysisResponse(BaseModel):
    symbol: str
    message: str
    analysis: Optional[Dict[str, Any]] = None