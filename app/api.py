from flask import Blueprint, jsonify, request
from .scraper import scrape_historical_data
from .storage import store_data_in_db, fetch_data_from_db, is_date_range_fully_covered
from .utils import convert_period_to_dates
from .config import Config

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/forex-data', methods=['POST'])
def request_json():
    data = request.get_json()
    from_currency = data['from']
    to_currency = data['to']
    period = data['period']
    
    currency_pair = f"{from_currency}_{to_currency}"
    quote = f'{from_currency}{to_currency}=X'
    from_date_str, to_date_str = convert_period_to_dates(period)
    
    if is_date_range_fully_covered(currency_pair, from_date_str, to_date_str):
        db_data = fetch_data_from_db(currency_pair, from_date_str, to_date_str)
        return jsonify({"requested_data": db_data})
    
    scraped_df = scrape_historical_data(quote, from_date_str, to_date_str)
    if scraped_df.empty:
        return jsonify({"error": "Failed to retrieve data from Yahoo Finance."}), 500

    store_data_in_db(scraped_df, currency_pair, from_date_str, to_date_str)
    
    db_data = fetch_data_from_db(currency_pair, from_date_str, to_date_str)
    return jsonify({"requested_data": db_data})
