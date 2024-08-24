# C:\Users\shali\Documents\shalin\test-app\laytime_details\models\shipping_stage.py

"""
Module for defining the ShippingStage model.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models import BaseModel
from .ShippingDetail import ShippingDetail

class ShippingStage(BaseModel):
    """
    Model to represent stages in shipping details.
    """
    shipping_detail = models.ForeignKey(ShippingDetail, on_delete=models.CASCADE,
                                        related_name='stages')
    count = models.BooleanField(db_column='COUNT', default = False)
    stage_name = models.CharField(max_length=255,db_column='STAGE_NAME')
    start_date_time = models.DateTimeField(db_column='START_DATE_TIME')
    end_date_time = models.DateTimeField(db_column='END_DATE_TIME')
    percentage = models.PositiveSmallIntegerField(default=100,
                                                  validators=[MinValueValidator(0),
                                                              MaxValueValidator(100)],
                                                  db_column='PERCENTAGE')

    class Meta:
        app_label = 'laytime_details'
        db_table = 'TRANS_SHIPPING_STAGE'

    def __str__(self):
        return f"{self.stage_name}-{self.shipping_detail}"
