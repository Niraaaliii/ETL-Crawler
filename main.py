import os
from dotenv import load_dotenv
from datetime import datetime

import os
from src.config import API_KEY, BASE_URL, SEARCH_KEYWORDS, SEARCH_LOCATION, DEFAULT_KEYWORDS, DEFAULT_LOCATIONS
from src.extractors.job_api_client import JobApiClient
# Removed transform_jobs import as it's no longer needed
from src.utils.excel_manager import save_to_csv # Changed import
from src.utils.logger import logger

os.environ["API_KEY"] = "8957d0c6e5msh7a908a3f48fbad3p10b7a6jsn422930cd37dc"

class ETLOrchestrator:
    def __init__(self):
        self.api_client = JobApiClient(API_KEY, BASE_URL)
        self.keywords = SEARCH_KEYWORDS.split(',') if SEARCH_KEYWORDS else DEFAULT_KEYWORDS
        self.location = SEARCH_LOCATION.split(',') if SEARCH_LOCATION else DEFAULT_LOCATIONS

    def run_etl(self, num_pages: int = 1):
        """Orchestrates the ETL process."""
        logger.info("Starting ETL process")

        try:
            # Restore original parameter logic
            keywords_param = self.keywords
            location_param = self.location
            # logger.info(f"--- Running test with single keyword: '{keywords_param}', location: '{location_param}' ---") # Remove test log

            raw_jobs = self.api_client.fetch_jobs(keywords_param, location_param, pages_to_fetch=num_pages)
            logger.info(f"Fetched {len(raw_jobs)} raw job listings")

            # Skip transformation step
            # job_listings = transform_jobs(raw_jobs)
            # logger.info(f"Transformed {len(job_listings)} job listings")

            if raw_jobs:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                # Update filename for CSV
                filename = f"job_listings_{self.keywords}_{self.location}_{timestamp}"
                # Call the new save_to_csv function with raw_jobs
                save_to_csv(raw_jobs, filename)
            else:
                logger.warning("No jobs fetched, skipping CSV save.")


            logger.info("ETL process completed successfully")

        except Exception as e:
            logger.error(f"ETL process failed: {e}")

def main():
    orchestrator = ETLOrchestrator()
    orchestrator.run_etl(num_pages=1)

if __name__ == "__main__":
    main()
