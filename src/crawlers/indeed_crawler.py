"""
Indeed Crawler for job listings
"""

import re
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlparse, parse_qs
from src.crawlers.base_crawler import BaseCrawler

class IndeedCrawler(BaseCrawler):
    """
    Crawler for Indeed job listings
    """
    
    def __init__(self, locations=None, keywords=None, limit=25):
        """
        Initialize the Indeed crawler
        
        Args:
            locations (list): List of locations to search
            keywords (list): List of job keywords to search
            limit (int): Maximum number of jobs to retrieve
        """
        super().__init__()
        self.base_url = "https://www.indeed.com"
        self.locations = locations or ["remote", "united states"]
        self.keywords = keywords or ["software engineer", "data engineer", "python developer"]
        self.limit = limit
        self.session = requests.Session()
    
    def _get_headers(self):
        """Get request headers with rotating user agents"""
        headers = {
            'User-Agent': self._get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        return headers
    
    def _make_request(self, url, max_retries=3):
        """
        Make a request with retry logic and random delays
        
        Args:
            url (str): URL to request
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            requests.Response: Response object
        """
        for attempt in range(max_retries):
            try:
                # Random delay between requests
                time.sleep(random.uniform(2, 5))
                
                # Make request with session
                response = self.session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    self.logger.warning(f"Request blocked (403) on attempt {attempt + 1}")
                    # Longer delay if blocked
                    time.sleep(random.uniform(5, 10))
                else:
                    self.logger.warning(f"Request failed with status {response.status_code} on attempt {attempt + 1}")
                    
            except Exception as e:
                self.logger.error(f"Request error on attempt {attempt + 1}: {str(e)}")
                time.sleep(random.uniform(1, 3))
        
        return None
    
    def _search_jobs(self, keyword, location):
        """
        Search Indeed for jobs with the given keyword and location
        
        Args:
            keyword (str): Job keyword
            location (str): Job location
            
        Returns:
            list: List of job dictionaries
        """
        jobs = []
        start = 0
        
        while True:
            # Construct search URL
            params = {
                'q': keyword,
                'l': location,
                'start': start,
                'fromage': '14'  # Last 14 days
            }
            search_url = f"{self.base_url}/jobs?{urlencode(params)}"
            
            # Make request
            response = self._make_request(search_url)
            
            if not response:
                self.logger.warning("Failed to get search results after retries")
                break
            
            # Parse the page
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract job cards
            job_cards = soup.select('div.job_seen_beacon')
            
            if not job_cards:
                self.logger.info("No more job cards found")
                break
            
            # Process each job card
            for card in job_cards:
                try:
                    job = self._parse_job_card(card)
                    if job:
                        job['source'] = 'Indeed'
                        jobs.append(job)
                except Exception as e:
                    self.logger.error(f"Error parsing job card: {str(e)}")
            
            # Move to next page
            start += len(job_cards)
            
            # Check if we've reached our limit
            if len(jobs) >= self.limit:
                break
            
            # Don't hit the server too quickly
            time.sleep(random.uniform(2, 4))
        
        return jobs
    
    def _parse_job_card(self, card):
        """
        Parse a job card element
        
        Args:
            card (BeautifulSoup): Job card element
            
        Returns:
            dict: Job dictionary
        """
        try:
            # Extract job title and URL
            title_elem = card.select_one('h2.jobTitle span[title]')
            if not title_elem:
                return None
                
            title = title_elem.get('title', '').strip() or title_elem.text.strip()
            
            # Extract job URL
            url_elem = card.select_one('h2.jobTitle a')
            if url_elem and url_elem.get('href'):
                job_path = url_elem.get('href')
                if job_path.startswith('/'):
                    url = f"{self.base_url}{job_path}"
                else:
                    url = job_path
            else:
                return None
            
            # Extract company name
            company_elem = card.select_one('span.companyName')
            company = company_elem.text.strip() if company_elem else ''
            
            # Extract location
            location_elem = card.select_one('div.companyLocation')
            location = location_elem.text.strip() if location_elem else ''
            
            # Extract salary if available
            salary_elem = card.select_one('div.salary-snippet-container .attribute_snippet')
            salary = salary_elem.text.strip() if salary_elem else ''
            
            # Extract job snippet/description
            snippet_elem = card.select_one('div.job-snippet')
            description = snippet_elem.text.strip() if snippet_elem else ''
            
            # Extract date posted
            date_elem = card.select_one('span.date')
            date_posted = date_elem.text.strip() if date_elem else ''
            
            # Create job dictionary
            job = {
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'description': description,
                'url': url,
                'date_posted': date_posted,
                'job_type': '',  # Indeed doesn't always have this clearly marked
                'experience_level': ''  # Indeed doesn't always have this clearly marked
            }
            
            return job
            
        except Exception as e:
            self.logger.error(f"Error parsing job card: {str(e)}")
            return None 