# Generated by Django 2.1.7 on 2019-09-16 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moneybook', '0005_fixedcost'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='fixedCost',
            new_name='FixedCostPlan',
        ),
    ]
