import os
import json
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
    
    def compare_brands(self, report_a: AuditReport, report_b: AuditReport, niche: str) -> ComparisonReport:
        """Pits two PRE-AUDITED reports against each other."""
        logger.info(f"⚔️ Refining Battle Data: {report_a.brand_name} vs {report_b.brand_name}")
        
        # We give the AI the exact data it needs so it doesn't hallucinate strings
        system_msg = (
            "You are a Competitive Intelligence Agent. Compare the two provided brand audits. "
            "Identify the winner and explain why in 3-4 sentences. "
            "Return ONLY a JSON object with the key 'winner_summary'."
        )
        
        user_msg = f"""
        DATA A: {report_a.model_dump_json()}
        DATA B: {report_b.model_dump_json()}
        NICHE: {niche}
        
        Return a ComparisonReport JSON with 'brand_a', 'brand_b', 'market_niche', and 'winner_summary'.
        """

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            response_format={"type": "json_object"}
        )
        
# Parse only the summary from the AI
        ai_data = json.loads(response.choices[0].message.content)
        summary = ai_data.get("winner_summary", "Comparison complete.")

        # MANUALLY build the report - This cannot fail validation!
        return ComparisonReport(
            brand_a=report_a,
            brand_b=report_b,
            market_niche=niche,
            winner_summary=summary
        )
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