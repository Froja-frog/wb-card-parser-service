import datetime
from datetime import date, timedelta

from django.db.models import QuerySet

from .models import Result


def get_month_dates():
    """Returns list of 30 days dates including today"""
    month_dates = [(date.today() + timedelta(days=days)).strftime("%d.%m") for days in range(-15, 16)]
    return month_dates


def _update_dates_keys(results: QuerySet[Result], month_dates: list):
    for result in results:
        result_dict: dict = result.results_dict
        for query_key in result_dict.keys():
            [result_dict[query_key].pop(key) for key in list(result_dict[query_key].keys()) if key not in month_dates]
            for month_date in month_dates:
                if month_date not in result_dict.get(query_key):
                    result_dict.get(query_key)[month_date] = ''


def _sort_result_dict(result: Result):
    rd = result.results_dict
    for key in rd.keys():
        sorted_rd = dict(sorted(rd.get(key).items(), key=lambda d: datetime.datetime.strptime(d[0], '%d.%m')))
        rd[key] = sorted_rd


def prepare_results():
    """Prepares results to output in view"""
    month_dates = get_month_dates()
    results = Result.objects.all()
    _update_dates_keys(results, month_dates)
    for result in results:
        _sort_result_dict(result)
        result.save()
    return results
