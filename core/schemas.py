from pydantic import BaseModel, Field
from typing import List, Dict

class CompetitorMetrics(BaseModel):
    brand_name: str
    citation_count: int
    top_sources: List[str]
    sentiment_score: float # 0.0 to 1.0

class CompetitorAnalysis(BaseModel):
    market_query: str
    leaderboard: List[CompetitorMetrics]
    citation_gaps: List[str] = Field(description="Topics competitors win that we miss")