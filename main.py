from core.config import Config
from agents.auditor import GEOAuditor
from tools.reporter import GEOReporter
from loguru import logger
from agents.researcher import CompetitorAgent
def run_competitive_sprint(client_brand, competitors, niche):
    Config.initialize_directories()
    
    # 1. Run Competitor Analysis
    researcher = CompetitorAgent()
    logger.info(f"Analyzing {client_brand} vs {competitors}...")
    comparison_json = researcher.compare_brands(client_brand, competitors, niche)
    
    # 2. Log Gaps
    logger.warning(f"Citation Gaps Found: {comparison_json}")
def main():
    # Warm up: Initialize directories
    Config.initialize_directories()
    
    logger.info(f"Welcome to {Config.AGENCY_NAME} Control Center")
    
    # Example Audit Run
    client_name = "SpaceX"
    niche = "Aerospace and Satellite Internet"
    
    try:
        auditor = GEOAuditor()
        report_data = auditor.perform_audit(client_name, niche)
        
        # Generate the PDF in the correct directory
        reporter = GEOReporter()
        filename = f"{client_name.replace(' ', '_')}_Audit.pdf"
        output_path = Config.REPORTS_DIR / filename
        
        reporter.generate_report(report_data.model_dump(), str(output_path))
        logger.success(f"Audit completed for {client_name}!")
        
    except Exception as e:
        logger.error(f"Operational failure: {e}")

if __name__ == "__main__":
    main()