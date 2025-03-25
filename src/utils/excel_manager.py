"""
Excel Manager utility for handling job data in Excel files
"""

import os
import pandas as pd
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger("excel_manager")

class ExcelManager:
    """
    Manages reading from and writing to Excel files for job data
    """
    
    def __init__(self, excel_path):
        """
        Initialize the Excel manager
        
        Args:
            excel_path (str): Path to Excel file
        """
        self.excel_path = excel_path
        self.ensure_excel_exists()
    
    def ensure_excel_exists(self):
        """
        Create the Excel file with proper structure if it doesn't exist
        """
        if not os.path.exists(self.excel_path):
            logger.info(f"Creating new Excel file: {self.excel_path}")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.excel_path), exist_ok=True)
            
            # Create an empty DataFrame with the right columns
            columns = [
                'job_id', 'title', 'company', 'location', 'salary', 
                'description', 'url', 'source', 'date_posted', 
                'experience_level', 'job_type', 'date_crawled'
            ]
            
            df = pd.DataFrame(columns=columns)
            
            # Save to Excel
            df.to_excel(self.excel_path, index=False, sheet_name='Jobs')
            logger.info(f"Excel file created successfully")
    
    def read_jobs(self):
        """
        Read jobs from the Excel file
        
        Returns:
            pd.DataFrame: DataFrame containing job data
        """
        try:
            if not os.path.exists(self.excel_path):
                return pd.DataFrame()
            return pd.read_excel(self.excel_path, sheet_name='Jobs')
        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            return pd.DataFrame()
    
    def update_jobs(self, new_jobs):
        """
        Update the Excel file with new job listings
        
        Args:
            new_jobs (list): List of job dictionaries
        
        Returns:
            int: Number of new jobs added
        """
        if not new_jobs:
            logger.info("No new jobs to add to Excel")
            return 0
        
        try:
            # Read existing jobs
            existing_df = self.read_jobs()
            
            # Convert new jobs to DataFrame
            new_df = pd.DataFrame(new_jobs)
            
            # Add date_crawled timestamp
            new_df['date_crawled'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Filter out jobs that already exist (based on job_id)
            if not existing_df.empty and 'job_id' in existing_df.columns and 'job_id' in new_df.columns:
                new_df = new_df[~new_df['job_id'].isin(existing_df['job_id'])]
            
            if new_df.empty:
                logger.info("All jobs already exist in the Excel file")
                return 0
            
            # Append new jobs
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Save back to Excel
            updated_df.to_excel(self.excel_path, index=False, sheet_name='Jobs')
            
            num_added = len(new_df)
            logger.info(f"Added {num_added} new jobs to Excel file")
            return num_added
            
        except Exception as e:
            logger.error(f"Error updating Excel file: {str(e)}")
            return 0 