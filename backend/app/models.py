from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, Boolean, Text, ForeignKey, JSON, Enum, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class EntryRating(enum.Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    AVOID = "avoid"

class StrategyRating(enum.Enum):
    ATTRACTIVE = "attractive"
    NEUTRAL = "neutral"
    UNATTRACTIVE = "unattractive"

class DailyRunStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class AnalysisType(enum.Enum):
    DAILY_AUTO = "daily_auto"
    ON_DEMAND = "on_demand"

class EventType(enum.Enum):
    UPCOMING = "upcoming"
    HISTORICAL = "historical"

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    exchange = Column(String)
    currency = Column(String, default="USD")
    sector = Column(String)
    industry = Column(String)
    is_tracked = Column(Boolean, default=True)
    
    # Relationships
    snapshots = relationship("StockSnapshot", back_populates="stock")
    earnings = relationship("EarningsEvent", back_populates="stock")
    news = relationship("NewsArticle", back_populates="stock")
    filings = relationship("Filing", back_populates="stock")
    options = relationship("OptionsSnapshot", back_populates="stock")
    analyses = relationship("AnalysisReport", back_populates="stock")

class DailyRun(Base):
    __tablename__ = "daily_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    run_date = Column(Date, nullable=False)
    universe = Column(String, nullable=False)
    status = Column(Enum(DailyRunStatus), default=DailyRunStatus.PENDING)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    notes = Column(Text)
    
    __table_args__ = (UniqueConstraint('run_date', 'universe'),)
    
    # Relationships
    snapshots = relationship("StockSnapshot", back_populates="daily_run")
    news = relationship("NewsArticle", back_populates="daily_run")
    filings = relationship("Filing", back_populates="daily_run")
    options = relationship("OptionsSnapshot", back_populates="daily_run")
    analyses = relationship("AnalysisReport", back_populates="daily_run")

class StockSnapshot(Base):
    __tablename__ = "stock_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    daily_run_id = Column(Integer, ForeignKey("daily_runs.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    sequence = Column(Integer, nullable=False)  # rank order
    market_cap = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)
    open_price = Column(Numeric)
    day_high = Column(Numeric)
    day_low = Column(Numeric)
    volume = Column(Integer)
    high_52w = Column(Numeric)
    low_52w = Column(Numeric)
    pe_ratio = Column(Numeric)
    dividend_yield = Column(Numeric)
    beta = Column(Numeric)
    as_of = Column(DateTime, nullable=False)
    
    # Relationships
    daily_run = relationship("DailyRun", back_populates="snapshots")
    stock = relationship("Stock", back_populates="snapshots")

class EarningsEvent(Base):
    __tablename__ = "earnings_events"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    source_run_id = Column(Integer, ForeignKey("daily_runs.id"), nullable=True)
    event_type = Column(Enum(EventType), nullable=False)
    fiscal_period = Column(String)
    event_date = Column(Date, nullable=False)
    eps_actual = Column(Numeric)
    eps_estimate = Column(Numeric)
    surprise_percent = Column(Numeric)
    
    # Relationships
    stock = relationship("Stock", back_populates="earnings")

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    source_run_id = Column(Integer, ForeignKey("daily_runs.id"), nullable=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    source = Column(String)
    summary_raw = Column(Text)
    is_issue_flag = Column(Boolean, default=False)
    
    # Relationships
    stock = relationship("Stock", back_populates="news")
    daily_run = relationship("DailyRun", back_populates="news")

class Filing(Base):
    __tablename__ = "filings"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    source_run_id = Column(Integer, ForeignKey("daily_runs.id"), nullable=True)
    filing_type = Column(String, nullable=False)  # 10-K, 10-Q, etc.
    period_end = Column(Date)
    file_url = Column(String, nullable=False)
    file_date = Column(Date, nullable=False)
    
    # Relationships
    stock = relationship("Stock", back_populates="filings")
    daily_run = relationship("DailyRun", back_populates="filings")

class OptionsSnapshot(Base):
    __tablename__ = "options_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    source_run_id = Column(Integer, ForeignKey("daily_runs.id"), nullable=True)
    underlying_price = Column(Numeric, nullable=False)
    days_to_expiry = Column(Integer, nullable=False)
    call_strike = Column(Numeric)
    put_strike = Column(Numeric)
    call_bid = Column(Numeric)
    put_bid = Column(Numeric)
    implied_vol = Column(Numeric)
    delta_call = Column(Numeric)
    delta_put = Column(Numeric)
    
    # Relationships
    stock = relationship("Stock", back_populates="options")
    daily_run = relationship("DailyRun", back_populates="options")

class AnalysisReport(Base):
    __tablename__ = "analysis_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    source_run_id = Column(Integer, ForeignKey("daily_runs.id"), nullable=True)
    analysis_type = Column(Enum(AnalysisType), nullable=False)
    llm_model = Column(String)
    raw_prompt = Column(Text)
    raw_response = Column(Text)
    summary_markdown = Column(Text, nullable=False)
    entry_rating = Column(Enum(EntryRating))
    entry_comment = Column(Text)
    covered_call_rating = Column(Enum(StrategyRating))
    covered_call_comment = Column(Text)
    secured_put_rating = Column(Enum(StrategyRating))
    secured_put_comment = Column(Text)
    risk_flags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    stock = relationship("Stock", back_populates="analyses")
    daily_run = relationship("DailyRun", back_populates="analyses")

class UserConfig(Base):
    __tablename__ = "user_config"
    
    id = Column(Integer, primary_key=True)
    top_n = Column(Integer, default=20)
    universe = Column(String, default="US_LARGE_CAP")
    custom_tickers = Column(JSON, default=list)
    daily_run_time_local = Column(String, default="09:00")
    time_zone = Column(String, default="America/New_York")

class UserSecrets(Base):
    __tablename__ = "user_secrets"
    
    id = Column(Integer, primary_key=True)
    openai_api_key_encrypted = Column(Text)
    market_data_api_key_encrypted = Column(Text)
    news_api_key_encrypted = Column(Text)
    options_api_key_encrypted = Column(Text)