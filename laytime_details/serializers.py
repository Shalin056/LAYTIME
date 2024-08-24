# C:\Users\shali\Documents\shalin\test-app\laytime_details\serializers.py

"""
Serializers for Laytime Details app.
"""

from datetime import datetime
from rest_framework import serializers
from .models import ShippingDetail, ShippingStage, SplitQuantity, LayTimeCalculator

class ShippingStageSerializer(serializers.ModelSerializer):
    """
    Serializer for ShippingStage model.
    """
    start_date_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    end_date_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = ShippingStage
        fields = '__all__'

####################################################################################################

class SplitQuantitySerializer(serializers.ModelSerializer):
    """
    Serializer for SplitQuantity model.
    """
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'amount' in data:
            # Convert amount to string and split integer and decimal parts
            integer_part, decimal_part = str(data['amount']).split('.')

            # Insert commas every three digits in integer part
            integer_part_with_commas = '{:,}'.format(int(integer_part))

            # Join integer and decimal parts back with the decimal separator
            data['amount'] = f"{integer_part_with_commas}.{decimal_part}"

        return data
    class Meta:
        model = SplitQuantity
        fields = '__all__'

####################################################################################################

class LayTimeCalculatorSerializer(serializers.ModelSerializer):
    """
    Serializer for LayTimeCalculator model.
    """
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'amount' in data:
            integer_part, decimal_part = str(data['amount']).split('.')

            integer_part_with_commas = '{:,}'.format(int(integer_part))

            data['amount'] = f"{integer_part_with_commas}.{decimal_part}"
        return data
    class Meta:
        model = LayTimeCalculator
        fields = '__all__'

    def validate_shipping_detail(self, value):
        # Check if there is already a LayTimeCalculator with this ShippingDetail
        if LayTimeCalculator.objects.filter(shipping_detail=value).exists():
            raise serializers.ValidationError(
                "A LayTimeCalculator already exists for this ShippingDetail.")
        return value

####################################################################################################

class ShippingDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for ShippingDetail model.
    """
    stages = ShippingStageSerializer(many=True, read_only=True)
    split_quantities = SplitQuantitySerializer(many=True, read_only=True)
    laytime_calculator = LayTimeCalculatorSerializer(read_only=True)
    bl_date = serializers.DateField(format='%d-%m-%Y')
    # nor_tendered = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    # commenced_loading_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    # completed_loading_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')

    nor_tendered = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    commenced_loading_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    completed_loading_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        created_date = data.get('created_date')
        if created_date:
            data['created_date'] = datetime.strptime(created_date,
                                    '%Y-%m-%dT%H:%M:%S.%f').strftime('%d-%m-%Y %H:%M:%S')
        return data

    class Meta:
        model = ShippingDetail
        fields = '__all__'

####################################################################################################

class ShippingExcelSerializer(serializers.ModelSerializer):
    """
    Serializer for Excel export of ShippingDetail model.
    """
    bl_date = serializers.DateField(format='%d-%m-%Y')
    nor_tendered = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    commenced_loading_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    completed_loading_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')

    def to_representation(self, instance):

        data = super().to_representation(instance)
        print(data)

        stages = instance.stages.all()
        for index, stage in enumerate(stages):
            data.update({
                f'Stage_{index}_Stage': stage.stage_name,
                f'Stage_{index}_Start Date Time': stage.start_date_time.strftime('%d-%m-%Y %H:%M'),
                f'Stage_{index}_End Date Time': stage.end_date_time.strftime('%d-%m-%Y %H:%M'),
                f'Stage_{index}_Is included':stage.count,
                f'Stage_{index}_Percentage':stage.percentage
            })

        split_quantities = instance.split_quantities.all()
        for index, split_quantity in enumerate(split_quantities):
            data.update({
                f'Split_{index}_Port': split_quantity.port_name,
                f'Split_{index}_Cargo Quantity': split_quantity.cargo_quantity,
                f'Split_{index}_Amount': split_quantity.amount,
            })

        laytime_calculator = instance.laytime_calculator
        if laytime_calculator:
            data.update({
                'Amount': laytime_calculator.amount,
                'Actual Time': laytime_calculator.actual_time,
                'Allowed Time': laytime_calculator.allowed_time,
                'Total Time Difference': laytime_calculator.total_time_difference,
                'Is Time Saved': laytime_calculator.is_time_saved
            })

        # Remove unwanted fields
        unwanted_fields = ['is_approved', 'is_active', 'is_deleted', 'last_updated_by',
                            'last_updated_date']
        for field in unwanted_fields:
            data.pop(field, None)

        return data
    class Meta:
        model = ShippingDetail
        fields = "__all__"

####################################################################################################
