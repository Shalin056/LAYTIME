# C:\Users\shali\Documents\shalin\test-app\laytime_details\constants.py

"""
Constants for the Laytime Details app.
"""

WORKFLOW= {
    'REJECT' : 'Reject',
    'INIT': 'Init',
    'INITIATED': 'Initiated',
    'APP_NAME': 'laytime_details',
    'MODEL_NAME': 'shippingdetail',
}

SHIP_DETAIL_FIELDS = [
    'vessel',
    'bl_date',
    'load_port',
    'discharge_port',
    'cargo',
    'shipper_supplier',
    'receiver_buyer',
    'charter_type',
    'cargo_qty',
    'demurrage_rate_per_day',
    'loading_rate',
    'discharge_rate',
    'allowed_time',
    'turn_time_hours',
    'nor_tendered',
    'commenced_loading_time',
    'completed_loading_time',
    'rate_type',
    'remarks'
]

LAYTIME_CALCULATIONS_FIELDS = [
    'allowed_time', 
    'actual_time',
    'total_time_difference',
    'amount',
]

SHIP_DETAIL_FIELDS_TO_EXCLUDE = [
    'id', 'status', 'is_approved', 'is_active', 'is_deleted', 'created_by', 
    'created_date', 'last_updated_by', 'last_updated_date', 'rate_type'
]

STAGES_FIELDS_TO_EXCLUDE = [
    'id', 'status', 'is_approved', 'is_active', 'is_deleted', 'created_by',
    'created_date', 'last_updated_by', 'last_updated_date', 'shipping_detail'
]

SPLIT_QUANTITIES_FIELDS_TO_EXCLUDE = [
    'id', 'status', 'is_approved', 'is_active', 'is_deleted', 'created_by',
    'created_date', 'last_updated_by', 'last_updated_date', 'remaining_cargo_qty', 'shipping_detail'
]

LAYTIME_CALCULATIONS_FIELDS_TO_EXCLUDE = [
    "id", "status", "is_approved", "is_active", "is_deleted", "created_by",
    "created_date", "last_updated_by", "last_updated_date","is_time_saved", "shipping_detail"
]