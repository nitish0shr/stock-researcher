import openai
import json
import os
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models import UserSecrets
from app.utils.encryption import decrypt_key

class OpenAIService:
    def __init__(self, db: Session):
        self.db = db
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Setup OpenAI client with API key"""
        # Try to get API key from database first
        secrets = self.db.query(UserSecrets).first()
        if secrets and secrets.openai_api_key_encrypted:
            api_key = decrypt_key(secrets.openai_api_key_encrypted)
        else:
            # Fallback to environment variable
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key not found")
        
        self.client = openai.OpenAI(api_key=api_key)
    
    async def analyze_stock(self, stock_data: Dict) -> Dict:
        """Analyze stock using OpenAI GPT"""
        try:
            # Prepare the prompt
            system_message = """You are an equity research assistant for an experienced but busy investor. 
You receive structured JSON that includes:
- real-time quote & basic fundamentals,
- recent earnings details,
- a list of recent news headlines with timestamps and URLs,
- latest filings / annual reports links,
- a simplified options snapshot (for covered calls and cash-secured puts),
- and a data_quality section indicating which data is present or missing.

Your job is to:
1. Produce a concise but detailed research report in markdown.
2. Highlight key risks, catalysts, and any recent issues or controversies.
3. Provide a non-binding, opinionated classification on whether:
   - the current moment seems attractive / neutral / unattractive for a new stock position (entry),
   - selling covered calls on an existing position seems attractive / neutral / unattractive,
   - selling cash-secured puts seems attractive / neutral / unattractive.

Treat this strictly as educational research, not as guaranteed or personalized financial advice. 
Never give absolute instructions like 'you must buy now'; instead, describe the risk-reward profile and conditions under which an experienced investor might consider each action. 
If some data is missing (e.g., no options, no recent news), clearly state that limitation."""
            
            # Format the stock data for the prompt
            user_message = f"""Please analyze the following stock data and provide a comprehensive research report:

```json
{json.dumps(stock_data, indent=2, default=str)}
```

Please provide your analysis in the following JSON format:
{{
  "summary_markdown": "Detailed markdown report with analysis",
  "entry": {{
    "rating": "strong_buy|buy|hold|avoid",
    "rationale": "Explanation for entry rating"
  }},
  "covered_call": {{
    "rating": "attractive|neutral|unattractive",
    "rationale": "Explanation for covered call rating",
    "notes": "Additional notes on covered calls"
  }},
  "secured_put": {{
    "rating": "attractive|neutral|unattractive", 
    "rationale": "Explanation for secured put rating",
    "notes": "Additional notes on secured puts"
  }},
  "risks_and_issues": [
    {{
      "label": "Risk label",
      "details": "Detailed description of the risk"
    }}
  ],
  "key_dates": [
    {{
      "label": "Event label",
      "date": "YYYY-MM-DD",
      "notes": "Event description"
    }}
  ]
}}"""
            
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the response
            content = response.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                # Find JSON in the response (it might be wrapped in code blocks)
                if '```json' in content:
                    json_start = content.find('```json') + 7
                    json_end = content.find('```', json_start)
                    json_str = content[json_start:json_end].strip()
                else:
                    json_str = content
                
                analysis_result = json.loads(json_str)
                return analysis_result
                
            except json.JSONDecodeError as e:
                # If JSON parsing fails, return structured response
                return {
                    "summary_markdown": content,
                    "entry": {
                        "rating": "hold",
                        "rationale": "Analysis completed but response format needs review"
                    },
                    "covered_call": {
                        "rating": "neutral",
                        "rationale": "Unable to parse detailed analysis",
                        "notes": ""
                    },
                    "secured_put": {
                        "rating": "neutral", 
                        "rationale": "Unable to parse detailed analysis",
                        "notes": ""
                    },
                    "risks_and_issues": [],
                    "key_dates": []
                }
                
        except Exception as e:
            print(f"Error in OpenAI analysis: {e}")
            return {
                "summary_markdown": f"Analysis failed: {str(e)}",
                "entry": {
                    "rating": "hold",
                    "rationale": "Analysis temporarily unavailable"
                },
                "covered_call": {
                    "rating": "neutral",
                    "rationale": "Analysis temporarily unavailable",
                    "notes": ""
                },
                "secured_put": {
                    "rating": "neutral",
                    "rationale": "Analysis temporarily unavailable", 
                    "notes": ""
                },
                "risks_and_issues": [],
                "key_dates": []
            }
    
    async def test_connection(self) -> Dict:
        """Test OpenAI API connection"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Hello, this is a test."}
                ],
                max_tokens=5
            )
            return {
                "success": True,
                "message": "OpenAI API connection successful"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}"
            }