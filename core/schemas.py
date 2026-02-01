from pydantic import BaseModel, Field
from typing import List

class Citation(BaseModel):
    source: str
    sentiment: str = Field(description="Positive, Neutral, or Negative")
    context: str

class AuditReport(BaseModel):
    brand_name: str
    visibility_score: float = Field(ge=0, le=100)
    citations: List[Citation]
    recommendations: List[str]