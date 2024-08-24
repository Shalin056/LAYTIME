# C:\Users\shali\Documents\shalin\test-app\masters\models\MstBRMStockOtherLoc.py

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
import reversion
from django.db import models
from api.models import BaseModel


class MstBRMStockOtherLoc(BaseModel):
    material_ref = models.CharField(db_column="MATERIAL_REF",max_length=200,blank=True,null=True)
    unit = models.CharField(db_column="UNIT",max_length=100,blank=True,null=True)
    dabuna = models.IntegerField(db_column="DABUNA",blank=True,null=True)
    paradeep = models.IntegerField(db_column="PARADEEP",blank=True,null=True)
    kirandul = models.IntegerField(db_column="KIRANDUL",blank=True,null=True)
    vizag = models.IntegerField(db_column="VIZAG",blank=True,null=True)
    
    class UI_Meta:
        ui_specs = {
            "listview": [
                "this value"
            ],
            "formview": [
                {
                    "sectionlabel": "BRM Stock Other Loc Master",
                    "cols": 2,
                    "colComponent": [
                        {
                            "label": "Material Ref",
                            "decorator": "material_ref",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Material Ref",
                            "id": "material_ref",
                            "placeholder": "Material Ref",
                            "disabled": False

                        },
                        {
                            "label": "Unit",
                            "decorator": "unit",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Unit",
                            "id": "unit",
                            "placeholder": "Unit",
                            "disabled": False

                        },
                        {
                            "label": "Dabuna",
                            "decorator": "dabuna",
                            "type": "number",
                            "required": False,
                            "message": "Enter dabuna",
                            "id": "dabuna",
                            "placeholder": "dabuna",
                            "disabled": False

                        },
                        {
                            "label": "Paradeep",
                            "decorator": "paradeep",
                            "type": "number",
                            "required": False,
                            "message": "Enter paradeep",
                            "id": "paradeep",
                            "placeholder": "paradeep",
                            "disabled": False

                        },
                        {
                            "label": "Kirandul",
                            "decorator": "kirandul",
                            "type": "number",
                            "required": False,
                            "message": "Enter kirandul",
                            "id": "kirandul",
                            "placeholder": "kirandul",
                            "disabled": False

                        },
                        {
                            "label": "Vizag",
                            "decorator": "vizag",
                            "type": "number",
                            "required": False,
                            "message": "Enter Vizag",
                            "id": "vizag",
                            "placeholder": "Vizag",
                            "disabled": False

                        },
                        {
                            "label": "Created By",
                            "decorator": "created_by",
                            "type": "textbox",
                            "required": "true",
                            "message": "Created By !",
                            "id": "created_by",
                            "placeholder": "This is Created By :",
                            "disabled": True
                        },
                        {
                            "label": "Created Date ",
                            "decorator": "created_date",
                            "required": "true",
                            "message": "Created Date ",
                            "placeholder": "Select Date",
                            "type": "date",
                            "id": "created_date",
                            "dateFormatList": "DD-MM-YYYY HH:mm:ss",
                            "disabled": True
                        },
                        {
                            "label": "Updated By ",
                            "decorator": "last_updated_by",
                            "type": "textbox",
                            "required": "true",
                            "message": "Last Updated By !",
                            "id": "last_updated_by",
                            "placeholder": "This was last Updated By:",
                            "disabled": True
                        },
                        {
                            "label": "Last Updated : ",
                            "decorator": "last_updated_date",
                            "required": "true",
                            "message": "Last Updated Date",
                            "placeholder": "Select Date",
                            "type": "date",
                            "id": "last_updated_date",
                            "dateFormatList": "DD-MM-YYYY HH:mm:ss",
                            "disabled": True
                        },
                    ]
                }
            ]
        }

    class Meta:
        # managed = False
        db_table = 'MST_BRM_STOCK_OTHER_LOC'
        # unique_together = (('p_date', 'sbu', 'plan_type', 'int_ext', 'region', 'division'),)


reversion.register(MstBRMStockOtherLoc)
