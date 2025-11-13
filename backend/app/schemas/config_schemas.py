from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.models import EntryRating, StrategyRating

class ConfigResponse(BaseModel):
    top_n: int
    universe: str
    custom_tickers: List[str]
    daily_run_time_local: str
    time_zone: str
    
    class Config:
        from_attributes = True

class ConfigUpdate(BaseModel):
    top_n: Optional[int] = None
    universe: Optional[str] = None
    custom_tickers: Optional[List[str]] = None
    daily_run_time_local: Optional[str] = None
    time_zone: Optional[str] = None

class SecretsResponse(BaseModel):
    openai_key_set: bool
    market_data_key_set: bool
    news_key_set: bool
    options_key_set: bool

class SecretsUpdate(BaseModel):
    openai_api_key: Optional[str] = None
    market_data_api_key: Optional[str] = None
    news_api_key: Optional[str] = None
    options_api_key: Optional[str] = None