import logging
import os
from datetime import datetime

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler(f"logs/etl_{datetime.now().strftime('%Y%m%d')}.log"),  # Output to file with date
    ],
)

logger = logging.getLogger(__name__)
