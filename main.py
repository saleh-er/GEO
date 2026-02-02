import json
from datetime import datetime
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
    
    # 4. Initialize the Auditor once (it can be reused)
    auditor = GEOAuditor()

    # 5. THE LOOP: Process each client automatically
    for client in clients:
        brand = client['brand_name']
        niche = client['niche']
        
        logger.info(f">>> Processing Audit: {brand}")
        
        try:
            # AI performs the audit
            report_data = auditor.perform_audit(brand, niche)
            
            # --- FIX: Re-initialize the reporter for EACH client ---
            # This prevents the 'closed document' error
            reporter = GEOReporter()
            
            # --- PRO FEATURE: Add a timestamp to the filename ---
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"{brand.replace(' ', '_')}_Audit_{timestamp}.pdf"
            output_path = Config.REPORTS_DIR / filename
            
            # Generate the PDF
            reporter.generate_report(report_data.model_dump(), str(output_path))
            logger.success(f"Audit exported for {brand}: {filename}")
            
        except Exception as e:
            # If one fails, the loop continues to the next client
            logger.error(f"Failed to audit {brand}: {e}")

if __name__ == "__main__":
    run_bulk_audits()