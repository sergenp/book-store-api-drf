# Generated by Django 3.1.5 on 2021-01-24 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commercebackend", "0002_auto_20210124_1937"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartmodel",
            name="shipping",
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="shipping",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="commercebackend.shippingmodel",
            ),
            preserve_default=False,
        ),
    ]
