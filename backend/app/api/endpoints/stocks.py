from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.database import get_db
from app.models import Stock, AnalysisReport, NewsArticle, Filing, OptionsSnapshot
from app.schemas.stock_schemas import StockDetailResponse, StockSummary

router = APIRouter()

@router.get("/", response_model=List[StockSummary])
async def list_stocks(
    limit: int = 50,
    offset: int = 0,
    sector: Optional[str] = None,
    entry_rating: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List stocks with optional filtering"""
    query = db.query(Stock).filter(Stock.is_tracked == True)
    
    if sector:
        query = query.filter(Stock.sector == sector)
    
    if entry_rating:
        query = query.join(AnalysisReport).filter(
            AnalysisReport.entry_rating == entry_rating
        )
    
    stocks = query.offset(offset).limit(limit).all()
    return stocks

@router.get("/{symbol}", response_model=StockDetailResponse)
async def get_stock_detail(symbol: str, db: Session = Depends(get_db)):
    """Get detailed information for a specific stock"""
    stock = db.query(Stock).filter(
        Stock.symbol == symbol.upper()
    ).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Get latest analysis
    latest_analysis = db.query(AnalysisReport).filter(
        AnalysisReport.stock_id == stock.id
    ).order_by(AnalysisReport.created_at.desc()).first()
    
    # Get recent news
    recent_news = db.query(NewsArticle).filter(
        NewsArticle.stock_id == stock.id
    ).order_by(NewsArticle.published_at.desc()).limit(10).all()
    
    # Get latest filings
    latest_filings = db.query(Filing).filter(
        Filing.stock_id == stock.id
    ).order_by(Filing.file_date.desc()).limit(5).all()
    
    # Get latest options snapshot
    latest_options = db.query(OptionsSnapshot).filter(
        OptionsSnapshot.stock_id == stock.id
    ).order_by(OptionsSnapshot.id.desc()).first()
    
    return {
        "stock": stock,
        "latest_analysis": latest_analysis,
        "recent_news": recent_news,
        "latest_filings": latest_filings,
        "latest_options": latest_options
    }

@router.get("/sectors", response_model=List[str])
async def get_sectors(db: Session = Depends(get_db)):
    """Get list of all sectors"""
    sectors = db.query(Stock.sector).distinct().filter(
        Stock.sector.isnot(None)
    ).all()
    return [sector[0] for sector in sectors if sector[0]]