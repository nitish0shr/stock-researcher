from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional
from app.models import DailyRunStatus

class DailyRunSummary(BaseModel):
    id: int
    run_date: date
    universe: str
    status: DailyRunStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

class DailyRunResponse(DailyRunSummary):
    # Add any additional fields needed for detailed response
    pass