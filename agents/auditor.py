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