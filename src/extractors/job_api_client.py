import requests
import time
from typing import List, Dict
import os
from src.config import API_KEY, BASE_URL
from src.utils.logger import logger
from urllib.parse import quote

class JobApiClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = os.environ.get("API_KEY")
        self.base_url = base_url

    def fetch_jobs(self, keywords: str, location: str, pages_to_fetch: int) -> List[Dict]:
        """Fetches job data from the API."""
        jobs = []
        if not self.api_key:
            raise ValueError("API key is missing. Please set the API_KEY environment variable.")

        # Log the API key being used (only first few chars for security)
        api_key_snippet = self.api_key[:5] + "..." if self.api_key else "None"
        logger.info(f"Using API Key: {api_key_snippet}")

        for page in range(1, pages_to_fetch + 1):
            try:
                keywords_string = ",".join(keywords)
                locations_string = ",".join(location)
                url = f"{self.base_url}/search?query={quote(keywords_string)}&location={quote(locations_string)}&page={page}"
                headers = {
                    "X-RapidAPI-Key": self.api_key,
                    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"  # Ensure matches API's domain
                }
                logger.info(f"Fetching page {page} from {url}")
                logger.info(f"Request Headers: {headers}")
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                data = response.json()

                # Assuming a hypothetical API structure: {'data': [{'job_title': ..., 'company': ...}]}
                jobs.extend(data.get('data', []))

                time.sleep(5)  # Respect rate limits

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                continue  # Or raise, depending on error handling strategy
            except ValueError as e:
                logger.error(f"JSON decoding failed: {e}")
                continue

        return jobs
