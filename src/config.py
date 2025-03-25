"""
Configuration settings for the ETL-Crawler project
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Job search settings
DEFAULT_KEYWORDS = [
    "software engineer",
    "data engineer",
    "python developer",
    "full stack developer",
    "backend developer"
]

DEFAULT_LOCATIONS = [
    "remote",
    "united states",
    "new york",
    "san francisco",
    "seattle"
]

# Crawler settings
MAX_JOBS_PER_SOURCE = 25
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = (2, 5)  # Random delay range in seconds
BLOCKED_DELAY = (5, 10)  # Longer delay when blocked

# File paths
DATA_DIR = "data"
LOG_DIR = "logs"
EXCEL_FILE = os.path.join(DATA_DIR, "jobs.xlsx")

# Logging settings
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Proxy settings (if needed)
USE_PROXY = os.getenv('USE_PROXY', 'false').lower() == 'true'
PROXY_LIST = os.getenv('PROXY_LIST', '').split(',') if os.getenv('PROXY_LIST') else [] 