# Generated by Django 4.0 on 2021-12-14 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_buss_address_buss_email_buss_phone_buss_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='buss',
            name='latitude',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='buss',
            name='longitude',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]