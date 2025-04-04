import os
from dotenv import load_dotenv
from datetime import datetime

from core.config import API_KEY, BASE_URL, SEARCH_KEYWORDS, SEARCH_LOCATION, DEFAULT_KEYWORDS, DEFAULT_LOCATIONS
from core.job_api_client import JobApiClient
from core.utils import save_to_csv, logger

# Load environment variables
load_dotenv()

class ETLOrchestrator:
    def __init__(self) -> None:
        self.api_client: JobApiClient = JobApiClient(API_KEY, BASE_URL)
        self.keywords: str = SEARCH_KEYWORDS or DEFAULT_KEYWORDS
        self.location: str = SEARCH_LOCATION or DEFAULT_LOCATIONS

    def run_etl(self, num_pages: int = 1) -> None:
        logger.info("Starting ETL process")
        try:
            raw_jobs = self.api_client.fetch_jobs(self.keywords, self.location, pages_to_fetch=num_pages)
            logger.info(f"Fetched {len(raw_jobs)} raw job listings")

            if raw_jobs:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"job_listings_{self.keywords.replace(',', '_')}_{self.location.replace(',', '_')}_{timestamp}"
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
