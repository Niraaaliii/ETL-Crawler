from dataclasses import dataclass
from typing import Optional

@dataclass
class JobListing:
    job_id: str
    title: str
    company_name: str
    location: str
    description: str
    url: str
    posted_date: Optional[str] = None
    source_api: str = "RapidAPI Jobs"
