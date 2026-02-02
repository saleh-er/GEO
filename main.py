import json
import webbrowser
from datetime import datetime
from loguru import logger
from core.config import Config
from agents.auditor import GEOAuditor
from tools.reporter import GEOReporter

def run_bulk_audits():
    """PHASE 1: Loop through all companies in the JSON database."""
    Config.initialize_directories()
    client_file = Config.DATA_DIR / "clients.json"
    
    if not client_file.exists():
        logger.error(f"Client file not found at {client_file}")
        return

    with open(client_file, 'r') as f:
        clients = json.load(f)

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
            
            stats["success"].append(brand)
            logger.success(f"Done: {brand}")
            
        except Exception as e:
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


def run_competitive_battle(brand_a, brand_b, niche):
    """PHASE 2: Create a side-by-side comparison for a specific rivalry."""
    auditor = GEOAuditor()
    
    # 1. Audit both brands
    report_a = auditor.perform_audit(brand_a, niche)
    report_b = auditor.perform_audit(brand_b, niche)
    
    # 2. Get the Competitive Analysis from AI
    battle_logic = auditor.compare_brands(report_a, report_b, niche)
    
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
    
    # 4. Success message and automatic opening
    logger.success(f"⚔️ Battle Report Generated: {output_path}")
    webbrowser.open(str(output_path))


if __name__ == "__main__":
    # --- Execute BOTH Options Sequentially ---
    
    # Step 1: Process every company in your large JSON file
    logger.info("🎬 STARTING ACT 1: BULK AUDITS")
    run_bulk_audits()

    # Step 2: Run the specific Competitive Battle
    print("\n" + "!"*50)
    logger.info("🎬 STARTING ACT 2: COMPETITIVE BATTLE")
    print("!"*50 + "\n")

    run_competitive_battle(
        brand_a="SpaceX", 
        brand_b="Blue Origin", 
        niche="Aerospace"
    )

    logger.success("🏁 ALL AGENCY TASKS COMPLETED SUCCESSFULLY.")