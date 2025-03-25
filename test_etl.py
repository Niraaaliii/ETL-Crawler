#!/usr/bin/env python3
"""
Test script for ETL-Crawler components
"""

import os
import sys
import unittest
from datetime import datetime
from src.crawlers.indeed_crawler import IndeedCrawler
from src.crawlers.linkedin_crawler import LinkedInCrawler
from src.processors.job_processor import JobProcessor
from src.utils.excel_manager import ExcelManager
from src.utils.logger import setup_logger

class TestETLCrawler(unittest.TestCase):
    """Test cases for ETL-Crawler components"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.logger = setup_logger("test_etl")
        cls.test_data_dir = "test_data"
        os.makedirs(cls.test_data_dir, exist_ok=True)
    
    def setUp(self):
        """Set up before each test"""
        self.test_excel_path = os.path.join(self.test_data_dir, "test_jobs.xlsx")
    
    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists(self.test_excel_path):
            os.remove(self.test_excel_path)
    
    def test_indeed_crawler(self):
        """Test Indeed crawler"""
        self.logger.info("Testing Indeed crawler...")
        crawler = IndeedCrawler(limit=2)  # Limit to 2 jobs for testing
        jobs = crawler.crawl()
        
        self.assertIsInstance(jobs, list)
        self.assertLessEqual(len(jobs), 2)
        if jobs:
            job = jobs[0]
            self.assertIn('title', job)
            self.assertIn('company', job)
            self.assertIn('url', job)
            self.assertEqual(job['source'], 'Indeed')
    
    def test_linkedin_crawler(self):
        """Test LinkedIn crawler"""
        self.logger.info("Testing LinkedIn crawler...")
        crawler = LinkedInCrawler(limit=2)  # Limit to 2 jobs for testing
        jobs = crawler.crawl()
        
        self.assertIsInstance(jobs, list)
        self.assertLessEqual(len(jobs), 2)
        if jobs:
            job = jobs[0]
            self.assertIn('title', job)
            self.assertIn('company', job)
            self.assertIn('url', job)
            self.assertEqual(job['source'], 'LinkedIn')
    
    def test_job_processor(self):
        """Test job processor"""
        self.logger.info("Testing job processor...")
        processor = JobProcessor()
        
        # Test data
        test_jobs = [{
            'title': 'Test Job',
            'company': 'Test Company',
            'location': 'Test Location',
            'url': 'http://test.com',
            'source': 'Test Source',
            'description': '<p>Test Description</p>',
            'date_posted': '2 days ago'
        }]
        
        processed_jobs = processor.process(test_jobs)
        
        self.assertEqual(len(processed_jobs), 1)
        job = processed_jobs[0]
        self.assertIn('job_id', job)
        self.assertEqual(job['title'], 'Test Job')
        self.assertEqual(job['description'], 'Test Description')  # HTML should be stripped
    
    def test_excel_manager(self):
        """Test Excel manager"""
        self.logger.info("Testing Excel manager...")
        excel_manager = ExcelManager(self.test_excel_path)
        
        # Test data
        test_jobs = [{
            'title': 'Test Job',
            'company': 'Test Company',
            'location': 'Test Location',
            'url': 'http://test.com',
            'source': 'Test Source',
            'description': 'Test Description',
            'date_posted': '2024-03-25'
        }]
        
        # Test writing
        num_added = excel_manager.update_jobs(test_jobs)
        self.assertEqual(num_added, 1)
        
        # Test reading
        df = excel_manager.read_jobs()
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['title'], 'Test Job')
        
        # Test deduplication
        num_added = excel_manager.update_jobs(test_jobs)
        self.assertEqual(num_added, 0)  # Should not add duplicates

def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestETLCrawler)
    
    # Run tests
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Return success/failure
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 