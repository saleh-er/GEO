import os
from dotenv import load_dotenv
from loguru import logger
from agents.auditor import GEOAuditor

load_dotenv()

def start_agency_workflow(brand, niche):
    logger.info(f"Initializing Audit for {brand}...")
    
    try:
        auditor = GEOAuditor()
        report = auditor.perform_audit(brand, niche)
        
        logger.success(f"Audit Complete! Score: {report.visibility_score}%")
        
        # Displaying Results
        for cite in report.citations:
            logger.info(f"Found citation on {cite.source} ({cite.sentiment})")
            
    except Exception as e:
        logger.error(f"Audit failed: {e}")

if __name__ == "__main__":
    start_agency_workflow("The Ritz-Carlton", "Luxury Hotels")