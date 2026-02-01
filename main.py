from core.config import Config
from agents.auditor import GEOAuditor
from tools.reporter import GEOReporter
from loguru import logger

def run_agency_sprint(brand_name, niche):
    logger.info(f"--- Starting Pro Sprint for {brand_name} ---")
    
    # 1. Perform AI Audit
    auditor = GEOAuditor()
    report_data = auditor.perform_audit(brand_name, niche)
    
    # 2. Add real-time context (Optional but Pro)
    # search_tool = PerplexitySearch()
    # live_data = search_tool.search(f"Current mentions of {brand_name}")
    
    # 3. Generate PDF
    reporter = GEOReporter()
    filename = f"{brand_name.replace(' ', '_')}_GEO_Audit.pdf"
    reporter.generate_report(report_data.model_dump(), filename)
    
    logger.success(f"REPORT GENERATED: reports/{filename}")

if __name__ == "__main__":
    run_agency_sprint("Tesla", "Electric Vehicles")