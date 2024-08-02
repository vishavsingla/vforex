from datetime import datetime, timedelta

def convert_period_to_dates(period):
    today = datetime.now() - timedelta(days=1)
    
    if period == '1W':
        start_date = today - timedelta(days=7)
    elif period == '1F':
        start_date = today - timedelta(days=14)
    elif period == '1M':
        start_date = today - timedelta(days=30)
    elif period == '3M':
        start_date = today - timedelta(days=90)
    elif period == '6M':
        start_date = today - timedelta(days=180)
    elif period == '1Y':
        start_date = today - timedelta(weeks=52)
    else:
        start_date = today - timedelta(days=365)

    return start_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')
