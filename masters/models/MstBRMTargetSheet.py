# C:\Users\shali\Documents\shalin\test-app\masters\models\MstBRMTargetSheet.py

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from .MstBRMStock import MstBRMStock
import reversion
from django.db import models
from api.models import BaseModel

class MstBRMTargetSheet(BaseModel):
    vessel = models.CharField(db_column='VESSEL', max_length=100)
    cargo = models.CharField(db_column='CARGO', max_length=100, blank=True, null=True)
    source_port = models.CharField(db_column='SOURCE_PORT', max_length=200, blank=True, null=True)
    discharge_port = models.CharField(db_column='DISCHARGE_PORT', max_length=200, blank=True, null=True)
    qty = models.IntegerField(db_column="QTY",blank=True,null=True)
    loadport_date = models.CharField(db_column="LOADPORT_DATE",blank=True,null=True,max_length=200)
    arrival = models.DateField(db_column='ARRIVAL', blank=True, null=True)
    today_position = models.CharField(db_column='TODAY_POSITION', max_length=200, blank=True, null=True)
    remarks = models.CharField(db_column="REMARKS",max_length=500,blank=True,null=True)
    dem = models.FloatField(db_column='DEM', blank=True, null=True)
    discharge_rate_berth = models.FloatField(db_column='DISCHARGE_RATE_BERTH', blank=True, null=True)
    shared_cargo = models.CharField(db_column="SHARED_CARGO",blank=True,null=True,default="N",max_length=10)
    stage = models.CharField(db_column="STAGE",max_length=200,blank=True,null=True)
    con_or_tbn = models.CharField("CON_OR_TBN",max_length=200,blank=True,null=True)
    material_n_lp = models.CharField("MATERIAL_N_LP",max_length=500,blank=True,null=True)
    vessel_cargo_arrival = models.CharField(db_column="VESSEL_CARGO_ARRIVAL",max_length=200,blank=True,null=True)
    major = models.CharField(db_column="MAJOR",blank=True,null=True,default='Y',max_length=10)
    material_ref = models.CharField(db_column="MATERIAL_REF",max_length=200,blank=True,null=True)
    material = models.CharField(db_column="MATERIAL",max_length=200,blank=True,null=True)
    rwb = models.CharField(db_column="RWB",blank=True,null=True,max_length=200)
    ground_stock = models.IntegerField(db_column="GROUND_STOCK",blank=True,null=True)

    def save(self, *args, **kwargs):
        self.material_n_lp = self.cargo + " " +  self.source_port
        super(MstBRMTargetSheet, self).save(*args, **kwargs)
    
    class UI_Meta:
        ui_specs = {
            "listview": [
                "this value"
            ],
            "formview": [
                {
                    "sectionlabel": "BRM Target Sheet Master",
                    "cols": 2,
                    "colComponent": [
                       
                        {
                            "label": "Vessel",
                            "decorator": "vessel",
                            "type": "textbox",
                            "required": "true",
                            "message": "Enter Vessel",
                            "id": "vessel",
                            "placeholder": "Enter Vessel",
                            "disabled": False
                        },
                        {
                            "label": "Cargo",
                            "decorator": "cargo",
                            "type": "select",
                            "required": False,
                            "message": "Select cargo",
                            "validator": None,
                            "validateStatus": None,
                            "id": "cargo",
                            "placeholder": "Please Select cargo",
                            "listed": "yes",
                            "link_api":"cargo",
                            "list_data": [
                                {"INGWE":"INGWE"},
                                {"Thermal Coal":"Thermal Coal"},
                                {"Poland BF Coke":"Poland BF Coke"},
                                {"Russian BF Coke":"Russian BF Coke"},
                                {"BPCI":"BPCI "},
                                {"VSKPCI":"VSKPCI"},
                                {"HFCCoal":"HFCCoal"},
                                {"Tweefontein":"Tweefontein"},
                                {"Japan BF Coke":"Japan BF Coke"},
                                {"Poland nut Coke":"Poland nut Coke"},
                                {"BF_Pdp":"BF_Pdp"},
                                {"DR_Pdp":"DR_Pdp"},
                                {"DR_Vzg":"DR_Vzg"},
                                {"Oxide Fines":"Oxide Fines"},
                                {"Hazira Fines":"Hazira Fines"},
                                {"BF_CLO":"BF_CLO"},
                                {"DR_CLO":"DR_CLO"},
                                {"DR_CLO":"DR_CLO"},
                                {"Mill Scale":"Mill Scale"},
                                {"Concentrate Slurry":"Concentrate Slurry"},
                                {"LS 3060":"LS 3060"},
                                {"DM 4080":"DM 4080"},
                                {"LS 06":"LS 06"},
                                {"PYROXENITE":"PYROXENITE"},
                                {"DM 06":"DM 06"},
                                {"LS 1040":"LS 1040"},
                                {"LS 1040":"LS 1040"},
                                {"DM 1040":"DM 1040"},
                                {"Anthracite Coal":"Anthracite Coal"},
                                {"PYROXENYTE 0-6 Mina Saqr":"PYROXENYTE 0-6 Mina Saqr"},
                                {"Tweefontein":"Tweefontein"},
                                {"Mafube":"Mafube"},
                            ],
                            "disabled": False
                        },
                        {
                            "label": "Source Port",
                            "decorator": "source_port",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Source Port",
                            "id": "source_port",
                            "placeholder": "Source Port",
                            "disabled": False

                        },
                        {
                            "label": "Discharge Port",
                            "decorator": "discharge_port",
                            "type": "select",
                            "required": False,
                            "message": "Select Discharge Port",
                            "validator": None,
                            "validateStatus": None,
                            "id": "discharge_port",
                            "placeholder": "Please Select Discharge Port",
                            "listed": "yes",
                            "link_api":"discharge_port",
                            "list_data": [
                                {"Hazira":"Hazira"},
                                {"Vizag":"Vizag"},
                                {"Paradeep":"Paradeep"},
                                {"Khopoli":"Khopoli"},
                            ],
                            "disabled": False
                        },
                        {
                            "label": "Qty",
                            "decorator": "qty",
                            "type": "number",
                            "required": False,
                            "message": "Enter qty",
                            "id": "qty",
                            "placeholder": "qty",
                            "disabled": False

                        },
                        {
                            "label": "Loadport Date",
                            "decorator": "loadport_date",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Source Port",
                            "id": "source_port",
                            "placeholder": "Source Port",
                            "dateFormatList": "DD-MM-YYYY",
                            "disabled": False
                        },
                        {
                            "label": "Arrival",
                            "decorator": "arrival",
                            "required": False,
                            "message": "Arrival",
                            "placeholder": "Select Date",
                            "type": "date",
                            "id": "arrival",
                            "dateFormatList": "DD-MM-YYYY",
                            "disabled": False
                        },
                        {
                            "label": "Today Position",
                            "decorator": "today_position",
                            "type": "select",
                            "required": False,
                            "message": "Select Today Position",
                            "validator": None,
                            "validateStatus": None,
                            "id": "today_position",
                            "placeholder": "Please Select Today Position",
                            "listed": "yes",
                            "link_api":"today_position",
                            "list_data": [
                                {"Awaiting at Hazira":"Awaiting at Hazira"},
                                {"Sailed for Hazira ":"Sailed for Hazira "},
                                {"To Arrive at Load Port":"To Arrive at Load Port"},
                                {"Discharging at Hazira":"Discharging at Hazira"},
                                {"Awaiting at Load Port":"Awaiting at Load Port"},
                                {"Loading at Load Port":"Loading at Load Port"},
                                {"Being Lightened - Hazira":"Being Lightened - Hazira"},
                                {"To load from Load Port":"To load from Load Port"},
                                {"Vessel to be Nominated":"Vessel to be Nominated"},
                                {"Waiting to load at Load Port":"Waiting to load at Load Port"},
                                {"Discharging at Adani":"Discharging at Adani"},
                                {"Barge to be Nominated":"Barge to be Nominated"},
                                {"Loading Stalled":"Loading Stalled"},
                                {"Report Awaited":"Report Awaited"},
                                {"Sailed for Vizag":"Sailed for Vizag"},
                                {"Sailed for Paradeep":"Sailed for Paradeep"},
                                {"Discharging at Vizag":"Discharging at Vizag"},
                                {"Discharging at Paradeep":"Discharging at Paradeep"},
                                {"Loaded but Vsl Breakdown":"Loaded but Vsl Breakdown"},
                                {"Waiting to Discharge":"Waiting to Discharge"},
                                {"Vessel to be Nominated by AMNSI":"Vessel to be Nominated by AMNSI"},
                                {"Sailed for Adani":"Sailed for Adani"},
                                {"Awaiting at Adani":"Awaiting at Adani"},
                                {"Awaiting at Paradeep":"Awaiting at Paradeep"},
                                {"Awaiting at Vizag":"Awaiting at Vizag"},
                                {"Sailed for Chennai":"Sailed for Chennai"},
                                {"Sailed for Kandla":"Sailed for Kandla"},
                                {"Anchorage loading at Hazira":"Anchorage loading at Hazira"},

                            ],
                            "disabled": False
                        },
                        
                        {
                            "label": "Remarks",
                            "decorator": "remarks",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Remarks",
                            "id": "remarks",
                            "placeholder": "Remarks",
                            "disabled": False

                        },
                        {
                            "label": "Dem",
                            "decorator": "dem",
                            "type": "number",
                            "required": False,
                            "message": "Enter dem",
                            "id": "dem",
                            "placeholder": "dem",
                            "disabled": False

                        },
                        {
                            "label": "Discharge Rate Berth",
                            "decorator": "discharge_rate_berth",
                            "type": "number",
                            "required": False,
                            "message": "Enter discharge rate berth",
                            "id": "discharge_rate_berth",
                            "placeholder": "discharge rate berth",
                            "disabled": False

                        },
                        {
                            "label": "Shared Cargo",
                            "decorator": "shared_cargo",
                            "type": "select",
                            "required": False,
                            "message": "Select Shared Cargo",
                            "validator": None,
                            "validateStatus": None,
                            "id": "shared_cargo",
                            "placeholder": "Please Select Shared Cargo",
                            "listed": "yes",
                            "list_data": [
                                {"Y":"Y"},
                                {"N":"N"},
                            ],
                            "link_api":"shared_cargo",
                            "disabled": False
                        },
                        {
                            "label": "Stage",
                            "decorator": "stage",
                            "type": "select",
                            "required": False,
                            "message": "Select stage",
                            "validator": None,
                            "validateStatus": None,
                            "id": "stage",
                            "placeholder": "Please Select stage",
                            "listed": "yes",
                            "link_api":"stage",
                            "list_data": [
                                {"Discharge Port":"Discharge Port"},
                                {"Sailed":"Sailed"},
                                {"Yet to arrive at Loadport":"Yet to arrive at Loadport"},
                                {"Loadport":"Loadport"},
                                {"Yet nominated":"Yet nominated"},
                                {"Report Awaited":"Report Awaited"},
                                {"Anchorage loading at Hazira":"Anchorage loading at Hazira"},
                            ],
                            "disabled": False
                        },
                        {
                            "label": "CON or TBN",
                            "decorator": "con_or_tbn",
                            "type": "textbox",
                            "required": False,
                            "message": "CON or TBN",
                            "id": "con_or_tbn",
                            "placeholder": "CON or TBN",
                            "disabled": False

                        },
                        {
                            "label": "Material N LP",
                            "decorator": "material_n_lp",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Material N LP",
                            "id": "material_n_lp",
                            "placeholder": "Material N LP",
                            "disabled": False

                        },
                        {
                            "label": "Vessel Cargo Arrival",
                            "decorator": "vessel_cargo_arrival",
                            "type": "textbox",
                            "required": False,
                            "message": "Enter Vessel Cargo Arrival",
                            "id": "vessel_cargo_arrival",
                            "placeholder": "Vessel Cargo Arrival",
                            "disabled": False

                        },
                        {
                            "label": "Major",
                            "decorator": "major",
                            "type": "textbox",
                            "required": False,
                            "message": "major",
                            "id": "major",
                            "placeholder": "major",
                            "disabled": False

                        },
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
                            "label": "Material",
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
                            "label": "Created Date",
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
                            "label": "Updated By",
                            "decorator": "last_updated_by",
                            "type": "textbox",
                            "required": "true",
                            "message": "Last Updated By !",
                            "id": "last_updated_by",
                            "placeholder": "This was last Updated By:",
                            "disabled": True
                        },
                        {
                            "label": "Last Updated",
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
        db_table = 'MST_BRM_TARGET_SHEET'
        # unique_together = (('p_date', 'sbu', 'plan_type', 'int_ext', 'region', 'division'),)


reversion.register(MstBRMTargetSheet)
