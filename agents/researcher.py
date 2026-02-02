import os
from typing import List
from tools.search import PerplexitySearch
from core.schemas import CompetitorAnalysis, CompetitorMetrics
from openai import OpenAI
import os

class CompetitorAgent:
    def __init__(self):
        self.search_tool = PerplexitySearch()
        self.ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def compare_brands(self, client_brand: str, competitors: List[str], niche: str):
        # 1. Get live market data
        query = f"Who are the top players in {niche} and what are they known for? Compare {client_brand} vs {', '.join(competitors)}."
        raw_market_data = self.search_tool.search(query)
        
        # 2. Use GPT to structure the 'Gap Analysis'
        analysis_prompt = f"Based on this research: {raw_market_data}, identify specific topics where {competitors} are cited but {client_brand} is not. Return in JSON."
        
        response = self.ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": analysis_prompt}],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content