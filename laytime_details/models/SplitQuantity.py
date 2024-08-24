# C:\Users\shali\Documents\shalin\test-app\laytime_details\models\split_quantity.py

"""
Model definition for SplitQuantity in Laytime Details app.
"""

from django.db import models
from api.models import BaseModel
from .ShippingDetail import ShippingDetail

class SplitQuantity(BaseModel):
    """
    Model representing split quantities in shipping details.
    """
    shipping_detail = models.ForeignKey(ShippingDetail, on_delete=models.CASCADE,
                                        null=True, related_name='split_quantities')
    port_name = models.CharField(max_length=100, db_column='PORT_NAME')
    cargo_quantity = models.FloatField(db_column='CARGO_QUANTITY', default=0.0)
    amount = models.FloatField(db_column='AMOUNT')
    remaining_cargo_qty = models.FloatField(db_column='REMAINING_CARGO_QUANTITY',
                                            default=0.0, null=True, blank=True)

    class Meta:
        app_label = 'laytime_details'
        db_table = 'TRANS_SPLIT_QUANTITY'

    def __str__(self):
        return f"{self.port_name} - {self.shipping_detail}"
