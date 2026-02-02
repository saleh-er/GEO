from pydantic import BaseModel, Field
from typing import List, Optional

class Citation(BaseModel):
    source: str
    sentiment: str
    context: str
class CompetitorMetrics(BaseModel):
    brand_name: str
    citation_count: int
    top_sources: List[str]
    sentiment_score: float # 0.0 to 1.0

class AuditReport(BaseModel):
    brand_name: str
    visibility_score: float = Field(ge=0, le=100)
    citations: List[Citation]
    recommendations: List[str]
    # Adding this field helps with the new hallucination feature
    hallucinations: Optional[List[dict]] = None


class CompetitorAnalysis(BaseModel):
    market_query: str
    leaderboard: List[CompetitorMetrics]
    citation_gaps: List[str] = Field(description="Topics competitors win that we miss")