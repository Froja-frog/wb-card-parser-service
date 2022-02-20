from django.db import models


class Query(models.Model):
    """Model of query to search product at wilderries"""
    query_text = models.CharField(max_length=200, db_index=True, verbose_name="Запрос / Ключевое слово", unique=True)
    prod_article = models.CharField(max_length=30, verbose_name='Артикул товара')
    start_date = models.DateField(db_index=True, auto_now_add=True, verbose_name='Дата начала отслеживания')

    def __str__(self):
        return self.query_text

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
        

class Result(models.Model):
    """Model of results of parsing to put in view"""
    position = models.CharField(max_length=5,default=None, verbose_name='Позиция')
    query = models.ForeignKey(Query, on_delete=models.CASCADE, verbose_name='Запрос')
    date = models.DateField(db_index=True, auto_now_add=True, verbose_name='Дата', unique=True)

    def __str__(self):
        return f"{self.query.query_text}: {self.date}"

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
        ordering = ('date',)
