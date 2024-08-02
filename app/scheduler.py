from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import logging
from .scraper import scrape_historical_data
from .storage import store_data_in_db, is_date_range_fully_covered
from .utils import convert_period_to_dates

def scheduled_scrape(interval):
    logging.info(f"Scheduled scraping job started for interval: {interval}.")
    currency_pairs = [
        ('GBP', 'INR'),
        ('AED', 'INR')
    ]
    
    for from_currency, to_currency in currency_pairs:
        currency_pair = f"{from_currency}_{to_currency}"
        quote = f'{from_currency}{to_currency}=X'
        from_date_str, to_date_str = convert_period_to_dates(interval)
        
        if not is_date_range_fully_covered(currency_pair, from_date_str, to_date_str):
            logging.info(f"Scraping data for {currency_pair} from {from_date_str} to {to_date_str}.")
            scraped_df = scrape_historical_data(quote, from_date_str, to_date_str)
            if not scraped_df.empty:
                store_data_in_db(scraped_df, currency_pair, from_date_str, to_date_str)
            else:
                logging.warning(f"Failed to scrape data for {currency_pair} from {from_date_str} to {to_date_str}.")
    logging.info("Scheduled scraping job completed.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_scrape,replace_existing=True, trigger=IntervalTrigger(weeks=1), id='weekly_scrape', args=['1W'])
    scheduler.add_job(scheduled_scrape,replace_existing=True, trigger=IntervalTrigger(days=30), id='monthly_scrape', args=['1M'])
    scheduler.add_job(scheduled_scrape,replace_existing=True, trigger=IntervalTrigger(weeks=13), id='quarterly_scrape', args=['3M'])
    scheduler.add_job(scheduled_scrape,replace_existing=True, trigger=IntervalTrigger(weeks=26), id='semiannual_scrape', args=['6M'])
    scheduler.add_job(scheduled_scrape,replace_existing=True, trigger=IntervalTrigger(weeks=52), id='annual_scrape', args=['1Y'])
    scheduler.add_job(scheduled_scrape,replace_existing=True, trigger=IntervalTrigger(weeks=52), id='annual_scrape', args=['1Y'])
    
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
