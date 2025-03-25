"""
LinkedIn Crawler for job listings
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from src.crawlers.base_crawler import BaseCrawler

class LinkedInCrawler(BaseCrawler):
    """
    Crawler for LinkedIn job listings
    """
    
    def __init__(self, locations=None, keywords=None, limit=25):
        """
        Initialize the LinkedIn crawler
        
        Args:
            locations (list): List of locations to search
            keywords (list): List of job keywords to search
            limit (int): Maximum number of jobs to retrieve
        """
        super().__init__()
        self.base_url = "https://www.linkedin.com"
        self.search_url = "https://www.linkedin.com/jobs/search"
        self.locations = locations or ["remote", "united states"]
        self.keywords = keywords or ["software engineer", "data engineer", "python developer"]
        self.limit = limit
    
    def crawl(self):
        """
        Crawl LinkedIn for job listings
        
        Returns:
            list: List of job dictionaries
        """
        self.logger.info(f"Starting LinkedIn crawler for {len(self.keywords)} keywords in {len(self.locations)} locations")
        
        all_jobs = []
        
        for keyword in self.keywords:
            for location in self.locations:
                try:
                    self.logger.info(f"Searching for '{keyword}' in '{location}'")
                    jobs = self._search_jobs(keyword, location)
                    all_jobs.extend(jobs)
                    
                    # Don't hit the server too quickly
                    time.sleep(2)
                    
                    if len(all_jobs) >= self.limit:
                        self.logger.info(f"Reached job limit ({self.limit})")
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error searching LinkedIn for '{keyword}' in '{location}': {str(e)}")
            
            if len(all_jobs) >= self.limit:
                break
        
        # Trim to limit
        all_jobs = all_jobs[:self.limit]
        
        self.logger.info(f"Found {len(all_jobs)} jobs from LinkedIn")
        return all_jobs
    
    def _search_jobs(self, keyword, location):
        """
        Search LinkedIn for jobs with the given keyword and location
        
        Args:
            keyword (str): Job keyword
            location (str): Job location
            
        Returns:
            list: List of job dictionaries
        """
        jobs = []
        page = 0
        count = 25  # LinkedIn usually shows 25 jobs per page
        
        while True:
            # Construct search URL
            params = {
                'keywords': keyword,
                'location': location,
                'start': page * count
            }
            search_url = f"{self.search_url}?{urlencode(params)}"
            
            # Get search results page
            headers = {
                'User-Agent': self._get_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            response = requests.get(search_url, headers=headers)
            
            if response.status_code != 200:
                self.logger.warning(f"Failed to get LinkedIn search results: Status {response.status_code}")
                break
            
            # Parse the page
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract job cards
            job_cards = soup.select('div.base-card.relative.w-full.hover\\:no-underline.focus\\:no-underline.base-card--link.base-search-card.base-search-card--link.job-search-card')
            
            if not job_cards:
                self.logger.info("No more job cards found")
                break
            
            # Process each job card
            for card in job_cards:
                try:
                    job = self._parse_job_card(card)
                    if job:
                        job['source'] = 'LinkedIn'
                        jobs.append(job)
                except Exception as e:
                    self.logger.error(f"Error parsing LinkedIn job card: {str(e)}")
            
            # Move to next page
            page += 1
            
            # Check if we've reached our limit
            if len(jobs) >= self.limit:
                break
                
            # Don't hit the server too quickly
            time.sleep(1)
        
        return jobs
    
    def _parse_job_card(self, card):
        """
        Parse a job card element
        
        Args:
            card (BeautifulSoup): Job card element
            
        Returns:
            dict: Job dictionary
        """
        # Extract job title and URL
        title_elem = card.select_one('h3.base-search-card__title')
        if not title_elem:
            return None
            
        title = title_elem.text.strip()
        
        # Extract job URL
        url_elem = card.select_one('a.base-card__full-link')
        url = url_elem.get('href').strip() if url_elem else None
        
        # Skip if no URL
        if not url:
            return None
        
        # Extract company name
        company_elem = card.select_one('h4.base-search-card__subtitle a')
        company = company_elem.text.strip() if company_elem else ''
        
        # Extract location
        location_elem = card.select_one('span.job-search-card__location')
        location = location_elem.text.strip() if location_elem else ''
        
        # Extract date posted
        date_elem = card.select_one('time.job-search-card__listdate')
        date_posted = date_elem.get('datetime', '') if date_elem else ''
        
        # Extract job type if available
        job_type_elem = card.select_one('div.search-entity-media__kind')
        job_type = job_type_elem.text.strip() if job_type_elem else ''
        
        # Create job dictionary
        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': '',  # LinkedIn doesn't always show salary on search results
            'description': '',  # Would need to fetch individual job pages
            'url': url,
            'date_posted': date_posted,
            'job_type': job_type,
            'experience_level': ''  # Would need to fetch individual job pages
        }
        
        return job 