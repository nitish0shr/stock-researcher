# Frontend Starter Structure (Next.js)

Create folders in your frontend project:
- /frontend/pages
- /frontend/components
- /frontend/public

Sample entry file (`pages/index.js`):
```javascript
import Head from 'next/head';
export default function Home() {
  return (
    <div>
      <Head><title>Stock Researcher Dashboard</title></Head>
      <h1>Stock Researcher</h1>
      <p>Welcome to your production dashboard!</p>
    </div>
  );
}
```

Sample component (`components/StockCard.js`):
```javascript
export default function StockCard({ symbol, price, name }) {
  return (
    <div className="card">
      <h3>{symbol}: {name}</h3>
      <div>Price: ${price}</div>
    </div>
  );
}
```

You can add other pages like:
- `/pages/stocks.js`
- `/pages/analysis.js`
- `/pages/login.js`

Add placeholder image/logo in `/public`.

# Backend Improvements

## Auth Scaffold (`backend/app/auth.py`):
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")
SECRET_KEY = "your-very-secret-key"

# Dummy user validation
def fake_decode_token(token):
    return {"username": "admin"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = fake_decode_token(token)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Example Test (`backend/tests/test_api.py`):
```python
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

# DevOps & DB

- Add Alembic for migration: `alembic init alembic` and configure with your db url.
- Example seed data (`data/storage/demo.json`):
```json
[{"symbol": "AAPL", "price": 190, "name": "Apple Inc."}]
```
- Update Docker Compose with healthcheck:
```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
```

# CI/CD

- Add GitHub Actions Workflows (create `.github/workflows/main.yml`):
```yaml
name: CI/CD
on:
  push:
    branches: [main]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10
      - name: Install requirements
        run: pip install -r backend/requirements.txt
      - name: Run backend tests
        run: pytest backend/tests
```

# Documentation

- Expand README to include frontend setup and API usage examples.
- Add LICENSE (MIT recommended).
- Add CONTRIBUTING.md.
- Update `.env.example` with all needed keys:
```
OPENAI_API_KEY=
MARKET_DATA_API_KEY=
NEWS_API_KEY=
DATABASE_URL=
SECRET_KEY=
```
