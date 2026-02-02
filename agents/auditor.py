import os
from openai import OpenAI
from loguru import logger
from core.schemas import AuditReport, ComparisonReport # Ensure ComparisonReport is in your schemas

class GEOAuditor:
    def __init__(self):
        # Using Groq for high-speed audits
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1", 
            api_key=os.getenv("GROQ_API_KEY")
        )

    def perform_audit(self, brand: str, niche: str) -> AuditReport:
        """Executes a single-brand GEO visibility audit."""
        logger.info(f"🔍 Analyzing Brand: {brand}")
        
        system_msg = (
            "You are a Senior GEO Analyst. Return a strictly valid JSON object. "
            "Analyze the brand's visibility in AI models. "
            "CRITICAL: Use these exact keys: 'brand_name', 'visibility_score', "
            "'recommendations', 'citations', 'hallucinations'."
        )
        
        user_msg = (
            f"Conduct a deep-dive audit for '{brand}' in the '{niche}' sector. "
            "1. Score visibility 0-100. 2. Provide 3 citation objects (source, sentiment, context). "
            "3. Identify hallucinations (fact, correction). 4. List 3 strings for recommendations."
        )

        # Using modern 'parse' to force Pydantic compliance
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            #use standard json mode 
            response_format={"type": "json_object"}
        )
        # FIX: Manually validate the response content
        raw_content = response.choices[0].message.content
        return AuditReport.model_validate_json(raw_content)
    
    def compare_brands(self, brand_1: str, brand_2: str, niche: str) -> ComparisonReport:
        logger.info(f"⚔️ Battle Mode: {brand_1} vs {brand_2}")
        
        system_msg = "You are a Competitive Intelligence Agent. Return valid JSON comparing Brand A and B."
        user_msg = f"Compare {brand_1} vs {brand_2} in {niche}."

        # FIX: Also update the comparison method
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            response_format={"type": "json_object"}
        )
        
        return ComparisonReport.model_validate_json(response.choices[0].message.content)


    def detect_hallucinations(self, ai_response: str, ground_truth_docs: str):
        """Compares AI claims against the client's verified data."""
        logger.info("🛡️ Running Hallucination Verification...")
        
        verification_prompt = f"""
        Compare this AI statement against the official ground truth.
        Identify FABRICATIONS, OUTDATED INFO, or INCORRECT ENTITIES.
        
        AI STATEMENT: {ai_response}
        GROUND TRUTH: {ground_truth_docs}
        
        Return a JSON list of objects with 'fact', 'severity', and 'correction'.
        """
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Switched to Groq for speed
            messages=[{"role": "user", "content": verification_prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

  
        return response.choices[0].message.parsed