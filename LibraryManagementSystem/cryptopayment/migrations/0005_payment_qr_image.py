# Generated by Django 3.1.5 on 2021-02-05 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptopayment', '0004_auto_20210205_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='qr_image',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]