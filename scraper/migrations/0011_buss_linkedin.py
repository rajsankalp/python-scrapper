# Generated by Django 4.0.1 on 2022-01-30 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0010_buss_availablity_json_buss_donation_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='buss',
            name='linkedin',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]