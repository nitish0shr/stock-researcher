# Autonomous Stock Research Platform

A production-ready, AI-powered stock research platform that automatically analyzes top stocks by market cap and provides comprehensive investment insights.

## 🚀 Features

### 🤖 Autonomous Analysis
- **Daily Automated Research**: Automatically analyzes top N stocks by market cap
- **On-Demand Analysis**: Instant analysis for any ticker symbol
- **AI-Powered Insights**: GPT-4 powered research reports
- **Real-time Data**: Live market data and news integration

### 📊 Comprehensive Analysis
- **Fundamental Analysis**: Market cap, P/E ratios, dividends, beta
- **Technical Indicators**: 52-week highs/lows, volume analysis
- **Options Strategies**: Covered calls and cash-secured put analysis
- **News & Sentiment**: Recent news with risk/issue flagging
- **Earnings Calendar**: Upcoming and historical earnings data

### 🎨 High-End UI
- **Modern Design**: Clean, professional interface
- **Responsive**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Real-time data visualization
- **Dark Mode**: Automatic theme switching
- **Smooth UX**: Loading states, error handling, notifications

### ⚙️ Configuration & Management
- **API Key Management**: Secure storage and testing
- **Custom Tickers**: Add your own stocks to track
- **Scheduled Runs**: Configure daily analysis timing
- **Settings Panel**: Easy platform configuration

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.11
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Integration**: OpenAI GPT-4 for analysis
- **Data Sources**: Yahoo Finance, News APIs
- **Security**: Encrypted API keys, CORS protection

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with shadcn/ui
- **State Management**: TanStack React Query
- **Charts**: Recharts for data visualization

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Node.js 18+ and Python 3.11+
- PostgreSQL 12+
- OpenAI API key

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stock-research-platform
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API keys
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Installation

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## 📖 Usage

### Initial Setup
1. **Open Settings**: Navigate to the settings page
2. **Add OpenAI API Key**: Required for AI analysis
3. **Configure Preferences**: Set top N stocks, custom tickers
4. **Test Connections**: Verify API key connectivity

### Daily Analysis
1. **Trigger Analysis**: Click "Run Analysis" or wait for scheduled run
2. **View Results**: Browse the dashboard for latest insights
3. **Drill Down**: Click any stock for detailed analysis
4. **Review Reports**: Read AI-generated research reports

### On-Demand Analysis
1. **Quick Analysis**: Use the dashboard input field
2. **Enter Ticker**: Type any stock symbol
3. **Get Insights**: Instant AI-powered analysis

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/stockresearch

# APIs
OPENAI_API_KEY=sk-...
MARKET_DATA_API_KEY=...
NEWS_API_KEY=...
OPTIONS_API_KEY=...

# Security
ENCRYPTION_PASSWORD=your-secure-password
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Platform Settings
- **Top N Stocks**: Number of large-cap stocks to analyze (default: 20)
- **Custom Tickers**: Additional stocks to track
- **Analysis Schedule**: Daily run time configuration
- **Time Zone**: Your local time zone

## 📊 Data Sources

### Market Data
- **Yahoo Finance**: Real-time quotes and fundamentals
- **Market Cap Rankings**: Top stocks by market capitalization
- **Options Chains**: Near-the-money options data

### News & Information
- **News APIs**: Recent articles and press releases
- **Risk Detection**: Automatic issue/controversy flagging
- **Earnings Calendar**: Upcoming and historical earnings

### AI Analysis
- **GPT-4 Integration**: Advanced language model analysis
- **Structured Reports**: Markdown-formatted insights
- **Strategy Ratings**: Entry, covered call, and CSP recommendations

## 🔒 Security

### API Key Management
- **Encrypted Storage**: All keys encrypted at rest
- **No Exposure**: Never displayed in UI or logs
- **Status Indicators**: Only show if keys are set
- **Connection Testing**: Verify key validity

### Data Protection
- **HTTPS Only**: Secure communication
- **CORS Configuration**: Controlled access
- **Input Validation**: Comprehensive request validation
- **No Trading**: Research platform only

## 🎯 Investment Strategies

### Entry Analysis
- **Strong Buy**: Compelling investment opportunity
- **Buy**: Favorable conditions for entry
- **Hold**: Maintain current position
- **Avoid**: Unfavorable risk/reward

### Covered Calls
- **Attractive**: High premium, good strike selection
- **Neutral**: Standard opportunity
- **Unattractive**: Low premium or poor timing

### Cash-Secured Puts
- **Attractive**: Good entry price with decent premium
- **Neutral**: Standard put selling opportunity
- **Unattractive**: Low premium or unfavorable strike

## 📱 User Interface

### Dashboard
- **Live Data**: Real-time stock information
- **Filter & Search**: Find stocks by criteria
- **Quick Analysis**: Instant ticker analysis
- **Status Indicators**: Analysis and data quality

### Stock Detail Pages
- **Comprehensive Reports**: AI-generated analysis
- **Multiple Tabs**: Report, news, filings, options
- **Strategy Ratings**: Visual indicators for strategies
- **Interactive Elements**: Expandable sections

### Settings
- **API Management**: Secure key configuration
- **Platform Preferences**: Customize behavior
- **Connection Testing**: Verify integrations
- **Usage Information**: Guidelines and disclaimers

## 🔧 Development

### Backend Development
```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest tests/

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend Development
```bash
cd frontend
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

## 🚀 Deployment

### Production Checklist
- [ ] Set production API keys
- [ ] Configure production database
- [ ] Set up SSL certificates
- [ ] Configure rate limiting
- [ ] Set up monitoring
- [ ] Configure backups

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Scale services
docker-compose up -d --scale backend=2
```

### Cloud Deployment
- **Vercel**: Frontend deployment
- **Railway/Render**: Backend deployment
- **AWS/GCP/Azure**: Full stack deployment

## 📈 Performance

### Optimization Features
- **Database Indexing**: Optimized queries
- **React Query Caching**: Efficient data fetching
- **Image Optimization**: Next.js automatic optimization
- **Code Splitting**: Lazy loading for better performance

### Monitoring
- **Health Checks**: API endpoint monitoring
- **Error Tracking**: Comprehensive logging
- **Performance Metrics**: Response time tracking
- **Usage Analytics**: Platform usage insights

## ⚠️ Disclaimer

**Important**: This platform is for educational and research purposes only. The AI-generated analysis should not be considered as financial advice. Investment decisions should always be based on your own research and consultation with qualified financial advisors.

### Risk Warning
- **No Guarantees**: AI analysis is not infallible
- **Market Risk**: All investments carry risk
- **Data Limitations**: Real-time data may have delays
- **Educational Use**: Not intended for live trading

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and research purposes only. See LICENSE file for details.

## 🆘 Support

- **Documentation**: Check this README and individual component docs
- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact support for urgent issues

---

**Built with ❤️ for the investment community**

*Empowering investors with AI-driven research and analysis*