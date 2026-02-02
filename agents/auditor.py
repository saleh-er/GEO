import os
from openai import OpenAI
from core.schemas import AuditReport

class GEOAuditor:
    def __init__(self):
      self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1", 
            api_key=os.getenv("GROQ_API_KEY")
               )
    def perform_audit(self, brand: str, niche: str) -> AuditReport:
        # Agency-grade system prompt
        system_msg = (
        "You are a Senior GEO Analyst. Return ONLY a valid JSON object. "
        "CRITICAL: You must use these exact keys:\n"
        "- 'brand_name'\n"
        "- 'visibility_score'\n"
        "- 'recommendations'\n"
        "- 'citations'\n"
        "- 'hallucinations'\n"
        "If you use 'score' or 'suggestions', the system will fail. Stick to the keys above."
    )
        
        user_msg = (
            f"Audit '{brand}' in '{niche}'. "
            "Ensure 'citations' is a list of 3 objects with source/sentiment/context keys. "
            "Ensure 'hallucinations' is a list of objects with fact/correction keys. "
            "Return ONLY JSON."
        )

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
            response_format={"type": "json_object"}
        )
        return AuditReport.model_validate_json(response.choices[0].message.content)
def detect_hallucinations(self, ai_response: str, ground_truth_docs: str):
    """
    Compares AI claims against the client's verified data.
    """
    verification_prompt = f"""
    Compare the following AI-generated statement about a brand against the official ground truth.
    Identify any FABRICATIONS, OUTDATED INFO, or INCORRECT ENTITIES.
    
    AI STATEMENT: {ai_response}
    GROUND TRUTH: {ground_truth_docs}
    
    Return a JSON list of errors with 'severity' (Low/High) and 'correction'.
    """
    
    response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": verification_prompt}],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content