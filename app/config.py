import os

class Config:
    CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH', 'C:/Users/visha/Downloads/chromedriver-win64/chromedriver.exe')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'forex_data.db')
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG').upper()
