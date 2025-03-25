"""
Job Processor module for transforming job data
"""

import re
import hashlib
import pandas as pd
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger("job_processor")

class JobProcessor:
    """
    Processes raw job data to clean and standardize it
    """
    
    def __init__(self):
        """Initialize the job processor"""
        pass
    
    def process(self, jobs):
        """
        Process a list of jobs
        
        Args:
            jobs (list): List of job dictionaries from crawlers
            
        Returns:
            list: List of processed job dictionaries
        """
        processed_jobs = []
        
        for job in jobs:
            try:
                processed_job = self._process_job(job)
                if processed_job:
                    processed_jobs.append(processed_job)
            except Exception as e:
                logger.error(f"Error processing job: {str(e)}")
        
        logger.info(f"Processed {len(processed_jobs)} jobs")
        return processed_jobs
    
    def _process_job(self, job):
        """
        Process a single job
        
        Args:
            job (dict): Job dictionary from crawler
            
        Returns:
            dict: Processed job dictionary
        """
        # Ensure all required fields are present
        required_fields = ['title', 'company', 'url', 'source']
        for field in required_fields:
            if field not in job or not job[field]:
                logger.warning(f"Job missing required field: {field}")
                return None
        
        # Create a processed job dictionary
        processed_job = {
            'title': self._clean_text(job['title']),
            'company': self._clean_text(job['company']),
            'url': job['url'],
            'source': job['source'],
        }
        
        # Generate a unique job ID
        job_id_str = f"{processed_job['title']}:{processed_job['company']}:{processed_job['url']}"
        processed_job['job_id'] = hashlib.md5(job_id_str.encode()).hexdigest()
        
        # Process optional fields
        processed_job['location'] = self._clean_text(job.get('location', ''))
        processed_job['salary'] = self._clean_text(job.get('salary', ''))
        processed_job['description'] = self._clean_text(job.get('description', ''))
        processed_job['date_posted'] = self._parse_date(job.get('date_posted', ''))
        processed_job['experience_level'] = self._clean_text(job.get('experience_level', ''))
        processed_job['job_type'] = self._clean_text(job.get('job_type', ''))
        
        return processed_job
    
    def _clean_text(self, text):
        """
        Clean text by removing extra whitespace and special characters
        
        Args:
            text (str): Text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ''
        
        # Convert to string if not already
        text = str(text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Replace multiple whitespace with a single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _parse_date(self, date_str):
        """
        Parse date string into a standard format
        
        Args:
            date_str (str): Date string to parse
            
        Returns:
            str: Standardized date string (YYYY-MM-DD)
        """
        if not date_str:
            return ''
        
        try:
            # Handle "x days ago" format
            days_ago_match = re.search(r'(\d+)\s*days?\s*ago', date_str, re.IGNORECASE)
            if days_ago_match:
                days = int(days_ago_match.group(1))
                date = datetime.now().date() - pd.Timedelta(days=days)
                return date.strftime('%Y-%m-%d')
            
            # Handle other common formats
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%B %d, %Y', '%b %d, %Y']:
                try:
                    date = datetime.strptime(date_str, fmt)
                    return date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # If we can't parse it, return as is
            return date_str
            
        except Exception:
            return date_str 