import aiohttp
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import feedparser

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    async def get_stock_news(self, symbol: str, days_back: int = 7) -> List[Dict]:
        """Get recent news for a stock"""
        try:
            # For demonstration, using a mock news service
            # In production, this would call NewsAPI or similar service
            
            # Mock news data for demonstration
            mock_news = [
                {
                    'title': f"{symbol} Reports Strong Q3 Earnings Beat",
                    'url': f'https://example.com/{symbol.lower()}-earnings',
                    'published_at': datetime.now() - timedelta(days=2),
                    'source': 'Financial Times',
                    'summary': f'{symbol} exceeded analyst expectations with strong revenue growth.',
                    'is_issue_flag': False
                },
                {
                    'title': f"Market Analysts Upgrade {symbol} Price Target",
                    'url': f'https://example.com/{symbol.lower()}-upgrade',
                    'published_at': datetime.now() - timedelta(days=5),
                    'source': 'Bloomberg',
                    'summary': f'Analysts cite strong fundamentals and market position for {symbol}.',
                    'is_issue_flag': False
                },
                {
                    'title': f"{symbol} Faces Regulatory Scrutiny in Key Market",
                    'url': f'https://example.com/{symbol.lower()}-regulatory',
                    'published_at': datetime.now() - timedelta(days=1),
                    'source': 'Reuters',
                    'summary': f'Regulatory concerns may impact {symbol} operations in key markets.',
                    'is_issue_flag': True
                }
            ]
            
            return mock_news[:2]  # Return first 2 for demo
            
        except Exception as e:
            print(f"Error fetching news for {symbol}: {e}")
            return []
    
    async def get_general_market_news(self, limit: int = 10) -> List[Dict]:
        """Get general market news"""
        try:
            # Mock market news
            market_news = [
                {
                    'title': "Fed Signals Potential Rate Cut in Coming Months",
                    'url': 'https://example.com/fed-rates',
                    'published_at': datetime.now() - timedelta(hours=6),
                    'source': 'CNBC',
                    'summary': 'Federal Reserve hints at monetary policy adjustments.',
                    'is_issue_flag': False
                },
                {
                    'title': "Tech Sector Shows Resilience Amid Market Volatility",
                    'url': 'https://example.com/tech-sector',
                    'published_at': datetime.now() - timedelta(days=1),
                    'source': 'Wall Street Journal',
                    'summary': 'Technology stocks demonstrate strong performance despite market uncertainty.',
                    'is_issue_flag': False
                }
            ]
            
            return market_news
            
        except Exception as e:
            print(f"Error fetching market news: {e}")
            return []
    
    def _is_issue_flag(self, title: str, summary: str) -> bool:
        """Determine if news article should be flagged as an issue/risk"""
        issue_keywords = [
            'lawsuit', 'scandal', 'fraud', 'investigation', 'penalty',
            'fine', 'violation', 'breach', 'downgrade', 'cut',
            'layoffs', 'restructuring', 'bankruptcy', 'default'
        ]
        
        text = (title + ' ' + summary).lower()
        return any(keyword in text for keyword in issue_keywords)