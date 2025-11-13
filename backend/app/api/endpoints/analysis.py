from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict
from app.database import get_db
from app.models import Stock, AnalysisReport, AnalysisType
from app.schemas.analysis_schemas import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import AnalysisService

router = APIRouter()

@router.post("/analyze_stock", response_model=AnalysisResponse)
async def analyze_stock(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger on-demand analysis for a specific stock"""
    symbol = request.symbol.upper()
    
    # Check if stock exists
    stock = db.query(Stock).filter(Stock.symbol == symbol).first()
    if not stock:
        # Create new stock entry
        stock = Stock(symbol=symbol, name=symbol, is_tracked=False)
        db.add(stock)
        db.commit()
        db.refresh(stock)
    
    # Start analysis in background
    analysis_service = AnalysisService(db)
    background_tasks.add_task(
        analysis_service.run_on_demand_analysis,
        stock.id,
        symbol
    )
    
    return {"message": f"Analysis started for {symbol}", "symbol": symbol}

@router.get("/latest_analysis/{symbol}", response_model=AnalysisResponse)
async def get_latest_analysis(symbol: str, db: Session = Depends(get_db)):
    """Get the latest analysis for a stock"""
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    latest_analysis = db.query(AnalysisReport).filter(
        AnalysisReport.stock_id == stock.id
    ).order_by(AnalysisReport.created_at.desc()).first()
    
    if not latest_analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this stock")
    
    return {
        "symbol": symbol,
        "analysis": latest_analysis,
        "message": "Analysis retrieved successfully"
    }