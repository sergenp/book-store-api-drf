# Generated by Django 3.1.5 on 2021-02-01 15:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('commercebackend', '0007_ordermodel_ordered_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartmodel',
            name='bought_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
