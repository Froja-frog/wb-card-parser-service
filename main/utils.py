from datetime import date, timedelta


def get_month_dates():
    """Returns list of 30 days dates including today"""
    month_dates = [(date.today() + timedelta(days=days)).strftime("%d.%m") for days in range(-15, 16)]
    return month_dates
