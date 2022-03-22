from django.contrib import admin
from .models import Query


class QueryAdmin(admin.ModelAdmin):
    list_display = ("queries_text", "prod_article", "start_date")
    fields = ("queries_text", "prod_article")


admin.site.register(Query, QueryAdmin)
