import aiohttp
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import yfinance as yf

class MarketDataService:
    def __init__(self):
        self.api_key = os.getenv("MARKET_DATA_API_KEY")
        self.base_url = "https://api.polygon.io"  # Using Polygon.io as default
    
    async def get_top_stocks_by_market_cap(self, limit: int = 20) -> List[Dict]:
        """Get top stocks by market cap"""
        try:
            # For demonstration, using a predefined list of large-cap stocks
            # In production, this would call the actual API
            large_cap_stocks = [
                "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM",
                "JNJ", "V", "PG", "UNH", "HD", "MA", "DIS", "PYPL", "ADBE",
                "NFLX", "CRM", "PEP"
            ]
            
            stock_data = []
            for symbol in large_cap_stocks[:limit]:
                data = await self.get_stock_data(symbol)
                if data:
                    stock_data.append(data)
            
            # Sort by market cap
            stock_data.sort(key=lambda x: x.get('market_cap', 0), reverse=True)
            return stock_data
            
        except Exception as e:
            print(f"Error fetching top stocks: {e}")
            return []
    
    async def get_stock_data(self, symbol: str) -> Optional[Dict]:
        """Get comprehensive stock data"""
        try:
            # Using yfinance as a fallback for demonstration
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info:
                return None
            
            # Get current quote
            hist = ticker.history(period="1d")
            current_price = hist['Close'].iloc[-1] if not hist.empty else info.get('currentPrice', 0)
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'exchange': info.get('exchange', 'NASDAQ'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'market_cap': info.get('marketCap', 0),
                'price': current_price,
                'open_price': hist['Open'].iloc[-1] if not hist.empty else current_price,
                'day_high': hist['High'].iloc[-1] if not hist.empty else current_price,
                'day_low': hist['Low'].iloc[-1] if not hist.empty else current_price,
                'volume': int(hist['Volume'].iloc[-1]) if not hist.empty else 0,
                'high_52w': info.get('fiftyTwoWeekHigh', current_price),
                'low_52w': info.get('fiftyTwoWeekLow', current_price),
                'pe_ratio': info.get('trailingPE'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta'),
                'as_of': datetime.now()
            }
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    async def get_earnings_data(self, symbol: str) -> Dict:
        """Get earnings data"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get earnings calendar
            calendar = ticker.calendar
            earnings_data = {
                'upcoming': [],
                'historical': []
            }
            
            if calendar is not None and not calendar.empty:
                for date, row in calendar.iterrows():
                    earnings_data['upcoming'].append({
                        'event_date': date,
                        'eps_estimate': row.get('EPS Estimate'),
                        'fiscal_period': row.get('Fiscal Quarter', 'Q1')
                    })
            
            # Get historical earnings
            earnings_history = ticker.earnings_dates
            if earnings_history is not None and not earnings_history.empty:
                for date, row in earnings_history.head(4).iterrows():
                    earnings_data['historical'].append({
                        'event_date': date,
                        'eps_actual': row.get('EPS Actual'),
                        'eps_estimate': row.get('EPS Estimate'),
                        'surprise_percent': row.get('Surprise %')
                    })
            
            return earnings_data
            
        except Exception as e:
            print(f"Error fetching earnings for {symbol}: {e}")
            return {'upcoming': [], 'historical': []}
    
    async def get_options_data(self, symbol: str) -> Optional[Dict]:
        """Get options data for covered calls and cash-secured puts"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get options expiration dates
            exp_dates = ticker.options
            if not exp_dates:
                return None
            
            # Get options for nearest expiration (30-60 days out)
            target_date = None
            current_date = datetime.now().date()
            
            for exp_date in exp_dates:
                exp_date_obj = datetime.strptime(exp_date, '%Y-%m-%d').date()
                days_to_expiry = (exp_date_obj - current_date).days
                
                if 30 <= days_to_expiry <= 60:
                    target_date = exp_date
                    break
            
            if not target_date:
                target_date = exp_dates[0]  # Use nearest expiration
            
            # Get options chain
            opt = ticker.option_chain(target_date)
            
            if opt.calls is None or opt.puts is None:
                return None
            
            current_price = ticker.info.get('currentPrice', 0)
            
            # Find near-the-money options
            calls = opt.calls[opt.calls['strike'] >= current_price].head(3)
            puts = opt.puts[opt.puts['strike'] <= current_price].tail(3)
            
            options_data = {
                'underlying_price': current_price,
                'expiration_date': target_date,
                'days_to_expiry': (datetime.strptime(target_date, '%Y-%m-%d').date() - current_date).days,
                'calls': [],
                'puts': []
            }
            
            # Process calls (for covered calls)
            for _, call in calls.iterrows():
                options_data['calls'].append({
                    'strike': call['strike'],
                    'bid': call['bid'],
                    'ask': call['ask'],
                    'implied_vol': call.get('impliedVolatility'),
                    'delta': call.get('delta'),
                    'premium': call['bid']  # Use bid price
                })
            
            # Process puts (for cash-secured puts)
            for _, put in puts.iterrows():
                options_data['puts'].append({
                    'strike': put['strike'],
                    'bid': put['bid'],
                    'ask': put['ask'],
                    'implied_vol': put.get('impliedVolatility'),
                    'delta': put.get('delta'),
                    'premium': put['bid']  # Use bid price
                })
            
            return options_data
            
        except Exception as e:
            print(f"Error fetching options for {symbol}: {e}")
            return None