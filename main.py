import json
from datetime import datetime
from loguru import logger
from core.config import Config
from agents.auditor import GEOAuditor
from tools.reporter import GEOReporter

def run_bulk_audits():
    Config.initialize_directories()
    client_file = Config.DATA_DIR / "clients.json"
    
    if not client_file.exists():
        logger.error(f"Client file not found.")
        return

    with open(client_file, 'r') as f:
        clients = json.load(f)

    # Agency Dashboard Tracking
    stats = {"success": [], "failed": []}
    logger.info(f"Loaded {len(clients)} clients. Starting engine...")
    
    auditor = GEOAuditor()

    for client in clients:
        brand = client['brand_name']
        niche = client['niche']
        logger.info(f">>> Auditing: {brand}")
        
        try:
            report_data = auditor.perform_audit(brand, niche)
            reporter = GEOReporter()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"{brand.replace(' ', '_')}_Audit_{timestamp}.pdf"
            output_path = Config.REPORTS_DIR / filename
            
            reporter.generate_report(report_data.model_dump(), str(output_path))
            
            # Record success
            stats["success"].append(brand)
            logger.success(f"Done: {brand}")
            
        except Exception as e:
            # Record failure
            stats["failed"].append({"brand": brand, "error": str(e)[:50]})
            logger.error(f"Failed: {brand}")

    # --- Print Agency Dashboard Summary ---
    print("\n" + "="*50)
    print(f"🚀 {Config.AGENCY_NAME} BATCH SUMMARY")
    print("="*50)
    print(f"✅ SUCCESSFULLY AUDITED: {len(stats['success'])}")
    for b in stats["success"]: print(f"  - {b}")
    
    print(f"\n❌ FAILED AUDITS: {len(stats['failed'])}")
    for f in stats["failed"]: print(f"  - {f['brand']}: {f['error']}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_bulk_audits()