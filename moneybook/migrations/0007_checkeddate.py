# Generated by Django 2.1.7 on 2019-09-21 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneybook', '0006_auto_20190916_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckedDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moneybook.Method')),
            ],
        ),
    ]
