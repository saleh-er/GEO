from pydantic import BaseModel, Field, AliasChoices
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
    brand_name: str = Field(
        validation_alias=AliasChoices('brand_name', 'brand', 'company', 'name')
    )
    
    # We add every possible name the AI might use for the score
    visibility_score: float = Field(
        validation_alias=AliasChoices('visibility_score', 'score', 'visibility', 'rating', 'ai_score')
    )
    
    citations: List[dict] 
    
    # We add aliases for recommendations too
    recommendations: List[str] = Field(
        validation_alias=AliasChoices('recommendations', 'strategic_recommendations', 'suggestions', 'advice', 'next_steps')
    )
    
    hallucinations: Optional[List[dict]] = None


class CompetitorAnalysis(BaseModel):
    market_query: str
    leaderboard: List[CompetitorMetrics]
    citation_gaps: List[str] = Field(description="Topics competitors win that we miss")