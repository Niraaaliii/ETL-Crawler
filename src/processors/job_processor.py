from typing import List, Dict
from src.models import JobListing
from src.utils.logger import logger

def transform_jobs(raw_job_data: List[Dict]) -> List[JobListing]:
    """Transforms raw job data into JobListing objects."""
    job_listings = []
    for job_data in raw_job_data:
        try:
            job_listing = JobListing(
                job_id=job_data.get('job_id', 'N/A'),
                title=job_data.get('job_title', 'N/A'),
                company_name=job_data.get('company', 'N/A'),
                location=job_data.get('location', 'N/A'),
                description=job_data.get('description', 'N/A'),
                url=job_data.get('url', 'N/A'),
                posted_date=job_data.get('posted_date', 'N/A'),
                source_api='RapidAPI Jobs'
            )
            job_listings.append(job_listing)
        except KeyError as e:
            logger.error(f"Missing key in job data: {e}")
            continue  # Skip this job if a required key is missing
        except Exception as e:
            logger.error(f"Error transforming job data: {e}")
            continue
    return job_listings
