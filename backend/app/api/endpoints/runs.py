from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import DailyRun, DailyRunStatus
from app.schemas.run_schemas import DailyRunResponse, DailyRunSummary
from app.services.analysis_service import AnalysisService
import datetime

router = APIRouter()

@router.post("/run_daily", response_model=DailyRunResponse)
async def trigger_daily_run(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger a new daily analysis run"""
    # Check if there's already a running or pending run for today
    today = datetime.date.today()
    existing_run = db.query(DailyRun).filter(
        DailyRun.run_date == today,
        DailyRun.status.in_([DailyRunStatus.PENDING, DailyRunStatus.RUNNING])
    ).first()
    
    if existing_run:
        raise HTTPException(
            status_code=400,
            detail=f"A run for {today} is already {existing_run.status.value}"
        )
    
    # Create new daily run record
    new_run = DailyRun(
        run_date=today,
        universe="US_LARGE_CAP",
        status=DailyRunStatus.PENDING
    )
    db.add(new_run)
    db.commit()
    db.refresh(new_run)
    
    # Start the analysis in background
    analysis_service = AnalysisService(db)
    background_tasks.add_task(analysis_service.run_daily_analysis, new_run.id)
    
    return new_run

@router.get("/latest", response_model=DailyRunSummary)
async def get_latest_run(db: Session = Depends(get_db)):
    """Get the latest completed daily run"""
    latest_run = db.query(DailyRun).filter(
        DailyRun.status == DailyRunStatus.COMPLETED
    ).order_by(DailyRun.run_date.desc()).first()
    
    if not latest_run:
        raise HTTPException(status_code=404, detail="No completed runs found")
    
    return latest_run

@router.get("/{run_id}", response_model=DailyRunResponse)
async def get_run_by_id(run_id: int, db: Session = Depends(get_db)):
    """Get a specific daily run by ID"""
    run = db.query(DailyRun).filter(DailyRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.get("/", response_model=List[DailyRunSummary])
async def list_runs(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List recent daily runs"""
    runs = db.query(DailyRun).order_by(
        DailyRun.run_date.desc()
    ).offset(offset).limit(limit).all()
    return runs