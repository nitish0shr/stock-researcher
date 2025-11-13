from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models import EntryRating, StrategyRating

class StockSummary(BaseModel):
    id: int
    symbol: str
    name: str
    exchange: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    is_tracked: bool
    
    class Config:
        from_attributes = True

class StockDetailResponse(BaseModel):
    stock: StockSummary
    latest_analysis: Optional[dict] = None
    recent_news: List[dict] = []
    latest_filings: List[dict] = []
    latest_options: Optional[dict] = None
    
    class Config:
        from_attributes = True