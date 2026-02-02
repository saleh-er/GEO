import os
from typing import List
from openai import OpenAI
from loguru import logger
from tools.search import PerplexitySearch
from core.schemas import CompetitorAnalysis

class CompetitorAgent:
    def __init__(self):
        # Tools for live web research
        self.search_tool = PerplexitySearch()
        
        # Pointing the client to Groq's servers
        self.ai_client = OpenAI(
            base_url="https://api.groq.com/openai/v1", 
            api_key=os.getenv("GROQ_API_KEY")
        )

    def compare_brands(self, client_brand: str, competitors: List[str], niche: str) -> CompetitorAnalysis:
        """Researches competitors and extracts a structured gap analysis via Groq."""
        logger.info(f"🛰️ Researching Market for {client_brand}...")

        # 1. Fetch live market data using Perplexity
        query = (
            f"Conduct a competitive research in the {niche} industry. "
            f"Compare {client_brand} against {', '.join(competitors)}. "
            "Highlight specific topics, keywords, and features where competitors are mentioned more than the client."
        )
        raw_market_data = self.search_tool.search(query)

        # 2. Instruct Groq/Llama to structure the findings
        # We must use 'json_object' format and mention 'JSON' in the prompt
        system_instruction = (
            "You are a Market Intelligence Expert. Analyze search data and output a JSON object. "
            "Identify 'topic_gaps'—areas where competitors excel but the client is invisible."
        )
        
        user_prompt = (
            f"Based on this research: {raw_market_data}\n\n"
            f"Create a gap analysis for {client_brand} vs {competitors}. "
            "Return a JSON object matching the CompetitorAnalysis schema."
        )

        response = self.ai_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )

        # 3. Validate the JSON string into our Pydantic model
        raw_json = response.choices[0].message.content
        return CompetitorAnalysis.model_validate_json(raw_json)