import pandas as pd
from typing import List, Dict
import logging
import os

def save_to_csv(raw_job_data: List[Dict], filename: str):
    """Saves raw job data (list of dictionaries) to a CSV file."""
    if not raw_job_data:
        logger.warning("No job data provided to save.")
        return

    try:
        # Ensure the data directory exists
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)

        # Define the desired fields
        desired_fields = [
            "job_title",
            "employer_name",
            "job_apply_link",
            "job_city",
            "job_state",
            "job_country",
            "job_employment_type",
            "job_is_remote",
            "job_highlights",
        ]

        # Extract only the desired fields from each job listing
        filtered_job_data = []
        for job in raw_job_data:
            filtered_job = {field: job.get(field) for field in desired_fields}
            filtered_job_data.append(filtered_job)

        # Create DataFrame from filtered job data
        df = pd.DataFrame(filtered_job_data)

        # Define the full path for the CSV file
        filepath = os.path.join(output_dir, f"{filename}.csv")

        # Save to CSV
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"Saved {len(raw_job_data)} job listings to {filepath}")

    except Exception as e:
        logger.error(f"Error saving to CSV: {e}")

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the minimum logging level

# Create a file handler
log_file = "logs/etl.log"
os.makedirs(os.path.dirname(log_file), exist_ok=True)
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)  # Set the logging level for the file handler

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the logging level for the console handler

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
