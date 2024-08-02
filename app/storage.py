import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import logging
from .database import get_db_connection

def create_table_for_currency_pair(currency_pair):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {currency_pair} (
                date TEXT PRIMARY KEY,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                adj_close REAL,
                volume TEXT
            )
        ''')
        conn.commit()
        conn.close()
        logging.info(f"Table {currency_pair} created or exists.")
    except Exception as e:
        logging.error(f"Error creating table {currency_pair}: {e}")

def store_data_in_db(df, currency_pair, from_date_str, to_date_str):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        create_table_for_currency_pair(currency_pair)
        
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
        date_range = {from_date + timedelta(days=i) for i in range((to_date - from_date).days + 1)}

        df['Date'] = df['Date'].apply(convert_date_format)
        df_dates = set(pd.to_datetime(df['Date']))

        missing_dates = date_range - df_dates
        zero_data = {
            'Date': [],
            'Open': [],
            'High': [],
            'Low': [],
            'Close': [],
            'Adj Close': [],
            'Volume': []
        }
        for missing_date in missing_dates:
            zero_data['Date'].append(missing_date.strftime('%Y-%m-%d'))
            zero_data['Open'].append(0.0)
            zero_data['High'].append(0.0)
            zero_data['Low'].append(0.0)
            zero_data['Close'].append(0.0)
            zero_data['Adj Close'].append(0.0)
            zero_data['Volume'].append('0')
        
        zero_df = pd.DataFrame(zero_data)
        df = pd.concat([df, zero_df], ignore_index=True)
        
        for _, row in df.iterrows():
            c.execute(f'''
                INSERT OR REPLACE INTO {currency_pair} (date, open, high, low, close, adj_close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', tuple(row))
        
        conn.commit()
        conn.close()
        logging.info(f"Data stored in database successfully for {currency_pair}.")
    except Exception as e:
        logging.error(f"Error storing data in database: {e}")

def fetch_data_from_db(currency_pair, from_date_str, to_date_str):
    try:
        logging.info(f"Querying database for {currency_pair} from {from_date_str} to {to_date_str}.")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(f'''
            SELECT date, open, high, low, close, adj_close, volume
            FROM {currency_pair}
            WHERE date BETWEEN ? AND ?
        ''', (from_date_str, to_date_str))
        rows = c.fetchall()
        conn.close()
        
        columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
        result = [dict(zip(columns, row)) for row in rows]
        
        logging.info(f"Data fetched successfully from {currency_pair}.")
        return result
    except Exception as e:
        logging.error(f"Error fetching data from database: {e}")
        return []

def is_date_range_fully_covered(currency_pair, from_date_str, to_date_str):
    try:
        logging.info(f"Checking date range coverage for {currency_pair} from {from_date_str} to {to_date_str}.")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(f'''
            SELECT MIN(date), MAX(date)
            FROM {currency_pair}
            WHERE date BETWEEN ? AND ?
        ''', (from_date_str, to_date_str))
        result = c.fetchone()
        conn.close()
        
        if result and result[0] and result[1]:
            return result[0] <= from_date_str and result[1] >= to_date_str
        
        return False
    except Exception as e:
        logging.error(f"Error checking date range coverage: {e}")
        return False

def convert_date_format(date_str):
    try:
        parsed_date = datetime.strptime(date_str.strip(), '%b %d, %Y')
        return parsed_date.strftime('%Y-%m-%d')
    except Exception as e:
        logging.error(f"Error converting date format: {e}")
        return date_str
