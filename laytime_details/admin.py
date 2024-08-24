# C:\Users\shali\Documents\shalin\test-app\laytime_details\admin.py

"""
Admin configuration for Laytime Details models.
"""

from django.contrib import admin
from .models import ShippingDetail, SplitQuantity

# Register your models here.

admin.site.register(ShippingDetail)
admin.site.register(SplitQuantity)
