# Generated by Django 4.0.4 on 2024-04-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laytime_details', '0002_alter_shippingstage_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingdetail',
            name='demurrage_reason',
            field=models.CharField(blank=True, db_column='DEMURRAGE_REASON', max_length=255, null=True),
        ),
    ]
