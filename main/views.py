from django.shortcuts import render
from .utils import get_month_dates, prepare_results
from .parser import Parser
from .models import Result


def index(request):
    month_dates = get_month_dates()
    parser = Parser()
    parser.run()
    results = prepare_results()
    context = {'month_dates': month_dates, 'results': results}
    return render(request, "main/index.html", context)
