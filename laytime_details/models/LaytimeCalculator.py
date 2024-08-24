# C:\Users\shali\Documents\shalin\test-app\laytime_details\models\laytime_calculator.py

"""
Module for defining the LayTimeCalculator model.
"""

from django.db import models
from api.models import BaseModel
from .ShippingDetail import ShippingDetail

class LayTimeCalculator(BaseModel):
    """
    Model to calculate laytime for shipping details.
    """
    shipping_detail = models.OneToOneField(ShippingDetail, on_delete=models.CASCADE,
                                            null=True, blank=True,
                                            db_column='SHIPPING_DETAIL',
                                            related_name='laytime_calculator')
    amount = models.FloatField(db_column='AMOUNT')
    actual_time = models.FloatField(default=1703823476.82923, null=True,
                                     blank=True, db_column='ACTUAL_TIME')
    allowed_time = models.FloatField( db_column='ALLOWED_TIME')
    total_time_difference = models.FloatField( db_column='TOTAL_TIME_DIFFERENCE')
    is_time_saved = models.BooleanField( db_column='IS_TIME_SAVED')

    class Meta:
        app_label = 'laytime_details'
        db_table = 'TRANS_LAYTIME_CALCULATOR'

    def __str__(self):
        return f"{self.shipping_detail} - {self.total_time_difference}"
