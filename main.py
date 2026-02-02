import json
from loguru import logger
from core.config import Config
from agents.auditor import GEOAuditor
from tools.reporter import GEOReporter

def run_bulk_audits():
    """Reads clients from JSON and processes them one by one."""
    # 1. Ensure folders (reports, data, etc.) exist
    Config.initialize_directories()
    
    # 2. Locate your client database
    client_file = Config.DATA_DIR / "clients.json"
    
    if not client_file.exists():
        logger.error(f"Client file not found at {client_file}. Please create it first.")
        return

    # 3. Load the data from the JSON file
    with open(client_file, 'r') as f:
        clients = json.load(f)

    logger.info(f"Loaded {len(clients)} clients. Starting bulk processing...")
    
    # 4. Initialize your agency tools once to save memory
    auditor = GEOAuditor()
    reporter = GEOReporter()

    # 5. THE LOOP: Process each client automatically
    for client in clients:
        brand = client['brand_name']
        niche = client['niche']
        
        logger.info(f">>> Processing Audit: {brand}")
        
        try:
            # AI performs the audit
            report_data = auditor.perform_audit(brand, niche)
            
            # Create a unique filename for this client
            filename = f"{brand.replace(' ', '_')}_Audit.pdf"
            output_path = Config.REPORTS_DIR / filename
            
            # Generate the PDF
            reporter.generate_report(report_data.model_dump(), str(output_path))
            logger.success(f"Audit exported for {brand}")
            
        except Exception as e:
            logger.error(f"Failed to audit {brand}: {e}")

if __name__ == "__main__":
    run_bulk_audits()