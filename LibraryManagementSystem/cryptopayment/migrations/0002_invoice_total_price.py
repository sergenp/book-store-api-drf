# Generated by Django 3.1.5 on 2021-02-05 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptopayment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]