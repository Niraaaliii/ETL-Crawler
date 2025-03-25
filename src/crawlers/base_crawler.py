"""
Base Crawler class for job sources
"""

from abc import ABC, abstractmethod
from src.utils.logger import setup_logger

logger = setup_logger("base_crawler")

class BaseCrawler(ABC):
    """
    Abstract base class for job crawlers
    All job source crawlers should inherit from this class
    """
    
    def __init__(self):
        """Initialize the crawler"""
        self.source_name = self.__class__.__name__.replace('Crawler', '')
        self.logger = setup_logger(self.__class__.__name__)
    
    @abstractmethod
    def crawl(self):
        """
        Crawl the job source and return a list of job dictionaries
        
        Returns:
            list: List of job dictionaries
        """
        pass
    
    def _get_user_agent(self):
        """
        Get a random user agent string
        
        Returns:
            str: User agent string
        """
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        ]
        
        import random
        return random.choice(user_agents) 