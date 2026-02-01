import os
import requests
from loguru import logger

class PerplexitySearch:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        self.base_url = "https://api.perplexity.ai/chat/completions"

    def search(self, query: str):
        if not self.api_key:
            logger.error("Perplexity API Key missing!")
            return None

        payload = {
            "model": "sonar-pro", # Latest 2026 high-performance model
            "messages": [
                {"role": "system", "content": "You are a GEO Researcher. Provide raw, cited search data."},
                {"role": "user", "content": query}
            ],
            "temperature": 0.2
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
    }

        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return None