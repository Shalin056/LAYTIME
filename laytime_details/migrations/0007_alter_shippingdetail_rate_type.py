# Generated by Django 4.0.4 on 2024-04-16 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laytime_details', '0006_shippingdetail_rate_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingdetail',
            name='rate_type',
            field=models.CharField(blank=True, db_column='RATE_TYPE', max_length=255, null=True),
        ),
    ]
