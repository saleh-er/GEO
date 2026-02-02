import sys
import json
from loguru import logger
from core.config import Config
from agents.auditor import GEOAuditor
from agents.researcher import CompetitorAgent
from tools.reporter import GEOReporter

def run_test_audit():
    """Runs a mock audit to verify PDF generation and styling."""
    logger.info("Executing Test Audit with mock data...")
    
    mock_data = {
        "brand_name": "TechFlow Solutions",
        "visibility_score": 35,
        "recommendations": [
            "Implement FAQ Schema on the homepage.",
            "Optimize for long-tail entity recognition.",
            "Increase presence on niche industry forums."
        ],
        "leaderboard": [
            {"brand_name": "TechFlow Solutions", "citation_count": 12, "sentiment_score": 0.85},
            {"brand_name": "CloudNexus", "citation_count": 45, "sentiment_score": 0.92},
            {"brand_name": "DataStream Inc", "citation_count": 38, "sentiment_score": 0.70}
        ],
        "hallucinations": [
            {"fact": "AI claims TechFlow was founded by Steve Jobs.", "correction": "Founded in 2018 by Sarah Jenkins."},
            {"fact": "AI states price is $999/mo.", "correction": "Actual price is $149/mo."}
        ]
    }

    reporter = GEOReporter()
    filename = Config.REPORTS_DIR / "TechFlow_Test_Report.pdf"
    reporter.generate_report(mock_data, str(filename))

def run_real_audit(brand, niche):
    """Executes a live audit using AI Agents."""
    logger.info(f"Starting Live GEO Audit for: {brand}")
    try:
        auditor = GEOAuditor()
        report_data = auditor.perform_audit(brand, niche)
        
        reporter = GEOReporter()
        filename = Config.REPORTS_DIR / f"{brand.replace(' ', '_')}_Final_Audit.pdf"
        
        reporter.generate_report(report_data.model_dump(), str(filename))
        logger.success(f"Live Audit Complete: {filename}")
    except Exception as e:
        logger.error(f"Audit failed: {e}")

def run_competitive_analysis(brand, competitors, niche):
    """Deep dive into competitive gaps."""
    logger.info(f"Analyzing {brand} vs {competitors}...")
    researcher = CompetitorAgent()
    
    # This currently returns JSON from our researcher agent
    raw_comparison = researcher.compare_brands(brand, competitors, niche)
    
    # For a Pro flow, we would parse this and add it to the final PDF
    logger.warning(f"Competitive Gaps Identified: {raw_comparison}")

if __name__ == "__main__":
    # 1. Warm up the agency
    Config.initialize_directories()
    logger.info(f"Welcome to {Config.AGENCY_NAME} Control Center")

    # 2. Choose your mode (Change this variable to test different features)
    # Options: "TEST", "LIVE", "COMPETE"
    MODE = "TEST" 

    if MODE == "TEST":
        run_test_audit()
    
    elif MODE == "LIVE":
        run_real_audit("SpaceX", "Aerospace and Satellite Internet")
        
    elif MODE == "COMPETE":
        run_competitive_analysis(
            "Tesla", 
            ["Lucid Motors", "Rivian", "BYD"], 
            "Electric Vehicles"
        )