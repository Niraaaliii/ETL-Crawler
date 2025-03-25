#!/usr/bin/env python3
"""
ETL Job Crawler - Main entry point
This script orchestrates the ETL process for job listings:
1. Extract: Crawl job listings from various sources
2. Transform: Process and clean the data
3. Load: Update the Excel file with new job listings
"""

import os
import time
import schedule
from datetime import datetime
from src.crawlers.indeed_crawler import IndeedCrawler
from src.crawlers.linkedin_crawler import LinkedInCrawler
from src.processors.job_processor import JobProcessor
from src.utils.excel_manager import ExcelManager
from src.utils.logger import setup_logger

# Setup logging
logger = setup_logger("main")

def run_etl_process():
    """Execute the full ETL process"""
    start_time = time.time()
    logger.info(f"Starting ETL process at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize components
    excel_manager = ExcelManager("data/jobs.xlsx")
    job_processor = JobProcessor()
    
    # Initialize crawlers
    crawlers = [
        IndeedCrawler(),
        LinkedInCrawler()
    ]
    
    # Extract jobs from sources
    all_jobs = []
    for crawler in crawlers:
        try:
            logger.info(f"Crawling jobs from {crawler.source_name}")
            jobs = crawler.crawl()
            logger.info(f"Found {len(jobs)} jobs from {crawler.source_name}")
            all_jobs.extend(jobs)
        except Exception as e:
            logger.error(f"Error crawling {crawler.source_name}: {str(e)}")
    
    if not all_jobs:
        logger.warning("No jobs found from any source")
        return
    
    # Transform jobs
    logger.info(f"Processing {len(all_jobs)} jobs")
    processed_jobs = job_processor.process(all_jobs)
    
    # Load jobs to Excel
    logger.info("Updating Excel file with new jobs")
    excel_manager.update_jobs(processed_jobs)
    
    # Log completion
    duration = time.time() - start_time
    logger.info(f"ETL process completed in {duration:.2f} seconds")
    logger.info(f"Total jobs processed: {len(processed_jobs)}")

def schedule_job():
    """Schedule the ETL process to run at regular intervals"""
    # Run immediately on startup
    run_etl_process()
    
    # Schedule to run daily at 9 AM
    schedule.every().day.at("09:00").do(run_etl_process)
    
    logger.info("ETL process scheduled to run daily at 09:00")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Run as a scheduled job or one-time
    if os.environ.get("SCHEDULE", "false").lower() == "true":
        schedule_job()
    else:
        run_etl_process() 