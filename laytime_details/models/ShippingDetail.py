# C:\Users\shali\Documents\shalin\test-app\laytime_details\models\shipping_detail.py

"""
Model definition for ShippingDetail in Laytime Details app.
"""

from decimal import Decimal
from django.db import models
from api.models import BaseModel
from django.core.validators import MinValueValidator

RATE_TYPE_CHOICES = (
    ("loading", "loading"),
    ("discharge", "discharge")
)

class ShippingDetail(BaseModel):
    """
    Model representing shipping details.
    """
    vessel = models.CharField(max_length=100, null=True, blank=True, db_column='VESSEL')
    bl_date = models.DateField(null=True, blank=True, db_column='BL_DATE')
    load_port = models.CharField(max_length=40,null=True, blank=True, db_column='LOAD_PORT')
    discharge_port = models.CharField(max_length=40,null=True, blank=True,
                                       db_column='DISCHARGE_PORT')
    turn_time_hours = models.FloatField(db_column='TURN_TIME_HOURS')
    cargo = models.CharField(max_length=100,null=True, blank=True,
                              db_column='CARGO')
    shipper_supplier = models.CharField(max_length=100,null=True, blank=True,
                                         db_column='SHIPPER_SUPPLIER')
    demurrage_rate_per_day = models.DecimalField(max_digits=10, decimal_places=2,
                                                  db_column='DEMURRAGE_RATE_PER_DAY')
    despatch_rate_per_day = models.DecimalField(max_digits=10, decimal_places=2,
                                                 db_column='DESPATCH_RATE_PER_DAY')
    cargo_qty = models.FloatField( db_column='CARGO_QTY', validators=[MinValueValidator(0),])
    rate_type = models.CharField( db_column='RATE_TYPE', choices=RATE_TYPE_CHOICES, max_length=20)
    discharge_rate = models.FloatField( db_column='DISCHARGE_RATE')
    allowed_time = models.FloatField( db_column='ALLOWED_TIME')
    charter_type = models.CharField(max_length=100,null=True, blank=True,
                                     db_column='CHARTER_TYPE')
    receiver_buyer = models.CharField(max_length=100,null=True, blank=True,
                                       db_column='RECEIVER_BUYER')
    nor_tendered = models.DateTimeField( db_column='NOR_TENDERED')
    commenced_loading_time = models.DateTimeField( db_column='COMMENCED_TIME')
    completed_loading_time = models.DateTimeField( db_column='COMPLETED_TIME')
    remarks = models.CharField(max_length=200,null=True, blank=True, db_column = 'REMARKS')

    class Meta:
        app_label = 'laytime_details'
        db_table = 'TRANS_SHIPPING_DETAIL'

    def get_exchange_rate(self):
        """
        Get the exchange rate.
        """
        return 83.94

    def check_ceo_approval(self):
        """
        function will add CEO in approval Hierarchy
        """
        amount = self.laytime_calculator.amount * self.get_exchange_rate()
        if amount >= Decimal(10000000):
            return True
        return False

    def check_cfo_approval(self):
        """
        function will add CFO in approval Hierarchy
        """
        amount = self.laytime_calculator.amount * self.get_exchange_rate()
        if amount >=  Decimal(50000000):
            return True
        return False

    def return_split_quantity_approvers(self):
        """
        Return the count of split quantity approvers.
        """
        split_quantities = self.split_quantities.all()
        count = split_quantities.count()
        return count if count != 0 else 1

    def __str__(self):
        return f"{self.id} - {self.vessel}"
