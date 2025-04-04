#!/usr/bin/env python3
"""
Test script for ETL-Crawler components
"""

import os
import sys
import unittest
from datetime import datetime
from src.extractors.job_api_client import JobApiClient
from src.config import API_KEY, BASE_URL  # Import API_KEY, BASE_URL
from src.processors.job_processor import transform_jobs
from src.utils.excel_manager import save_to_csv # Corrected import
from src.models import JobListing

class TestETLCrawler(unittest.TestCase):
    """Test cases for ETL-Crawler components"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.test_data_dir = "test_data"
        os.makedirs(cls.test_data_dir, exist_ok=True)

    def setUp(self):
        """Set up before each test"""
        self.test_excel_path = os.path.join(self.test_data_dir, "test_jobs.xlsx")

    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists(self.test_excel_path):
            os.remove(self.test_excel_path)

    def test_api_client(self):
        """Test JobApiClient"""
        api_client = JobApiClient(api_key=API_KEY, base_url=BASE_URL)
        jobs = api_client.fetch_jobs(keywords="Software Engineer", location="Remote", pages_to_fetch=1)
        self.assertIsInstance(jobs, list)
        # Add more assertions to check job data structure if needed

    def test_job_processor(self):
        """Test job processor"""
        test_jobs = [{
            'job_id': '123',
            'job_title': 'Test Job',
            'company': 'Test Company',
            'location': 'Test Location',
            'url': 'http://test.com',
            'source': 'Test Source',
            'description': '<p>Test Description</p>',
            'date_posted': '2 days ago'
        }]
        processed_jobs = transform_jobs(test_jobs)
        self.assertEqual(len(processed_jobs), 1)

    def test_excel_manager(self):
        """Test Excel manager"""
        test_jobs = [
            JobListing(
                job_id='123',
                title='Test Job',
                company_name='Test Company',
                location='Test Location',
                url='http://test.com',
                description='Test Description',
            )
        ]
        save_to_csv(test_jobs, "test_jobs") # Corrected function call

def run_tests():
    """Run all tests"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestETLCrawler)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
