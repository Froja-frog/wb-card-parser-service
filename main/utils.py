import datetime
from datetime import date, timedelta
from .models import Result


def get_month_dates():
    """Returns list of 30 days dates including today"""
    month_dates = [(date.today() + timedelta(days=days)).strftime("%d.%m") for days in range(-15, 16)]
    return month_dates


def _update_dates_keys(results,month_dates: list):
    for result in results:
        result_dict = result.results_dict
        [result_dict.pop(key) for key in list(result_dict.keys()) if key not in month_dates]
        for month_date in month_dates:
            if month_date not in result.results_dict:
                result.results_dict[month_date] = ''


def _sort_result_dict(result: Result):
    rd = result.results_dict
    sorted_rd = dict(sorted(rd.items(), key=lambda d: datetime.datetime.strptime(d[0], '%d.%m')))
    result.results_dict = sorted_rd


def prepare_results():
    """Prepares results to output in view"""
    month_dates = get_month_dates()
    results = Result.objects.all()
    _update_dates_keys(results, month_dates)
    for result in results:
        _sort_result_dict(result)
        result.save()
    return results
