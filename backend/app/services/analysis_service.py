import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models import (
    Stock, DailyRun, StockSnapshot, EarningsEvent, 
    NewsArticle, Filing, OptionsSnapshot, AnalysisReport,
    DailyRunStatus, AnalysisType, EventType
)
from app.services.market_data import MarketDataService
from app.services.news_service import NewsService
from app.services.openai_service import OpenAIService

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.market_service = MarketDataService()
        self.news_service = NewsService()
    
    async def run_daily_analysis(self, run_id: int):
        """Run comprehensive daily analysis for configured stocks"""
        try:
            # Get the daily run record
            daily_run = self.db.query(DailyRun).filter(DailyRun.id == run_id).first()
            if not daily_run:
                return
            
            # Update status to running
            daily_run.status = DailyRunStatus.RUNNING
            self.db.commit()
            
            # Get configuration
            from app.models import UserConfig
            config = self.db.query(UserConfig).first()
            if not config:
                config = UserConfig(top_n=20, universe="US_LARGE_CAP", custom_tickers=[])
                self.db.add(config)
                self.db.commit()
            
            # Get top stocks by market cap
            top_stocks = await self.market_service.get_top_stocks_by_market_cap(config.top_n)
            
            # Add custom tickers
            all_symbols = list(set([stock['symbol'] for stock in top_stocks] + config.custom_tickers))
            
            # Process each stock
            for i, symbol in enumerate(all_symbols):
                try:
                    await self._analyze_single_stock(
                        symbol, daily_run, rank=i+1
                    )
                except Exception as e:
                    print(f"Error analyzing {symbol}: {e}")
                    continue
            
            # Update run status to completed
            daily_run.status = DailyRunStatus.COMPLETED
            daily_run.completed_at = datetime.now()
            self.db.commit()
            
        except Exception as e:
            # Update run status to failed
            if daily_run:
                daily_run.status = DailyRunStatus.FAILED
                daily_run.notes = str(e)
                self.db.commit()
            print(f"Daily analysis failed: {e}")
    
    async def run_on_demand_analysis(self, stock_id: int, symbol: str):
        """Run on-demand analysis for a single stock"""
        try:
            # Create a dummy daily run for on-demand analysis
            daily_run = DailyRun(
                run_date=datetime.now().date(),
                universe="ON_DEMAND",
                status=DailyRunStatus.COMPLETED,
                completed_at=datetime.now()
            )
            self.db.add(daily_run)
            self.db.commit()
            
            # Analyze the stock
            await self._analyze_single_stock(
                symbol, daily_run, rank=1, analysis_type=AnalysisType.ON_DEMAND
            )
            
        except Exception as e:
            print(f"On-demand analysis failed for {symbol}: {e}")
            self.db.rollback()
    
    async def _analyze_single_stock(self, symbol: str, daily_run: DailyRun, 
                                   rank: int, analysis_type: AnalysisType = AnalysisType.DAILY_AUTO):
        """Analyze a single stock and store results"""
        
        # Get or create stock record
        stock = self.db.query(Stock).filter(Stock.symbol == symbol).first()
        if not stock:
            stock = Stock(symbol=symbol, name=symbol, is_tracked=True)
            self.db.add(stock)
            self.db.commit()
            self.db.refresh(stock)
        
        # Fetch market data
        stock_data = await self.market_service.get_stock_data(symbol)
        if not stock_data:
            return
        
        # Update stock info
        stock.name = stock_data.get('name', symbol)
        stock.sector = stock_data.get('sector')
        stock.industry = stock_data.get('industry')
        
        # Create stock snapshot
        snapshot = StockSnapshot(
            daily_run_id=daily_run.id,
            stock_id=stock.id,
            sequence=rank,
            market_cap=stock_data['market_cap'],
            price=stock_data['price'],
            open_price=stock_data.get('open_price', stock_data['price']),
            day_high=stock_data.get('day_high', stock_data['price']),
            day_low=stock_data.get('day_low', stock_data['price']),
            volume=stock_data.get('volume', 0),
            high_52w=stock_data.get('high_52w', stock_data['price']),
            low_52w=stock_data.get('low_52w', stock_data['price']),
            pe_ratio=stock_data.get('pe_ratio'),
            dividend_yield=stock_data.get('dividend_yield'),
            beta=stock_data.get('beta'),
            as_of=stock_data['as_of']
        )
        self.db.add(snapshot)
        
        # Fetch earnings data
        earnings_data = await self.market_service.get_earnings_data(symbol)
        
        # Store earnings events
        for earning in earnings_data.get('upcoming', []):
            earnings_event = EarningsEvent(
                stock_id=stock.id,
                source_run_id=daily_run.id if analysis_type == AnalysisType.DAILY_AUTO else None,
                event_type=EventType.UPCOMING,
                fiscal_period=earning.get('fiscal_period', 'Q1'),
                event_date=earning['event_date'],
                eps_estimate=earning.get('eps_estimate')
            )
            self.db.add(earnings_event)
        
        for earning in earnings_data.get('historical', []):
            earnings_event = EarningsEvent(
                stock_id=stock.id,
                source_run_id=daily_run.id if analysis_type == AnalysisType.DAILY_AUTO else None,
                event_type=EventType.HISTORICAL,
                event_date=earning['event_date'],
                eps_actual=earning.get('eps_actual'),
                eps_estimate=earning.get('eps_estimate'),
                surprise_percent=earning.get('surprise_percent')
            )
            self.db.add(earnings_event)
        
        # Fetch news
        news_data = await self.news_service.get_stock_news(symbol)
        
        # Store news articles
        for article in news_data:
            news_article = NewsArticle(
                stock_id=stock.id,
                source_run_id=daily_run.id if analysis_type == AnalysisType.DAILY_AUTO else None,
                title=article['title'],
                url=article['url'],
                published_at=article['published_at'],
                source=article['source'],
                summary_raw=article.get('summary'),
                is_issue_flag=article.get('is_issue_flag', False)
            )
            self.db.add(news_article)
        
        # Fetch options data
        options_data = await self.market_service.get_options_data(symbol)
        
        # Store options snapshot
        if options_data:
            # Store the best covered call and cash-secured put options
            best_call = options_data['calls'][0] if options_data['calls'] else None
            best_put = options_data['puts'][-1] if options_data['puts'] else None
            
            if best_call and best_put:
                options_snapshot = OptionsSnapshot(
                    stock_id=stock.id,
                    source_run_id=daily_run.id if analysis_type == AnalysisType.DAILY_AUTO else None,
                    underlying_price=options_data['underlying_price'],
                    days_to_expiry=options_data['days_to_expiry'],
                    call_strike=best_call['strike'],
                    put_strike=best_put['strike'],
                    call_bid=best_call['bid'],
                    put_bid=best_put['bid'],
                    implied_vol=best_call.get('implied_vol'),
                    delta_call=best_call.get('delta'),
                    delta_put=best_put.get('delta')
                )
                self.db.add(options_snapshot)
        
        # Prepare data for OpenAI analysis
        analysis_data = {
            'symbol': symbol,
            'name': stock_data['name'],
            'quote': {
                'price': stock_data['price'],
                'market_cap': stock_data['market_cap'],
                'pe_ratio': stock_data.get('pe_ratio'),
                'dividend_yield': stock_data.get('dividend_yield'),
                'beta': stock_data.get('beta'),
                'high_52w': stock_data.get('high_52w'),
                'low_52w': stock_data.get('low_52w')
            },
            'earnings': earnings_data,
            'news': [
                {
                    'title': article['title'],
                    'published_at': article['published_at'].isoformat(),
                    'source': article['source'],
                    'is_issue_flag': article.get('is_issue_flag', False)
                } for article in news_data[:5]  # Limit to 5 recent articles
            ],
            'options': options_data,
            'data_quality': {
                'has_options': options_data is not None,
                'has_recent_news': len(news_data) > 0,
                'has_earnings_data': len(earnings_data.get('upcoming', [])) > 0 or len(earnings_data.get('historical', [])) > 0,
                'has_fundamentals': all([
                    stock_data.get('pe_ratio') is not None,
                    stock_data.get('beta') is not None
                ])
            }
        }
        
        # Get OpenAI analysis
        openai_service = OpenAIService(self.db)
        ai_analysis = await openai_service.analyze_stock(analysis_data)
        
        # Create analysis report
        report = AnalysisReport(
            stock_id=stock.id,
            source_run_id=daily_run.id if analysis_type == AnalysisType.DAILY_AUTO else None,
            analysis_type=analysis_type,
            llm_model="gpt-4",
            summary_markdown=ai_analysis.get('summary_markdown', 'Analysis completed'),
            entry_rating=ai_analysis['entry']['rating'],
            entry_comment=ai_analysis['entry']['rationale'],
            covered_call_rating=ai_analysis['covered_call']['rating'],
            covered_call_comment=ai_analysis['covered_call']['rationale'],
            secured_put_rating=ai_analysis['secured_put']['rating'],
            secured_put_comment=ai_analysis['secured_put']['rationale'],
            risk_flags=ai_analysis.get('risks_and_issues', [])
        )
        self.db.add(report)
        
        # Commit all changes
        self.db.commit()