# Generated by Django 2.2.5 on 2019-09-08 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneybook', '0002_auto_20190908_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateField(),
        ),
    ]