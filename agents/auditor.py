import os
from openai import OpenAI
from core.schemas import AuditReport

class GEOAuditor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def perform_audit(self, brand: str, niche: str) -> AuditReport:
        # Agency-grade system prompt
        system_msg = "You are a GEO Visibility Expert. Analyze brands in JSON format."
        user_msg = f"Audit '{brand}' in the '{niche}' niche. Provide visibility score and citations."

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
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