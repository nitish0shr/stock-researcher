# Stock Research Frontend

Next.js frontend for the autonomous stock research platform.

## Features

- **Modern UI**: Built with Next.js 14, TypeScript, and Tailwind CSS
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Updates**: Live data with React Query
- **Interactive Charts**: Stock analysis visualizations
- **Settings Panel**: Configure API keys and preferences
- **Dark Mode Support**: Automatic theme switching

## Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Data Fetching**: TanStack React Query
- **Charts**: Recharts
- **Markdown**: React Markdown with GFM support

## Installation

### Prerequisites

- Node.js 18+ 
- npm or yarn package manager

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Production Build

1. **Build the application**
   ```bash
   npm run build
   # or
   yarn build
   ```

2. **Start the production server**
   ```bash
   npm start
   # or
   yarn start
   ```

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── globals.css         # Global styles
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Dashboard page
│   │   ├── settings/           # Settings page
│   │   └── stock/[symbol]/     # Stock detail pages
│   ├── components/             # React components
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── stock-table.tsx     # Stock data table
│   │   └── run-status.tsx      # Analysis status component
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   └── utils.ts            # Utility functions
│   └── types/                  # TypeScript type definitions
├── public/                     # Static assets
├── package.json                # Dependencies
├── tailwind.config.js          # Tailwind configuration
└── tsconfig.json               # TypeScript configuration
```

## Configuration

### Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### API Integration

The frontend connects to the backend API through the client in `src/lib/api.ts`. All API calls are managed through React Query for optimal caching and performance.

## Components

### UI Components

Built using shadcn/ui patterns:
- **Button**: Various button styles and variants
- **Card**: Content containers with headers and footers
- **Badge**: Status indicators and labels
- **Input**: Form inputs with validation
- **Tabs**: Tabbed content navigation
- **Toast**: Notification system

### Custom Components

- **StockTable**: Displays stock analysis results in a sortable table
- **RunStatus**: Shows the status of daily analysis runs
- **SettingsForm**: Configuration management interface

## Pages

### Dashboard (`/`)
- Real-time stock analysis overview
- Quick analysis input
- Filter and search functionality
- Run status indicators

### Stock Detail (`/stock/[symbol]`)
- Comprehensive stock analysis
- AI-generated research report
- News and filings tabs
- Options strategy analysis

### Settings (`/settings`)
- Platform configuration
- API key management
- Connection testing
- Usage information

## Features in Detail

### Real-time Data
- Live stock prices and market data
- Automatic refresh with React Query
- Loading states and error handling

### AI Analysis Reports
- Markdown-rendered research reports
- Interactive strategy ratings
- Risk assessment and key dates

### Options Analysis
- Covered call candidates
- Cash-secured put opportunities
- Implied volatility and Greeks

### News Integration
- Recent news articles
- Issue/risk flagging
- Source attribution and links

## Styling

### Tailwind CSS
- Utility-first CSS framework
- Custom color palette
- Responsive design utilities
- Dark mode support

### Custom Styles
- Loading animations
- Gradient backgrounds
- Glass morphism effects
- Smooth transitions

## Performance

### Optimization Features
- Next.js image optimization
- Automatic code splitting
- React Query caching
- Lazy loading for charts

### Bundle Analysis
```bash
npm run build
npm run analyze
```

## Deployment

### Vercel (Recommended)
1. Connect your GitHub repository
2. Configure environment variables
3. Deploy automatically on push

### Docker
```bash
# Build the image
docker build -t stock-research-frontend .

# Run the container
docker run -p 3000:3000 --env-file .env.local stock-research-frontend
```

### Other Platforms
- Netlify
- AWS Amplify
- Google Cloud Run
- Azure Static Web Apps

## Development

### Code Style
- ESLint configuration
- Prettier for formatting
- TypeScript strict mode
- Husky pre-commit hooks

### Testing
```bash
# Run tests
npm test

# Run tests in watch mode
npm test:watch

# Generate coverage report
npm test:coverage
```

### Debugging
- React DevTools
- Redux DevTools (if using)
- Network tab for API calls
- Console logging

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check backend URL in environment variables
   - Verify CORS settings in backend
   - Check network connectivity

2. **Build Failures**
   - Clear node_modules and reinstall
   - Check TypeScript errors
   - Verify all imports

3. **Performance Issues**
   - Check for memory leaks
   - Optimize React Query settings
   - Use React DevTools Profiler

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and research purposes only. See LICENSE file for details.