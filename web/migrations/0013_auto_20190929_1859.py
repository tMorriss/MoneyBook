# Generated by Django 2.1.7 on 2019-09-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20190921_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
