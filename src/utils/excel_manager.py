import pandas as pd
from typing import List, Dict
from src.utils.logger import logger
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

        # Create DataFrame directly from the list of dictionaries
        # Pandas will automatically create columns for all keys found in the dictionaries.
        # Missing keys in some dictionaries will result in NaN values.
        df = pd.DataFrame(raw_job_data)

        # Define the full path for the CSV file
        filepath = os.path.join(output_dir, f"{filename}.csv")

        # Save to CSV
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"Saved {len(raw_job_data)} job listings to {filepath}")

    except Exception as e:
        logger.error(f"Error saving to CSV: {e}")
