# C:\Users\shali\Documents\shalin\test-app\masters\models\MstBRMStock.py

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


class MstBRMStock(BaseModel):
    material_ref = models.CharField(db_column="MATERIAL_REF",max_length=200,blank=True,null=True)
    raw_report = models.CharField(db_column="RAW_REPORT",max_length=500,blank=True,null=True)
    material = models.CharField(db_column="MATERIAL",max_length=200,blank=True,null=True)
    rwb = models.CharField(db_column="RWB",blank=True,null=True,max_length=200)
    total_stock_name = models.CharField(db_column="TOTAL_STOCK_NAME",blank=True,null=True,max_length=200)
    ground_stock = models.IntegerField(db_column="GROUND_STOCK",blank=True,null=True)
    
    class UI_Meta:
        ui_specs = {
            "listview": [
                "this value"
            ],
            "formview": [
                {
                    "sectionlabel": "BRM Stock Master",
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
                            "label": "Raw Report",
                            "decorator": "raw_report",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Raw Report",
                            "id": "raw_report",
                            "placeholder": "Raw Report",
                            "disabled": False

                        },
                        {
                            "label": "material",
                            "decorator": "material",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter material",
                            "id": "material",
                            "placeholder": "material",
                            "disabled": False

                        },
                        {
                            "label": "RWB",
                            "decorator": "rwb",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter rwb",
                            "id": "rwb",
                            "placeholder": "rwb",
                            "disabled": False

                        },
                        {
                            "label": "Total Stock Name",
                            "decorator": "total_stock_name",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Total Stock Name",
                            "id": "total_stock_name",
                            "placeholder": "Total Stock Name",
                            "disabled": False

                        },
                        {
                            "label": "Ground Stock",
                            "decorator": "ground_stock",
                            "type": "number",
                            "required": False,
                            "message": "Enter Ground Stock",
                            "id": "ground_stock",
                            "placeholder": "Ground Stock",
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
        db_table = 'MST_BRM_STOCK'
        # unique_together = (('p_date', 'sbu', 'plan_type', 'int_ext', 'region', 'division'),)


reversion.register(MstBRMStock)
