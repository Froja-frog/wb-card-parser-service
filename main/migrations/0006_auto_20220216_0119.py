# Generated by Django 3.2.8 on 2022-02-15 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_query_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='start_date',
            field=models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата начала отслеживания'),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=None, verbose_name='Позиция')),
                ('date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата')),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.query', verbose_name='Запрос')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
                'ordering': ('-date',),
            },
        ),
    ]
