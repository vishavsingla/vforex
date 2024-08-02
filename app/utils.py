from datetime import datetime, timedelta

def convert_period_to_dates(period):
    today = datetime.now() - timedelta(days=1)
    
    # Check if the period contains a dash indicating a range
    if '-' in period:
        start_period, end_period = period.split('-')

        def get_days_from_period(period):
            if period == '1W':
                return 7
            elif period == '2W':
                return 14
            elif period == '1M':
                return 30
            elif period == '3M':
                return 90
            elif period == '6M':
                return 180
            elif period == '1Y':
                return 365
            else:
                raise ValueError(f"Unknown period: {period}")
        
        start_days = get_days_from_period(start_period)
        end_days = get_days_from_period(end_period)
        start_date = today - timedelta(days=start_days)
        end_date = today - timedelta(days=end_days)
    
    else:
        # Single period, calculate the start date based on the given period
        if period == '1W':
            start_date = today - timedelta(days=7)
        elif period == '2W':
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
            raise ValueError(f"Unknown period: {period}")
        end_date = today

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
