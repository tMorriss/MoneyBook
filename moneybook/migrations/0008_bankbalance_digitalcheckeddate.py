# Generated by Django 2.1.7 on 2019-09-21 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneybook', '0007_checkeddate'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DigitalCheckedDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('price', models.IntegerField(default=0)),
            ],
        ),
    ]
