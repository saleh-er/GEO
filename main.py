import sys
from loguru import logger

# Internal Imports
from core.config import Config
from agents.auditor import GEOAuditor
from agents.researcher import CompetitorAgent
from tools.reporter import GEOReporter

def run_test_audit():
    """Validates the PDF generation engine with dummy data."""
    logger.info("Running system diagnostic: Generating Test Report...")
    
    test_data = {
        "brand_name": "Test-Agent-Alpha",
        "visibility_score": 42,
        "recommendations": [
            "Diagnostic: Ensure API keys are active.",
            "Diagnostic: Verify reports/ folder permissions.",
            "Diagnostic: Check font rendering in PDF."
        ],
        "leaderboard": [
            {"brand_name": "Test-Agent-Alpha", "citation_count": 5, "sentiment_score": 0.5},
            {"brand_name": "Benchmark-Beta", "citation_count": 10, "sentiment_score": 0.9}
        ],
        "hallucinations": [
            {"fact": "System is offline.", "correction": "System is fully operational."}
        ]
    }

    reporter = GEOReporter()
    filename = Config.REPORTS_DIR / "System_Diagnostic_Report.pdf"
    reporter.generate_report(test_data, str(filename))
    logger.success(f"Diagnostic Complete: {filename}")

def run_live_audit(brand: str, niche: str):
    """The bread and butter of the agency: Real-time AI Visibility Audit."""
    logger.info(f"Initializing Live GEO Audit for: {brand} ({niche})")
    
    try:
        # 1. AI Analysis
        auditor = GEOAuditor()
        report_data = auditor.perform_audit(brand, niche)
        
        # 2. PDF Production
        reporter = GEOReporter()
        filename = f"{brand.replace(' ', '_')}_GEO_Audit.pdf"
        output_path = Config.REPORTS_DIR / filename
        
        # Use model_dump() to convert Pydantic to a Dictionary for the Reporter
        reporter.generate_report(report_data.model_dump(), str(output_path))
        
        logger.success(f"Audit finalized and exported to: {output_path}")
        
    except Exception as e:
        logger.critical(f"Audit Engine Failure: {str(e)}")

def run_competitive_sprint(brand: str, competitors: list, niche: str):
    """Deep analysis of market share and citation gaps."""
    logger.info(f"Starting Competitive Sprint: {brand} vs {competitors}")
    
    try:
        researcher = CompetitorAgent()
        # This calls the Perplexity Search + OpenAI Analysis
        comparison_results = researcher.compare_brands(brand, competitors, niche)
        
        # Log results to console (In a later version, we'll pipe this to the PDF)
        logger.warning(f"Market Intelligence Gathered: {comparison_results}")
        
    except Exception as e:
        logger.error(f"Competitive Analysis failed: {e}")

if __name__ == "__main__":
    # --- 1. System Initialization ---
    Config.initialize_directories()
    logger.info(f"--- {Config.AGENCY_NAME} v1.0 Operational ---")

    # --- 2. Configuration Switch ---
    # Change 'MODE' to switch between services
    MODE = "LIVE" 

    if MODE == "TEST":
        run_test_audit()
        
    elif MODE == "LIVE":
        # Example Client
        run_live_audit(brand="Perplexity AI", niche="Conversational Search Engines")
        
    elif MODE == "COMPETE":
        # Example Sprint
        run_competitive_sprint(
            brand="OpenAI", 
            competitors=["Anthropic", "Google DeepMind", "Meta AI"], 
            niche="Large Language Models"
        )
    
    else:
        logger.error("Invalid MODE selected. Choose 'TEST', 'LIVE', or 'COMPETE'.")