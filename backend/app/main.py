from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, create_tables
from app.services.market_data import MarketDataService
from app.services.news_service import NewsService
from app.services.openai_service import OpenAIService
from app.services.analysis_service import AnalysisService
from app.api.endpoints import stocks, runs, config, analysis
import uvicorn

# Create database tables on startup
create_tables()

app = FastAPI(
    title="Stock Research API",
    description="Autonomous stock research and analysis platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(runs.router, prefix="/api/runs", tags=["runs"])
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])

@app.get("/")
async def root():
    return {"message": "Stock Research API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)