# ETL-Crawler

A Python-based ETL (Extract, Transform, Load) system for scraping job listings, with data processing and storage capabilities. (Note: Specific platform crawlers like Indeed/LinkedIn are currently missing).

## Project Overview

This project implements an automated system for:
- Scraping job listings (requires implementation or configuration, e.g., using SerpAPI)
- Processing and transforming the collected data
- Storing the results in Excel format
- Managing the ETL process with proper logging and error handling

## Project Structure

```
ETL-Crawler/
├── src/                    # Source code directory
│   ├── crawlers/          # Web crawler implementations
│   │   └── base_crawler.py    # Base crawler class with common functionality
│   ├── processors/        # Data processing modules
│   │   └── job_processor.py   # Job data processing and transformation
│   ├── utils/            # Utility modules
│   │   ├── excel_manager.py   # Excel file handling
│   │   ├── logger.py         # Logging configuration
│   │   └── request_helper.py  # HTTP request handling
│   ├── config.py         # Configuration settings
│   └── models.py         # Data models
├── data/                 # Data storage directory
├── logs/                 # Log files directory
├── test_data/           # Test data directory
├── main.py              # Main application entry point
├── test_etl.py          # Test suite
├── requirements.txt     # Project dependencies
└── .env                 # Environment variables (not in repo)
```

## Key Components

### Crawlers
- **Base Crawler**: Abstract base class providing common crawling functionality (Specific implementations for job sites like Indeed/LinkedIn need to be added or configured, potentially using an external service like SerpAPI).

### Processors
- **Job Processor**: Handles data transformation and cleaning
- Processes raw job data into structured format
- Implements data validation and normalization

### Utilities
- **Excel Manager**: Handles Excel file operations
- **Logger**: Manages application logging
- **Request Helper**: Manages HTTP requests and responses

## Dependencies

- requests==2.31.0: HTTP requests
- beautifulsoup4==4.12.2: HTML parsing
- pandas==2.1.0: Data manipulation
- openpyxl==3.1.2: Excel file handling
- python-dotenv==1.0.0: Environment variable management
- schedule==1.2.1: Task scheduling
- lxml==4.9.3: XML/HTML processing
- tqdm==4.66.1: Progress bars

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure your environment variables
5. Run the application:
   ```bash
   python main.py
   ```

## Configuration

The application uses environment variables for configuration. Create a `.env` file based on `.env.example`. Key variables include:
- `SERPAPI_KEY`: API key for SerpAPI (used for fetching job listings if implemented this way).
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- Other configuration variables as specified in `.env.example`

## Logging

The application maintains detailed logs in the `logs/` directory:
- Separate log files for each component
- Daily log rotation
- Different log levels for different types of information

## Testing

Run the test suite:
```bash
python -m pytest test_etl.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Current Status

The project structure includes:
- A base crawler class. (Note: Specific crawlers for Indeed/LinkedIn mentioned previously are missing).
- Data processing pipeline
- Excel export functionality
- Comprehensive logging
- Test coverage
- Error handling and retry mechanisms

## Future Improvements

- Add more job platforms
- Implement database storage
- Add data visualization
- Enhance error handling
- Add more test cases
- Implement rate limiting
- Add proxy support
