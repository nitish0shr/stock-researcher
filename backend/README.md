# Stock Research Backend

FastAPI backend for the autonomous stock research platform.

## Features

- **Real-time Market Data**: Integration with financial data providers
- **AI-Powered Analysis**: OpenAI GPT-4 integration for comprehensive stock analysis
- **Options Analysis**: Covered calls and cash-secured put strategies
- **News Integration**: Recent news and sentiment analysis
- **Scheduled Analysis**: Daily automated research runs
- **RESTful API**: Clean API design with comprehensive endpoints

## Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: OpenAI GPT-4
- **Data Sources**: Yahoo Finance, News APIs
- **Deployment**: Docker-ready

## Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database configuration
   ```

4. **Set up the database**
   ```bash
   # Create PostgreSQL database
   createdb stockresearch
   
   # Run database migrations
   alembic upgrade head
   ```

5. **Run the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t stock-research-backend .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 --env-file .env stock-research-backend
   ```

## API Documentation

Once the server is running, you can access:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI analysis | Yes |
| `MARKET_DATA_API_KEY` | Market data provider API key | No |
| `NEWS_API_KEY` | News API key | No |
| `OPTIONS_API_KEY` | Options data API key | No |
| `ENCRYPTION_PASSWORD` | Password for encrypting sensitive data | Yes |

### API Endpoints

#### Runs Management
- `POST /api/runs/run_daily` - Trigger daily analysis run
- `GET /api/runs/latest` - Get latest completed run
- `GET /api/runs/{id}` - Get specific run details

#### Stock Analysis
- `GET /api/stocks` - List all tracked stocks
- `GET /api/stocks/{symbol}` - Get detailed stock information
- `POST /api/analyze_stock` - Trigger on-demand analysis
- `GET /api/stocks/sectors` - Get available sectors

#### Configuration
- `GET /api/config/config` - Get current configuration
- `POST /api/config/config` - Update configuration
- `GET /api/config/secrets` - Get API key status
- `POST /api/config/secrets` - Update API keys

## Database Schema

The application uses the following main tables:

- `stocks` - Stock basic information
- `daily_runs` - Daily analysis execution tracking
- `stock_snapshots` - Price and fundamental data snapshots
- `analysis_reports` - AI-generated analysis reports
- `news_articles` - Recent news articles
- `earnings_events` - Earnings calendar and history
- `options_snapshots` - Options chain data
- `user_config` - Platform configuration
- `user_secrets` - Encrypted API keys

## Daily Analysis Workflow

1. **Trigger**: Scheduled run or manual trigger
2. **Stock Selection**: Get top N stocks by market cap + custom tickers
3. **Data Collection**: 
   - Fetch current market data
   - Get recent news
   - Retrieve earnings information
   - Collect options data
4. **AI Analysis**: Send structured data to OpenAI for analysis
5. **Report Generation**: Store comprehensive analysis report
6. **Notification**: Update run status

## Security Features

- **Encrypted Storage**: API keys are encrypted at rest
- **No Key Exposure**: Never expose full API keys in responses
- **Secure Headers**: Proper CORS and security headers
- **Input Validation**: Comprehensive request validation

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black app/
flake8 app/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "migration description"

# Apply migrations
alembic upgrade head

# Downgrade migration
alembic downgrade -1
```

## Troubleshooting

### Common Issues

1. **Database Connection**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL format
   - Verify database exists

2. **API Key Issues**
   - Verify API keys are valid
   - Check rate limits
   - Ensure proper permissions

3. **CORS Issues**
   - Update allowed origins in main.py
   - Check frontend API URL configuration

### Logging

The application logs to:
- Console output for development
- `/app/logs/` directory in production

## Production Deployment

### Environment Requirements

- Python 3.11+
- PostgreSQL 12+
- Redis (optional, for caching)
- Sufficient API quotas for data providers

### Scaling Considerations

- Use connection pooling for database
- Implement rate limiting for API calls
- Consider Redis for caching frequent requests
- Use background tasks for long-running analysis

## License

This project is for educational and research purposes only. See LICENSE file for details.