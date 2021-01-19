# Generated by Django 3.1.5 on 2021-01-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryfrontend', '0003_auto_20210119_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authormodel',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='authormodel',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='authormodel',
            name='death_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='authormodel',
            name='is_test_data',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='bookmodel',
            name='is_test_data',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='bookmodel',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categorymodel',
            name='is_test_data',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='publishermodel',
            name='is_test_data',
            field=models.BooleanField(default=True),
        ),
    ]
