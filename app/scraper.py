import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import logging

from .config import Config

def scrape_historical_data(quote, from_date, to_date):
    try:
        from_timestamp = int(time.mktime(datetime.strptime(from_date, '%Y-%m-%d').timetuple()))
        to_timestamp = int(time.mktime(datetime.strptime(to_date, '%Y-%m-%d').timetuple()))
        url = f"https://finance.yahoo.com/quote/{quote}/history?period1={from_timestamp}&period2={to_timestamp}&interval=1d"
        
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.headless = True
        
        driver = webdriver.Chrome(service=Service(Config.CHROMEDRIVER_PATH), options=options)
        driver.get(url)
        time.sleep(5)

        table = driver.find_element(By.CLASS_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        data = []
        headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, 'th')]
        
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) > 1:
                row_data = [col.text for col in cols]
                data.append(row_data)
        
        driver.quit()
        logging.info(f"Data scraped successfully for {quote} from {from_date} to {to_date}.")
        return pd.DataFrame(data, columns=headers)
    except Exception as e:
        logging.error(f"Error scraping data: {e}")
        return pd.DataFrame()
