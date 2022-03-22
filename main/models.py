from django.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField, JSONField


class Query(models.Model):
    """Model of query to search product at wilderries"""
    queries_text = models.CharField(max_length=200, db_index=True, verbose_name='Запрос(ы)', default='')
    prod_article = models.CharField(max_length=20, db_index=True, verbose_name='Артикул')
    start_date = models.DateField(db_index=True, auto_now_add=True, verbose_name='Дата начала отслеживания')

    def __str__(self):
        return f"Запрос {self.prod_article}"

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'


class Result(models.Model):
    """Model of results of parsing to put in view"""
    query = models.ForeignKey(Query, on_delete=models.CASCADE, verbose_name='Запрос')
    results_dict = models.JSONField(verbose_name='Результаты', default=dict)

    def __str__(self):
        return f"Результат: {self.query.prod_article})"

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
