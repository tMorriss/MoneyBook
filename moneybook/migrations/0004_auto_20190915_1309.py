# Generated by Django 2.1.7 on 2019-09-15 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneybook', '0003_auto_20190908_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='method',
            old_name='order',
            new_name='show_order',
        ),
    ]
