"""
User Profile Master
"""
from reversion import revisions as reversion
from api.alias import AliasField
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Employee Mapping
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER')
    outlook_id = models.CharField(db_column='OUTLOOK_ID', max_length=50, unique=True)
    sap_code = models.CharField(max_length=50, db_column="SAP_CODE", null=True, blank=True)
    is_active = models.BooleanField(db_column='IS_ACTIVE', default=True)
    name = AliasField(db_column='OUTLOOK_ID', blank=True, null=True)

    def __str__(self):
        return self.outlook_id

    class Meta:
        """
        Class Meta
        """
        db_table = 'MST_USER_PROFILE'
        app_label = "masters"

reversion.register(UserProfile)
