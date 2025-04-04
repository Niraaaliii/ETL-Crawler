# ETL-Crawler

A Python-based ETL (Extract, Transform, Load) system for fetching job listings from JSearch API, processing the data, and storing the results in a CSV file.

## Project Overview

This project implements an automated system for:
- Fetching job listings from JSearch API
- Processing the collected data
- Storing the results in CSV format
- Managing the ETL process with proper logging and error handling

## Project Structure

```
ETL-Crawler/
├── core/                   # Core logic directory
│   ├── config.py           # Configuration settings
│   ├── job_api_client.py   # JSearch API client
│   └── utils.py            # Utility functions (logging, CSV handling)
├── data/                   # Data storage directory
├── etl.py                  # Main application entry point
├── .env                    # Environment variables (not in repo)
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies
```

## Key Components

*   **core**: Contains the core logic of the project, including:
    *   `config.py`: Configuration settings
    *   `job_api_client.py`: JSearch API client
    *   `utils.py`: Utility functions (logging, CSV handling)
*   **etl.py**: The main application entry point, which orchestrates the ETL process.
*   **data**: The directory where the extracted job listings are stored.
*   **.env**: The file where environment variables are stored (not committed to the repository).
*   **README.md**: This file, which provides documentation for the project.
*   **requirements.txt**: Lists the project's dependencies.

## Dependencies

*   `requests`: For making HTTP requests to the JSearch API.
*   `pandas`: For data manipulation and saving to CSV.
*   `python-dotenv`: For loading environment variables from the `.env` file.

## Setup

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    ```
2.  Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the root directory and set the `API_KEY` variable with your JSearch API key.

## Usage

To run the ETL process, execute the following command:

```bash
python etl.py
```

This will fetch job listings from the JSearch API and save them to a CSV file in the `data` directory. You can specify the number of pages to fetch by modifying the `etl.py` file.

## Error Handling

The project includes error handling mechanisms to catch potential exceptions during the ETL process. Errors are logged to a file and the console, providing detailed information about the cause of the failure.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
