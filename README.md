# VForex

VForex is a project that scrapes historical exchange data from Yahoo Finance and provides a REST API to query this data.

## Project Overview

This project consists of two main tasks:
1. Scraping Historical Exchange Data from Yahoo Finance
2. Building a REST API around the Scraped Data to Query Historical Data Between Given Periods

## Tech Stack

* Python
* Flask
* SQLite
* Selenium
* APScheduler

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── scraper.py
│   ├── storage.py
│   ├── api.py
│   ├── scheduler.py
│   └── utils.py
│
├── logs/
│   └── app.log
│
├── requirements.txt
├── README.md
└── ...
```

## Setup Instructions

### Prerequisites

* Python 3.8+
* ChromeDriver (Download from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads))
* Virtualenv (optional, but recommended)

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/vishavsingla/vforex
   cd vforex
   ```

2. **Set up a Virtual Environment (optional)**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up ChromeDriver**

   Download the ChromeDriver and place it in an accessible path. Update the `CHROMEDRIVER_PATH` in `app/config.py` accordingly.

### Configuration

Create a file named `config.py` inside the `app/` directory with the following content:

```python
CHROMEDRIVER_PATH = 'path_to_your_chromedriver'
DATABASE_PATH = 'forex_data.db'
LOG_FILE_PATH = 'logs/app.log'
```

## Running the Application

**Start the Flask Application**

   ```sh
   python run.py
   ```

## Scheduled Data Scraping

The application uses APScheduler for periodic scraping of forex data. The scheduler is initialized when you start the Flask application.

### Scheduler Periods

The following schedules are set up for data scraping:

1. **Weekly Scrape**: Runs every week
   - Scrapes data for the last 7 days (1W)
2. **Monthly Scrape**: Runs every 30 days
   - Scrapes data for the last 30 days (1M)
3. **Quarterly Scrape**: Runs every 13 weeks
   - Scrapes data for the last 90 days (3M)
4. **Semi-Annual Scrape**: Runs every 26 weeks
   - Scrapes data for the last 180 days (6M)
5. **Annual Scrape**: Runs every 52 weeks
   - Scrapes data for the last 365 days (1Y)
6. **Minute Scrape**: Runs every 3 minutes (for testing purposes)
   - Scrapes data for the last 7 days (1W)

### Time Interval Meanings

- **1W**: 1 Week (7 days)
- **1M**: 1 Month (30 days)
- **3M**: 3 Months (90 days)
- **6M**: 6 Months (180 days)
- **1Y**: 1 Year (365 days)
- **Period Range**: A period range is specified using a dash, e.g., `3M-1M`, which means data from 3 months ago to 1 month ago.(for POST request only, not for scheduling)

These intervals are used both in the scheduled scraping jobs and can be used as parameters in API requests to specify the period for which data is required.

## API Endpoints

1. `POST /api/forex-data`

   Fetch historical exchange data for a specified currency pair and period.

   **Request:**
   ```json
   {
     "from": "GBP",
     "to": "INR",
     "period": "1M"
   }
   ```

   **Response:**
   ```json
   {
     "requested_data": [
       {
         "date": "2023-07-01",
         "open": 101.0,
         "high": 102.0,
         "low": 100.0,
         "close": 101.5,
         "adj_close": 101.5,
         "volume": "1000000"
       },
       ...
     ]
   }
   ```
   

   Request with Period Range:

   **Request:**
   ```json
   {
     "from": "GBP",
     "to": "INR",
     "period": "3M-1M"
   }
   ```

   **Response:**
   ```json
   {
     "requested_data": [
       {
         "date": "2023-05-01",
         "open": 101.0,
         "high": 102.0,
         "low": 100.0,
         "close": 101.5,
         "adj_close": 101.5,
         "volume": "1000000"
       },
       ...
     ]
   }
   ```


## Running the API in Postman

1. **Start the Flask Application**

   ```sh
   flask run
   ```

2. **Open Postman**

3. **Create a New Request**
   - **Method**: POST
   - **URL**: `http://127.0.0.1:5000/api/forex-data`

4. **Set the Headers**
   - **Content-Type**: application/json

5. **Set the Body**
   ```json
   {
     "from": "GBP",
     "to": "INR",
     "period": "1M"
   }
   ```

6. **Send the Request**

   You should receive a JSON response with the requested data.

## Logging

Logs are stored in `logs/app.log`. You can view the logs for debugging and monitoring purposes.

