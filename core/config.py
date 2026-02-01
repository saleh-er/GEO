import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# 1. Dynamically find the Project Root (where .env lives)
# Path(__file__) is the current file, .parent is 'core/', .parent.parent is root
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Load Environment Variables
load_dotenv(BASE_DIR / ".env")

class Config:
    # --- API Keys ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    
    # --- Paths ---
    DATA_DIR = BASE_DIR / "data"
    REPORTS_DIR = BASE_DIR / "reports"
    LOGS_DIR = BASE_DIR / "logs"
    
    # --- Agency Settings ---
    AGENCY_NAME = "The GEO Agency"
    DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

    @classmethod
    def initialize_directories(cls):
        """Ensures all necessary folders exist on startup."""
        dirs = [cls.DATA_DIR, cls.REPORTS_DIR, cls.LOGS_DIR]
        for directory in dirs:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {directory.relative_to(BASE_DIR)}")

# Initialize logs immediately
logger.add(Config.LOGS_DIR / "agency.log", rotation="1 MB", level="INFO")