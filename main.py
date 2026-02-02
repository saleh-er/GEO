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

def run_competitive_battle(brand_a, brand_b, niche):
    auditor = GEOAuditor()
    
    # 1. Audit both brands
    report_a = auditor.perform_audit(brand_a, niche)
    report_b = auditor.perform_audit(brand_b, niche)
    
    # 2. Get the "Winner Summary" from AI
    battle_logic = auditor.compare_brands(brand_a, brand_b, niche)
    
    # 3. Generate the Dashboard
    reporter = GEOReporter()
    filename = f"Battle_{brand_a}_vs_{brand_b}.pdf"
    output_path = Config.REPORTS_DIR / filename
    reporter.generate_battle_report(
        report_a.model_dump(), 
        report_b.model_dump(), 
        battle_logic.winner_summary, 
        str(output_path)
    )
    logger.success(f"⚔️ Battle Report Generated: {output_path}")