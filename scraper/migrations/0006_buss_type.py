# Generated by Django 4.0 on 2021-12-16 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_buss_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='buss',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
