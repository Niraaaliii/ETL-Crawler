import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

BASE_URL = "https://jsearch.p.rapidapi.com"
DATA_DIR = "data/"  # Directory to save output files

DEFAULT_KEYWORDS = ["Software Engineer", "Data Analyst", "Business Intelligence"]
DEFAULT_LOCATIONS = ["Houston", "United States", "Texas"]

SEARCH_KEYWORDS = os.getenv("SEARCH_KEYWORDS", ",".join(DEFAULT_KEYWORDS))
SEARCH_LOCATION = os.getenv("SEARCH_LOCATION", ",".join(DEFAULT_LOCATIONS))
