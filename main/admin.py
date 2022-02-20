from django.contrib import admin
from .models import Query, Result


class QueryAdmin(admin.ModelAdmin):
    list_display = ("query_text", "prod_article", "start_date")
    fields = ("query_text", "prod_article")


admin.site.register(Query, QueryAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = ("position", "query", "date")
    fields = ("position", "query")


admin.site.register(Result, ResultAdmin)
