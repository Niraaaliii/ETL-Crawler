# ETL-Crawler

An ETL (Extract, Transform, Load) tool for crawling job listings from various job boards.

## Features

- Crawls job listings from Indeed and LinkedIn
- Extracts detailed job information including title, company, location, salary, and description
- Processes and normalizes job data
- Stores results in Excel format
- Configurable search parameters
- Anti-blocking measures and rate limiting
- Comprehensive logging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ETL-Crawler.git
cd ETL-Crawler
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file:
```bash
cp .env.example .env
```

5. Configure your environment variables in `.env`

## Usage

1. Run the crawler:
```bash
python main.py
```

2. Run tests:
```bash
python test_etl.py
```

## Configuration

The crawler can be configured through:
- `src/config.py` - Main configuration file
- `.env` - Environment variables
- Command line arguments

## Project Structure

```
ETL-Crawler/
├── src/
│   ├── crawlers/         # Job board crawlers
│   ├── processors/       # Data processing
│   ├── utils/           # Utility functions
│   └── config.py        # Configuration
├── data/                # Output directory
├── logs/                # Log files
├── tests/               # Test files
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Please respect the terms of service of the job boards you're crawling. 