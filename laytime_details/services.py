# C:\Users\shali\Documents\shalin\test-app\laytime_details\services.py

"""
Service layer for Laytime Details app.
"""
import traceback
import pandas as pd
import numpy as np

from io import BytesIO
from datetime import datetime
from dateutil import parser
from operator import itemgetter

from django.conf import settings
from django.db.models import Count, Q, IntegerField, CharField, DateField, FloatField, \
    DecimalField, DateTimeField, ManyToManyField
from django.http import JsonResponse, HttpResponse

from rest_framework import status
from rest_framework.response import Response

from workflow.models import WorkflowTransactions
from workflow.serializers import WorkflowTransactionSerializer
from workflow.services import to_show_approval_button, indicate_approval_type

from laytime_details.models import ShippingDetail, ShippingStage, SplitQuantity, LayTimeCalculator
from laytime_details.serializers import ShippingDetailSerializer, ShippingStageSerializer, \
    LayTimeCalculatorSerializer, SplitQuantitySerializer
from laytime_details.workflowtrigger import trigger_workflow
from laytime_details.constants import WORKFLOW, SHIP_DETAIL_FIELDS_TO_EXCLUDE, SHIP_DETAIL_FIELDS, \
    LAYTIME_CALCULATIONS_FIELDS, STAGES_FIELDS_TO_EXCLUDE, SPLIT_QUANTITIES_FIELDS_TO_EXCLUDE, \
    LAYTIME_CALCULATIONS_FIELDS_TO_EXCLUDE
from laytime_details.logger import USER_LOGS, REQUEST, EXCEL_LOGS

class LaytimeService:
    """
    Service class for processing laytime-related operations.
    """
    def process_shipping_detail(self, request, data):
        """
        Process ship detail data received from a form.

        :param self: The LaytimeService instance.
        :param request: HttpRequest object containing the HTTP request.
        :param data: Dictionary containing ship detail data.
        :return:dictionary containing ship detail, shipping stages, and split quantities if created.
        :rtype: dictionary
        """
        try:
            form_values_data = data['shipping_detail']
            REQUEST.debug('Form values data: %s', form_values_data)
            form_values_data['created_by'] = request.user.username

            REQUEST.info('Created by -- %s -- IP -- %s', form_values_data['created_by'],
                str(request.META.get('REMOTE_ADDR')))
            USER_LOGS.info('Created by -- %s -- IP -- %s', form_values_data['created_by'],
                str(request.META.get('REMOTE_ADDR')))

            stages_data = form_values_data.pop('stages', None)
            split_quantities_data = form_values_data.pop('split_quantities', None)
            remaining_cargo_qty = form_values_data.pop('remaining_cargo_qty', None)
            form_values_data['bl_date'] = parser.parse(form_values_data['bl_date']).date()

            numeric_fields = ['turn_time_hours', 'demurrage_rate_per_day',
                              'despatch_rate_per_day', 'cargo_qty',
                              'discharge_rate', 'allowed_time']
            for field in numeric_fields:
                form_values_data[field] = float(form_values_data[field])
                REQUEST.info('Field %s converted to float', field)

            existing_shipping_detail = ShippingDetail.objects.filter(**form_values_data).first()
            REQUEST.info('Existing ship detail fetched by user -- %s -- IP -- %s',
                          form_values_data['created_by'], str(request.META.get('REMOTE_ADDR')))

            if existing_shipping_detail:
                shipping_detail_serializer = ShippingDetailSerializer(existing_shipping_detail,
                                                                       data=form_values_data)
            else:
                shipping_detail_serializer = ShippingDetailSerializer(data=form_values_data)

            if shipping_detail_serializer.is_valid():
                REQUEST.info('Ship detail serializer is valid')
                shipping_detail = shipping_detail_serializer.save()

                shipping_stages = self.process_shipping_stages(stages_data,
                                                                          shipping_detail)

                laytime_calculations = self.calculate_laytime( data, stages_data,
                                                               shipping_detail.id)
                REQUEST.info('Laytime calculated for %s', shipping_detail.id)

                if split_quantities_data:
                    split_quantities = self.process_split_quantities(
                                        split_quantities_data, shipping_detail,
                                        laytime_calculations)
                    REQUEST.info('Split quantities created for %s', shipping_detail.id)

                # if existing_shipping_detail:
                #     return shipping_detail, \
                #         shipping_stages, laytime_calculations, split_quantities if split_quantities_data else None
                # return shipping_detail, \
                #         shipping_stages, laytime_calculations, split_quantities if split_quantities_data else None
                response_data = {
                    'shipping_detail': ShippingDetailSerializer(shipping_detail).data,
                    'shipping_stages': ShippingStageSerializer(shipping_stages, many=True).data,
                    'laytime_calculations': laytime_calculations,
                    'split_quantities': SplitQuantitySerializer(split_quantities, many=True).data if split_quantities_data else None
                }

                return response_data
            REQUEST.error('Ship detail serializer has errors: %s',shipping_detail_serializer.errors)
        except Exception as e:
            REQUEST.error("Error processing ship detail: %s", e)
            traceback.print_exc()
        return shipping_detail, \
                        shipping_stages, laytime_calculations, split_quantities if split_quantities_data else None

####################################################################################################

    def service_trigger_workflow(self, request, shipping_detail):
        """
        Triggers the workflow for a ship detail object.

        :param self: The LaytimeService instance.
        :param request: HttpRequest object containing the HTTP request.
        :param shipping_detail: The ship detail object for which the workflow is triggered.
        """
        try:
            trigger_workflow(request, shipping_detail, WORKFLOW.get('INITIATED'),
                            WORKFLOW.get('APP_NAME'), WORKFLOW.get('MODEL_NAME'),
                            WORKFLOW.get('INIT'))
        except Exception as e:
            print(f"Error triggering workflow: {str(e)}")
            # traceback.print_exc()

####################################################################################################

    def process_shipping_stages(self, stage_details_data, shipping_detail):
        """
        Processes and creates shipping stages based on the provided stage details data.

        :param self: The LaytimeService instance.
        :param stage_details_data: List of dictionaries containing stage details data.
        :param shipping_detail: The ship detail object for which stages are processed.

        :return: List of created ShippingStage objects.
        """
        try:
            shipping_stages = []
            for detail in stage_details_data:
                if (
                    detail and
                    detail.get('stage_name') and
                    detail.get('end_date_time') and
                    detail.get('start_date_time') and
                    detail.get('percentage')
                ):
                    existing_stage = ShippingStage.objects.filter(
                        # count=detail['count'],
                        stage_name=detail['stage_name'],
                        start_date_time=parser.parse(detail['start_date_time']),
                        end_date_time=parser.parse(detail['end_date_time']),
                        percentage = detail['percentage'],
                        shipping_detail=shipping_detail.id
                    ).first()

                    if existing_stage:
                        REQUEST.debug(
                            "Shipping stage already exists for ship detail %s. Skipping creation.",
                            shipping_detail.id)
                        REQUEST.debug("Stage '%s' already exists", existing_stage.stage_name)
                    else:
                        stage_data = {
                            'count': detail['count'] if 'count' in detail else False,
                            'stage_name': detail['stage_name'],
                            'start_date_time': parser.parse(detail['start_date_time']),
                            'end_date_time': parser.parse(detail['end_date_time']),
                            'percentage': detail['percentage'],
                            'shipping_detail': shipping_detail.id,
                        }
                        serializer = ShippingStageSerializer(data=stage_data)

                        if serializer.is_valid():
                            shipping_stage = serializer.save()
                            shipping_stages.append(shipping_stage)
                            REQUEST.info("Added shipping stage '%s' for ship detail %s",
                                shipping_stage.stage_name, shipping_detail.id)
                            REQUEST.debug("Stage data for ship detail %s: %s",
                                shipping_detail.id, stage_data)
                        else:
                            REQUEST.error("Invalid data for shipping stage: %s", serializer.errors)
            return shipping_stages
        except Exception as e:
            REQUEST.error("Error processing shipping stage: %s", e)
            traceback.print_exc()
            return []

####################################################################################################

    def process_split_quantities(self, split_details_data, shipping_detail, laytime_calculations):
        """
        Processes and creates split quantities based on the provided split details data.

        :param self: The LaytimeService instance.
        :param split_details_data: List of dictionaries containing split details data.
        :param shipping_detail: The ship detail object for which split quantities are processed.

        :return: List of created SplitQuantity objects.
        """
        try:
            split_quantities = []
            for split_detail in split_details_data:
                if (
                    split_detail and
                    split_detail.get('port_name') and
                    split_detail.get('cargo_quantity') and
                    split_detail.get('amount')
                ):
                    remaining_cargo_qty = split_detail.get('remaining_cargo_qty', None)

                    existing_quantity = SplitQuantity.objects.filter(
                        port_name=split_detail['port_name'],
                        cargo_quantity=split_detail['cargo_quantity'],
                        amount=split_detail['amount'],
                        remaining_cargo_qty=remaining_cargo_qty,
                        shipping_detail=shipping_detail.id
                    ).first()

                    if existing_quantity:
                        REQUEST.debug(
                            "Split quantity already exists for ship detail %s. Skipping creation.",
                            shipping_detail.id)
                    else:
                        print('\n\neach_cargo_quantity: ', split_detail['cargo_quantity'])
                        print('\n\ntotal_cargo_quantity: ', shipping_detail.cargo_qty)
                        print('\n\ntotal_amount: ', laytime_calculations[0]['amount'])
                        total_amount_str = laytime_calculations[0]['amount']
                        # Remove the comma
                        total_amount_str = total_amount_str.replace(',', '')
                        # Convert to float
                        total_amount_float = float(total_amount_str)
                        each_amount = (split_detail['cargo_quantity'] / shipping_detail.cargo_qty
                                       )*total_amount_float
                        split_data = {
                            'port_name': split_detail['port_name'],
                            'cargo_quantity': split_detail['cargo_quantity'],
                            'amount': each_amount,
                            'remaining_cargo_qty': remaining_cargo_qty,
                            'shipping_detail': shipping_detail.id,
                        }
                        serializer = SplitQuantitySerializer(data=split_data)

                        if serializer.is_valid():
                            split_quantity = serializer.save()
                            split_quantities.append(split_quantity)
                            REQUEST.info("Added split quantity for port '%s' and ship detail %s",
                                split_quantity.port_name, shipping_detail.id)
                            REQUEST.debug("Split quantity data for ship detail %s: %s",
                                shipping_detail.id, split_data)
                        else:
                            REQUEST.error("Invalid data for split quantity: %s", serializer.errors)
            return split_quantities
        except Exception as e:
            REQUEST.error("Error processing split quantities: %s", e)
            traceback.print_exc()
            return None

####################################################################################################

    def validate_stage_dates(self, stage_details, commenced_loading_time, completed_loading_time):
        commenced_loading_time = commenced_loading_time
        completed_loading_time = completed_loading_time
        
        for index, each_stage in enumerate(stage_details):
            start_date_time = each_stage['start_date_time']
            end_date_time = each_stage['end_date_time']
            
            if start_date_time >= end_date_time:
                raise ValueError(f"Start date time must be smaller than end date time for stage {index + 1}.")
            
            if start_date_time < commenced_loading_time or start_date_time > completed_loading_time:
                raise ValueError(f"Start date time for stage {index + 1} must be within the range of commenced and completed loading time.")
            
            if end_date_time < commenced_loading_time or end_date_time > completed_loading_time:
                raise ValueError(f"End date time for stage {index + 1} must be within the range of commenced and completed loading time.")

        return True
    
    def calculate_time_details(self, stage_details, allowed_time, demurrage_rate_per_day,
                               despatch_rate_per_day):
        """
        Calculate time details based on stage details and allowed time.

        :param self: The LaytimeService instance.
        :param stage_details: List of dictionaries containing stage details.
        :param allowed_time: Allowed time in days.
        :param demurrage_rate_per_day: Demurrage rate per day.
        :param despatch_rate_per_day: Despatch rate per day.
        :param percentage: Percentage factor for calculations.

        :return: dictionary containing total minutes, amount, actual time,
                 total time difference, and time saved flag.
        """
        total_minute = 0
        amount = 0
        actual_time = 0
        total_time_difference = 0
        is_time_saved = False

        for each_stage in stage_details:
            if (
                each_stage and
                each_stage.get('count') and
                each_stage.get('end_date_time') and
                each_stage.get('start_date_time')
            ):
                # Convert string representations to datetime objects
                start_datetime = parser.parse(each_stage['start_date_time'])
                end_datetime = parser.parse(each_stage['end_date_time'])

                if start_datetime >= end_datetime:
                    raise ValueError("Start date time must be smaller than end date time.")

                start_datetime = start_datetime.replace(second=0, microsecond = 0)
                end_datetime = end_datetime.replace(second=0, microsecond = 0)
                difference_in_minutes = int(
                    (end_datetime - start_datetime).total_seconds() / 60
                    ) * (each_stage['percentage']/100)
                total_minute += difference_in_minutes

        REQUEST.debug("Total minutes calculated: %s", total_minute)

        if allowed_time and demurrage_rate_per_day and despatch_rate_per_day:
            actual_time = round(total_minute / (24 * 60), 5)
            REQUEST.debug("Actual time calculated: %s", actual_time)
            total_time_difference = round(abs(allowed_time - actual_time), 5)
            REQUEST.debug("Total time difference calculated: %s", total_time_difference)

            if allowed_time < actual_time:
                is_time_saved = False
                amount = round(total_time_difference * demurrage_rate_per_day, 5)
                REQUEST.info("Demurrage amount calculated: %s", amount)
            else:
                is_time_saved = True
                amount = round(total_time_difference * despatch_rate_per_day, 5)
                REQUEST.info("Despatch amount calculated: %s", amount)

        REQUEST.debug("Actual time: %s, Total time difference: %s, Is time saved: %s",
                      actual_time, total_time_difference, is_time_saved)

        return total_minute, amount, actual_time, total_time_difference, is_time_saved

    def calculate_laytime(self, data, stage_details_data, shipping_id, update_laytime=False):
        """
        Calculate laytime based on input data and stage details.

        :param self: The LaytimeService instance.
        :param data: Input data containing percentage, allowed time,
                     demurrage rate, and despatch rate.
        :param stage_details_data: Stage details data.
        :param shipping_id: ID of the ship detail.

        :return: List of calculated LayTimeCalculator instances or error message with status code.
        """
        try:
            calculated_data=[]
            
            percentage = data.get("percentage", 100) / 100
            REQUEST.debug("Percentage for calculation for: %s", percentage)
            # Extract required data from the input
            allowed_time = float(data['shipping_detail']['allowed_time'])
            demurrage_rate_per_day = float(data['shipping_detail']['demurrage_rate_per_day'])
            despatch_rate_per_day = float(data['shipping_detail']['despatch_rate_per_day'])
            
            commenced_loading_time = data['shipping_detail']['commenced_loading_time']
            completed_loading_time = data['shipping_detail']['completed_loading_time']

            # Validate stage dates
            try:
                self.validate_stage_dates(stage_details_data, commenced_loading_time, completed_loading_time)
            except Exception as ve:
                REQUEST.error("Stage dates validation failed: %s", ve)
                return {'message': 'Stage dates validation failed', 'error': str(ve)}, 400
            
            # Call the calculate_time_details function
            total_minute, amount, actual_time, total_time_difference, is_time_saved = (
                LaytimeService().calculate_time_details(
                stage_details_data,
                allowed_time,
                demurrage_rate_per_day,
                despatch_rate_per_day
            ))

            shipping_detail_instance = ShippingDetail.objects.get(id=shipping_id)

            shipping_detail_instance_id = shipping_detail_instance.id

            # Create or update LayTimeCalculator instance
            laytime_calculator_data = {
                'shipping_detail': shipping_detail_instance_id,
                'amount': round(amount, 2),
                'actual_time': actual_time,
                'allowed_time': allowed_time,
                'total_time_difference': total_time_difference,
                'is_time_saved': is_time_saved,
            }

            if update_laytime:
                return laytime_calculator_data

            laytime_calculator_serializer = (
                LayTimeCalculatorSerializer(data=laytime_calculator_data))
            if laytime_calculator_serializer.is_valid():
                laytime_calculator = laytime_calculator_serializer.save()
                calculated_data.append(laytime_calculator_serializer.data)
                REQUEST.info("Laytime calculation successful for %s", shipping_id)
                shipping_detail_instance.save()
            else:
                REQUEST.error("Error validating laytime calculator serializer: %s",
                               laytime_calculator_serializer.errors)
                return {'message': 'Error validating laytime calculator serializer',
                                 'errors': laytime_calculator_serializer.errors}, 400
                                 

            return calculated_data

        except Exception as e:
            REQUEST.error("Error calculating laytime: %s", e)
            return {'message': 'Error calculating laytime', 'error': str(e)}, 500

    @classmethod
    def calculate_allowed_time(cls, data):
        """
        Calculate the allowed time based on cargo quantity and discharge rate.

        :param data: Dictionary containing cargo quantity and discharge rate.

        :return: Dictionary with success status and calculated allowed time if successful,
                 otherwise, a dictionary with success status and an error message.
        """
        try:
            cargo_qty = float(data.get("cargoQty", 0))
            discharge_rate = float(data.get("dischRate", 0))

            # Perform the calculation to get allowed time
            allowed_time = (cargo_qty / discharge_rate) if discharge_rate != 0 else 0

            REQUEST.info("Allowed time calculated successfully: cargoQty=%s, "
                         "dischRate=%s, allowed_time=%s",cargo_qty, discharge_rate, allowed_time)
            USER_LOGS.info("Allowed time calculated successfully: cargoQty=%s, "
                            "dischRate=%s, allowed_time=%s",cargo_qty, discharge_rate, allowed_time)

            return {'success': True, 'data': {'allowed_time': allowed_time}}

        except Exception as e:
            REQUEST.error("Error calculating allowed time: %s", e)
            return {'success': False, 'message': 'Error calculating allowed time.'}

####################################################################################################

####################################################################################################

class DetailViewService:
    """
    Service class for handling model instances, filtering querysets, pagination,
    and data serialization.
    """
    def get_queryset(self, model_class):
        """
        Get the queryset for a given model class,
        filtering based on 'is_deleted' attribute if available.

        :param model_class: The model class to retrieve the queryset for.
        :return: Queryset filtered based on 'is_deleted' attribute if available,
                 otherwise, all objects queryset.
        """
        if hasattr(model_class, 'is_deleted'):
            return model_class.objects.filter(is_deleted=False)
        return model_class.objects.all()

    def get_model_class(self, model_name):
        """
        Get the model class based on the provided model name.

        :param model_name: The name of the model.
        :return: The corresponding model class.
        """
        model_classes = {
            'shipping_detail': ShippingDetail,
            'shipping_stage': ShippingStage,
            'split_quantity': SplitQuantity,
            'laytime_calculator': LayTimeCalculator,
            'workflow_transactions': WorkflowTransactions,
        }
        return model_classes.get(model_name)

    def get_serializer(self, model_class):
        """
        Get the serializer class based on the provided model class.

        :param model_class: The model class.
        :return: The corresponding serializer class.
        """
        serializers = {
            ShippingDetail: ShippingDetailSerializer,
            ShippingStage: ShippingStageSerializer,
            SplitQuantity: SplitQuantitySerializer,
            LayTimeCalculator: LayTimeCalculatorSerializer,
            WorkflowTransactions: WorkflowTransactionSerializer,
        }
        return serializers.get(model_class)

    # @classmethod
    def retrieve_model_instance(self, pk, model_name):
        """
        Retrieve a model instance by primary key and model name.

        :param pk: The primary key of the instance.
        :param model_name: The name of the model.
        :return: The retrieved model instance if found, otherwise None.
        """
        model_class = DetailViewService.get_model_class(self, model_name)
        instance = DetailViewService.get_queryset(self, model_class).filter(
            pk=pk, is_deleted=False).first()
        if instance:
            return instance
        REQUEST.warning("Model instance not found for pk: %s, model: %s",
                         pk, model_name)
        USER_LOGS.warning("Model instance not found for pk: %s, model: %s",
                           pk, model_name)
        return None
        # return cls.get_queryset(model_class).filter(pk=pk, is_deleted=False).first()

    def retrieve_all_serialized_instances(self, model_name):
        """
        Retrieve all instances of a model and serialize them.

        :param model_name: The name of the model.
        :return: Serialized data for all instances of the model.
        """
        model_class = DetailViewService.get_model_class(self, model_name)
        queryset = DetailViewService.get_queryset(self, model_class)
        serializer = DetailViewService.get_serializer(self, model_class)

        serialized_data = [serializer(instance).data for instance in queryset]
        return serialized_data

    def retrieve_serialized_instance(self, pk, model_name):
        """
        Retrieve and serialize a specific instance of a model.

        :param pk: The primary key of the instance.
        :param model_name: The name of the model.
        :return: Serialized data for the instance if found, otherwise None.
        """
        model_class = DetailViewService.get_model_class(self, model_name)
        if hasattr(model_class, 'is_deleted'):
            instance = DetailViewService.get_queryset(self, model_class).filter(
                pk=pk, is_deleted=False).first()
        else:
            instance = DetailViewService.get_queryset(self, model_class).filter(
                pk=pk).first()

        if instance:
            serializer = DetailViewService.get_serializer(self, instance.__class__)(instance)
            return serializer.data
        REQUEST.warning("Model instance not found for pk: %s, model: %s",
                         pk, model_name)
        USER_LOGS.warning("Model instance not found for pk: %s, model: %s",
                           pk, model_name)
        return None

####################################################################################################

    # @classmethod
    def update_model_instance(self, pk, model_name, data):
        """
        Update a model instance with the provided data.

        :param pk: The primary key of the instance to update.
        :param model_name: The name of the model to update.
        :param data: The data to update the instance with.
        :return: Serialized data of the updated instance if successful,
          otherwise serializer errors or None.
        """
        try:
            update_data = data
            print('\n\n\n---------data--------', data['shipping_detail'])
            print('\n\n\n')

            model_class = DetailViewService.get_model_class(self, model_name)
            serializer_class = DetailViewService.get_serializer(self, model_class)
            instance = DetailViewService.retrieve_model_instance(self, pk, model_name)

            if instance:
                extracted_data = update_data.get('shipping_detail', {})
                extracted_stages = extracted_data.get('stages', [])
                extracted_split_quantities = extracted_data.get('split_quantities', [])

                commenced_loading_time = extracted_data['commenced_loading_time']
                completed_loading_time = extracted_data['completed_loading_time']

                try:
                    LaytimeService().validate_stage_dates(extracted_stages, commenced_loading_time, completed_loading_time)
                except Exception as ve:
                    REQUEST.error("Stage dates validation failed: %s", ve)
                    USER_LOGS.error("Stage dates validation failed: %s", ve)
                    return {"error": str(ve)}
                
                serializer = serializer_class(instance, data=extracted_data, partial=True)

                if serializer.is_valid():
                    updated_obj = serializer.save()

                    # Update nested fields
                    if extracted_stages:
                        instance.stages.all().delete()
                        for stage_data in extracted_stages:
                            stage_data.update({'shipping_detail': updated_obj})
                            instance.stages.create(**stage_data)

                    # update laytime calculations
                    laytime_data = LaytimeService().calculate_laytime(
                        update_data, extracted_stages, updated_obj.id, True)
                    laytime_data.pop('shipping_detail')
                    laytime_calculator_serializer = LayTimeCalculatorSerializer(
                        updated_obj.laytime_calculator, data=laytime_data, partial=True)
                    if laytime_calculator_serializer.is_valid():
                        laytime_calculator_serializer.save()

                    if extracted_split_quantities:
                        instance.split_quantities.all().delete()
                        for split_quantities in extracted_split_quantities:
                            print('\n\nupdated_obj: ', updated_obj.cargo_qty)
                            split_quantities['amount'] = (
                                split_quantities['cargo_quantity'] / updated_obj.cargo_qty
                                                          )*laytime_data['amount']
                            split_quantities.update({'shipping_detail': updated_obj})
                            instance.split_quantities.create(**split_quantities)
                    else:
                        instance.split_quantities.all().delete()

                    REQUEST.info("Shipping ID %s updated successfully by %s",
                                  updated_obj.id, updated_obj.created_by)
                    USER_LOGS.info("Shipping ID %s updated successfully", updated_obj.id)

                    return serializer.data
                REQUEST.error("Serializer errors: %s",serializer.errors)
                USER_LOGS.error("Serializer errors: %s",serializer.errors)
                return serializer.errors
            REQUEST.warning("Model instance not found for pk: %s, model: %s",
                            pk, model_name)
            USER_LOGS.warning("Model instance not found for pk: %s, model: %s",
                            pk, model_name)
            return None

        except Exception as e:
            REQUEST.error("Error updating model instance: %s",e)
            USER_LOGS.error("Error updating model instance: %s",e)
            traceback.print_exc()
            return None
        
    # @classmethod
    def update_pdf_model_instance(self, pk, model_name, data):
        """
        Update a model instance with the provided data.

        :param pk: The primary key of the instance to update.
        :param model_name: The name of the model to update.
        :param data: The data to update the instance with.
        :return: Serialized data of the updated instance if successful,
          otherwise serializer errors or None.
        """
        try:
            # id = pk  # Assuming the update data is provided in the request body
            # shipping_detail = ShippingDetail.objects.filter(id=id).values()[0]
            # if shipping_detail:
            #     shipping_detail.pop('id', None)
            # stages = list(ShippingStage.objects.filter(shipping_detail_id=id).values())
            # split_quantities = list(SplitQuantity.objects.filter(shipping_detail_id=id).values())
            # update_data = {
            #     'shipping_detail': shipping_detail,
            #     'stages': stages,
            #     'split_quantities': split_quantities
            # }
            # print('\n\n\n---------data--------', data['shipping_detail'])
            # print('\n\n\n')
            update_data = data
            model_class = DetailViewService.get_model_class(self, model_name)
            serializer_class = DetailViewService.get_serializer(self, model_class)
            instance = DetailViewService.retrieve_model_instance(self, pk, model_name)

            if instance:
                extracted_data = update_data.get('shipping_detail', {})
                extracted_stages = extracted_data.get('stages', [])
                extracted_split_quantities = extracted_data.get('split_quantities', [])

                commenced_loading_time = extracted_data['commenced_loading_time']
                completed_loading_time = extracted_data['completed_loading_time']

                try:
                    LaytimeService().validate_stage_dates(extracted_stages, commenced_loading_time, completed_loading_time)
                except Exception as ve:
                    REQUEST.error("Stage dates validation failed: %s", ve)
                    USER_LOGS.error("Stage dates validation failed: %s", ve)
                    return {"error": str(ve)}
                
                serializer = serializer_class(instance, data=extracted_data, partial=True)

                if serializer.is_valid():
                    updated_obj = serializer.save()

                    # Update nested fields
                    if extracted_stages:
                        instance.stages.all().delete()
                        for stage_data in extracted_stages:
                            stage_data.update({'shipping_detail': updated_obj})
                            instance.stages.create(**stage_data)

                    # update laytime calculations
                    laytime_data = LaytimeService().calculate_laytime(
                        update_data, extracted_stages, updated_obj.id, True)
                    laytime_data.pop('shipping_detail')
                    laytime_calculator_serializer = LayTimeCalculatorSerializer(
                        updated_obj.laytime_calculator, data=laytime_data, partial=True)
                    if laytime_calculator_serializer.is_valid():
                        laytime_calculator_serializer.save()

                    if extracted_split_quantities:
                        instance.split_quantities.all().delete()
                        for split_quantities in extracted_split_quantities:
                            print('\n\nupdated_obj: ', updated_obj.cargo_qty)
                            split_quantities['amount'] = (
                                split_quantities['cargo_quantity'] / updated_obj.cargo_qty
                                                          )*laytime_data['amount']
                            split_quantities.update({'shipping_detail': updated_obj})
                            instance.split_quantities.create(**split_quantities)
                    else:
                        instance.split_quantities.all().delete()

                    REQUEST.info("Shipping ID %s updated successfully by %s",
                                  updated_obj.id, updated_obj.created_by)
                    USER_LOGS.info("Shipping ID %s updated successfully", updated_obj.id)

                    return serializer.data
                REQUEST.error("Serializer errors: %s",serializer.errors)
                USER_LOGS.error("Serializer errors: %s",serializer.errors)
                return serializer.errors
            REQUEST.warning("Model instance not found for pk: %s, model: %s",
                            pk, model_name)
            USER_LOGS.warning("Model instance not found for pk: %s, model: %s",
                            pk, model_name)
            return None

        except Exception as e:
            REQUEST.error("Error updating model instance: %s",e)
            USER_LOGS.error("Error updating model instance: %s",e)
            traceback.print_exc()
            return None
####################################################################################################

    # @classmethod
    def delete_model_instance(self, pk, model_name):
        """
        Soft delete a model instance by setting 'is_deleted' attribute to True.

        :param pk: The primary key of the instance to delete.
        :param model_name: The name of the model to delete.
        :return: True if the instance is successfully deleted, False otherwise.
        """
        try:
            model_instance = DetailViewService.retrieve_model_instance(self, pk, model_name)
            if model_instance:
                model_instance.is_deleted = True
                model_instance.save()
                REQUEST.info("Model instance deleted successfully")
                USER_LOGS.info("Model instance deleted successfully")
                return True
            REQUEST.warning("Model instance not found for pk: %s, model: %s",
                            pk, model_name)
            USER_LOGS.warning("Model instance not found for pk: %s, model: %s",
                            pk, model_name)
            return False
        except Exception as e:
            REQUEST.error("Error deleting model instance: %s",e)
            USER_LOGS.error("Error deleting model instance: %s",e)
            return False

####################################################################################################

    def delete_multiple_model_instances(self, pk_list, model_name):
        """
        Soft delete multiple model instances in a list by setting 'is_deleted' attribute to True.

        :param pk_list: List of primary keys of instances to delete.
        :param model_name: The name of the model to delete instances from.
        :return: True if all instances are successfully deleted, False otherwise.
        """
        try:
            model_class = DetailViewService.get_model_class(self, model_name)

            # Soft delete for each instance in the list
            for pk in pk_list:
                instance = model_class.objects.filter(pk=pk).first()
                if instance:
                    instance.is_deleted = True
                    instance.save()
            REQUEST.info("Multiple model instances deleted successfully")
            USER_LOGS.info("Multiple model instances deleted successfully")
            return True
        except Exception as e:
            REQUEST.error("Error deleting multiple model instances: %s",e)
            USER_LOGS.error("Error deleting multiple model instances: %s",e)
            return False

####################################################################################################

    def get_model_fields(self, model):
        """
        Retrieve all fields of a model including related fields.

        :param model: The model class to retrieve fields from.
        :return: List of field names.
        """
        model_fields = []
        REQUEST.debug("Initializing model fields retrieval for %s", model.__name__)

        for field in model._meta.get_fields():
            REQUEST.debug("Field found: %s", field.name)

            if isinstance(field, (
                IntegerField,
                CharField,
                DateField,
                FloatField,
                DecimalField,
                DateTimeField)
                ):
                model_fields.append(field.name)
                REQUEST.debug("Added field '%s' to model fields list", field.name)

            elif isinstance(field, ManyToManyField):
                model_fields.append(field.name)
                REQUEST.debug("Added field '%s' to model fields list", field.name)
                related_model = field.related_model
                model_fields.extend([
                    f"{field.name}__{related_field.name}" 
                    for related_field in related_model._meta.get_fields()])

        REQUEST.info("Model fields retrieval completed for %s", model.__name__)
        return model_fields

####################################################################################################

    def filter_queryset(self, model_obj, search_query):
        """
        Filter queryset based on search query across model fields.

        :param model_obj: The model object to filter.
        :param search_query: The search query string.
        :return: Filtered queryset.
        """
        model_fields = DetailViewService.get_model_fields(self, model_obj)
        or_conditions = Q()

        for field in model_fields:
            lookup = f"{field}"
            if "__" in lookup:
                related_model_name = lookup.split("__")[0]
                related_field_name = lookup.split("__")[1]

                try:
                    related_model = model_obj._meta.get_field(related_model_name).related_model
                    related_field = related_model._meta.get_field(related_field_name)
                except Exception as e:
                    REQUEST.error('Error accessing related model or field: %s', str(e))
                    raise Exception(f'Error accessing related model or field: {str(e)}') from e

                if isinstance(
                    related_field, (CharField, DateField, FloatField, DecimalField, DateTimeField)
                ) and not related_field.is_relation and not related_field.auto_created:
                    lookup += "__icontains"
                    REQUEST.debug("Modified lookup for related field '%s__%s'",
                                   related_model_name, related_field_name)
                else:
                    continue
            else:
                try:
                    fields = model_obj._meta.get_field(field)
                    if isinstance(fields, (IntegerField, CharField, DateField,
                                            FloatField, DecimalField, DateTimeField)):
                        lookup += "__icontains"
                        REQUEST.debug("Modified lookup for field '%s'", field)
                    else:
                        continue
                except Exception as e:
                    REQUEST.error('Error accessing field: %s', str(e))
                    raise Exception(f'Error accessing field: {str(e)}') from e

            or_conditions |= Q(**{lookup: search_query})

        queryset = model_obj.objects.filter(is_deleted=False).distinct('id')
        filtered_queryset = queryset.filter(or_conditions)
        REQUEST.info("Queryset filtering completed for model %s", model_obj.__name__)
        return filtered_queryset

####################################################################################################

    def paginate_results(self, filtered_queryset, page, pagesize):
        """
        Paginate queryset results.

        :param filtered_queryset: The filtered queryset to paginate.
        :param page: The page number.
        :param pagesize: The number of items per page.
        :return: Total count of items and paginated queryset.
        """
        REQUEST.debug("Paginating results")
        total_count = filtered_queryset.count()
        REQUEST.info("Total count calculated: %s",total_count)

        start_index = (page - 1) * pagesize
        end_index = start_index + pagesize

        paginated_queryset = filtered_queryset[start_index:end_index]
        REQUEST.info("Pagination completed")
        return total_count, paginated_queryset

####################################################################################################

    def serialize_data(self, model_obj, queryset):
        """
        Serialize queryset data.

        :param model_obj: The model object.
        :param queryset: The queryset to serialize.
        :return: Serialized data.
        """
        serializer = DetailViewService.get_serializer(self, model_obj)(queryset, many=True)
        REQUEST.info("Data serialized successfully")
        return serializer.data

####################################################################################################

    def handle_search_data(self, model, search_query, page=None, pagesize=None):
        """
        Handle search query data for a model.

        :param model: The model name.
        :param search_query: The search query string.
        :param page: The page number for pagination (optional).
        :param pagesize: The number of items per page for pagination (optional).
        :return: Response with serialized data or error message.
        """
        try:
            model_obj = DetailViewService.get_model_class(self, model)
        except Exception as e:
            REQUEST.error('Error getting model class: %s', str(e))
            return Response({'error': f'Error getting model class: {str(e)}'},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            filtered_queryset = DetailViewService.filter_queryset(self, model_obj, search_query)
            REQUEST.info("Filtered queryset obtained")
        except Exception as e:
            REQUEST.error('Error filtering queryset: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if page is not None and pagesize is not None:
            try:
                total_count, paginated_queryset = DetailViewService.paginate_results(self,
                    filtered_queryset, page, pagesize)
                serialized_data = DetailViewService.serialize_data(self, model_obj,
                                                                    paginated_queryset)
                response = {"total": total_count, "results": serialized_data}
                REQUEST.info("Pagination and serialization completed")
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                REQUEST.error('Error paginating results: %s', str(e))
                return Response({'error': f'Error paginating results: {str(e)}'},
                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            serialized_data = DetailViewService.serialize_data(self, model_obj, filtered_queryset)
            REQUEST.info("Serialization completed for full queryset")
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            REQUEST.error('Error serializing queryset: %s', str(e))
            return Response({'error': f'Error serializing queryset: {str(e)}'},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

####################################################################################################

class ExcelExportService:
    """
    Service class for exporting data to an Excel file.

    Example Data Structure for 'data' parameter:
        data = {
            'results': [
                {'id': 1, 'stages': [...], 'split_quantities': [...], 'laytime_calculator': {...}},
                {'id': 2, 'stages': [...], 'split_quantities': [...], 'laytime_calculator': {...}},
                ...
            ],
            'columns': ['id', 'column1', 'column2', ...],
        }
    """
    def export_excel_data(self, data):
        """
        Export data to an Excel file.

        :param data: Data to be exported in Excel format. 
                     Should contain 'results' and 'columns' keys.
                     'results' should be a list of dictionaries representing rows of data.
                     'columns' should be a list of column names.
        :return: HttpResponse containing the Excel file as an attachment.
        """
        try:
            results = data.get('results', [])
            print('\nresults: ',results)
            columns = data.get('columns', [])

            # Create a DataFrame from the data
            df = pd.DataFrame(results)
            EXCEL_LOGS.info('DataFrame created from data: %s',df)

            # Extracting 'stages', 'split_quantities', and 'laytime_calculator' from 'results'
            stages_data = [[
                            {
                             key: value for key, value in stage.items()
                             if key not in ['count', 'is_deleted', 'shipping_detail']
                            } for stage in result.get('stages', [])
                           ] for result in results
                          ]

            split_quantities_data = [[
                                      {
                                        key: value for key, value in split.items()
                                        if key not in ['remaining_cargo_qty',
                                                       'shipping_detail',
                                                       'is_deleted']
                                      } for split in result.get('split_quantities', [])
                                     ] for result in results
                                    ]

            laytime_calculator_data = [{
                                        key: value
                                        for key,value in result.get('laytime_calculator',{}).items()
                                        if key not in ['is_time_saved',
                                                       'shipping_detail',
                                                       'is_deleted']
                                       } for result in results
                                       if isinstance(result.get('laytime_calculator', {}), dict)
                                      ]

            # Creating DataFrames for 'stages', 'split_quantities', and 'laytime_calculator'
            max_stage_count = max(len(stage) for stage in stages_data)
            stage_dfs = []
            for stages in stages_data:
                stage_dict = {}
                for i in range(max_stage_count):
                    prefix = f"Stage{i}_"
                    if i < len(stages):
                        stage = stages[i]
                        for key, value in stage.items():
                            # Convert boolean values to proper representation
                            if isinstance(value, bool):
                                value = str(value).capitalize()  # Convert to string representation
                            stage_dict[prefix + key] = value
                    else:
                        for key in stages[0].keys():
                            stage_dict[prefix + key] = np.nan
                stage_dfs.append(pd.DataFrame([stage_dict]))

            new_df1 = pd.concat(stage_dfs, ignore_index=True)
            EXCEL_LOGS.info('DataFrame created for stages: %s',new_df1)

            max_split_count = max(len(split) for split in split_quantities_data)
            split_dfs = []
            for splits in split_quantities_data:
                split_dict = {}
                if splits:  # Check if splits is not empty
                    for i in range(max_split_count):
                        prefix = f"Split{i}_"
                        if i < len(splits):
                            split = splits[i]
                            for key, value in split.items():
                                # Convert boolean values to proper representation
                                if isinstance(value, bool):
                                    # Convert to string representation
                                    value = str(value).capitalize()
                                split_dict[prefix + key] = value
                        else:
                            for key in splits[0].keys():
                                split_dict[prefix + key] = np.nan
                split_dfs.append(pd.DataFrame([split_dict]))

            new_df2 = pd.concat(split_dfs, ignore_index=True)
            EXCEL_LOGS.info('DataFrame created for split quantities: %s',new_df2)

            new_df3 = pd.concat([pd.DataFrame(laytime, index=[0])
                                 for laytime in laytime_calculator_data], ignore_index=True)
            EXCEL_LOGS.info('DataFrame created for laytime calculator: %s',new_df3)

            # Concatenate the DataFrames horizontally
            df_concatenated = pd.concat([df, new_df1, new_df2, new_df3], axis=1)

            # Drop unnecessary columns
            df_concatenated.drop(['stages', 'split_quantities',
                                   'laytime_calculator', 'is_deleted'], axis=1, inplace=True)

            # Create a BytesIO buffer to store the Excel file
            excel_buffer = BytesIO()

            # Save the DataFrame to an Excel file
            df_concatenated.to_excel(excel_buffer, index=False)

            excel_buffer.seek(0)

            # Save the Excel buffer to HttpResponse
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=data_export.xlsx'
            response.write(excel_buffer.read())

            EXCEL_LOGS.info('Excel data exported successfully')
            return response

        except Exception as e:
            EXCEL_LOGS.error('Error exporting Excel data: %s', str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

####################################################################################################

class FormExcelExportService:
    """
    Service class for exporting data to an Excel file with structured formatting.

    Example Data Structure for 'data' parameter:
        data = {
            'id': 123,
            'stages': [
                {'shipping_detail': 'Stage 1', 'quantity': 100, 'status': 'Pending'},
                {'shipping_detail': 'Stage 2', 'quantity': 200, 'status': 'In Progress'},
            ],
            'split_quantities': [
                {'shipping_detail': 'Split 1', 'quantity': 50, 'status': 'Approved'},
                {'shipping_detail': 'Split 2', 'quantity': 150, 'status': 'Rejected'},
            ],
            'laytime_calculator': {'shipping_detail': 'Calculator', 'allowed_time': 10,
                                    'actual_time': 8},
        }
    """
    def form_export_excel_data(self, data):
        """
        Export data to an Excel file with structured formatting.

        :param data: Data to be exported in Excel format.
                     Should be a dictionary containing the following keys:
                     - 'id': Ship detail ID.
                     - 'stages': List of dictionaries representing shipping stages data.
                     - 'split_quantities': List of dictionaries representing split quantities data.
                     - 'laytime_calculator': Dictionary representing laytime calculator data.
        :return: HttpResponse containing the Excel file as an attachment.
        """
        try:
            results = [data]
            EXCEL_LOGS.info('Received results: %s', results)

            stages_data = [result.get('stages', []) for result in results]
            EXCEL_LOGS.info('Extracted stages data: %s', stages_data)

            split_quantities_data = [result.get('split_quantities', [])
                                      for result in results if 'split_quantities' in result]
            laytime_calculator_data = [result.get('laytime_calculator', {}) for result in results]
            EXCEL_LOGS.info('Extracted laytime calculator data: %s', laytime_calculator_data)

            def create_dataframe(data_list):
                df = pd.DataFrame(data_list)
                df.columns = df.columns.map(str)
                return df.rename(columns=str.upper)

            df = create_dataframe(results)
            stages_df = create_dataframe([stage for stages in stages_data for stage in stages])
            stages_df = stages_df.rename(columns={'COUNT': 'IS INCLUDED'})
            stages_df['IS INCLUDED'] = stages_df['IS INCLUDED'].apply(
                lambda x: 'Yes' if x else 'No')

            split_quantities_df = create_dataframe(
                [split for splits in split_quantities_data for split in splits])
            laytime_df = create_dataframe(laytime_calculator_data)

            EXCEL_LOGS.info('DataFrames created')

            # Drop unnecessary columns
            drop_columns_common = ['CREATED_DATE', 'LAST_UPDATED_DATE', 'LAST_UPDATED_BY',
                                    'REMAINING_CARGO_QTY', 'SHIPPING_DETAIL', 'IS_DELETED',
                                    'IS_APPROVED', 'IS_ACTIVE', 'STAGES', 'SPLIT_QUANTITIES',
                                    'LAYTIME_CALCULATOR']
            drop_columns_specific = ['ID', 'STATUS', 'CREATED_BY']

            df.drop(columns=[col for col in drop_columns_common if col in df.columns], inplace=True)
            stages_df.drop(
                columns=[col for col in drop_columns_common + drop_columns_specific 
                         if col in stages_df.columns], inplace=True)
            split_quantities_df.drop(
                columns=[col for col in drop_columns_common + drop_columns_specific 
                         if col in split_quantities_df.columns], inplace=True)
            laytime_df.drop(
                columns=[col for col in drop_columns_common + drop_columns_specific 
                         if col in laytime_df.columns], inplace=True)
            df.columns = df.columns.str.replace('_', ' ')
            stages_df.columns = stages_df.columns.str.replace('_', ' ')
            split_quantities_df.columns = split_quantities_df.columns.str.replace('_', ' ')
            laytime_df.columns = laytime_df.columns.str.replace('_', ' ')

            if 'RATE TYPE' in df.columns:
                rate_type = df['RATE TYPE'].iloc[0].lower()
                if rate_type == 'loading':
                    df.rename(columns={'DISCHARGE RATE': 'LOADING RATE'}, inplace=True)
                elif rate_type == 'discharge':
                    df.rename(columns={'COMMENCED LOADING TIME': 'COMMENCED DISCHARGING TIME',
                                        'COMPLETED LOADING TIME': 'COMPLETED DISCHARGING TIME'},
                                        inplace=True)

            # Custom renaming in LAYTIME CALCULATIONS table
            if 'ACTUAL TIME' in laytime_df.columns:
                laytime_df.rename(columns={'ACTUAL TIME': 'USED TIME'}, inplace=True)

            if 'ALLOWED TIME' in laytime_df.columns and 'USED TIME' in laytime_df.columns:
                for index, row in laytime_df.iterrows():
                    if row['ALLOWED TIME'] > row['USED TIME']:
                        laytime_df.rename(columns={'TOTAL TIME DIFFERENCE': 'TIME SAVED',
                                                    'AMOUNT': 'TOTAL DESPATCH'}, inplace=True)
                    else:
                        laytime_df.rename(columns={'TOTAL TIME DIFFERENCE': 'TIME EXCEEDED',
                                                    'AMOUNT': 'TOTAL DEMURRAGE'}, inplace=True)
            excel_buffer = BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                def write_df_to_excel(writer, df, title, current_row, bg_color):
                    if not df.empty:
                        title_df = pd.DataFrame([title])
                        title_df.to_excel(writer, index=False, header=False,
                                           sheet_name='Sheet1', startrow=current_row)
                        worksheet = writer.sheets['Sheet1']
                        title_format = writer.book.add_format(
                            {'bold': True, 'align': 'center', 'bg_color': bg_color,
                              'font_color': 'white', 'text_wrap': True, 'valign': 'vcenter'})
                        # title_format = writer.book.add_format(
                        # {'bold': True, 'align': 'center', 'bg_color': '#DB4040',
                        #  'font_color': 'white', 'text_wrap': True, 'valign': 'vcenter'})# 00B400
                        header_format = writer.book.add_format(
                            {'bold': True, 'align': 'center',
                              'valign': 'vcenter', 'text_wrap': True})
                        cell_format = writer.book.add_format(
                            {'align': 'center', 'valign': 'vcenter',
                              'text_wrap': True})

                        worksheet.merge_range(
                            current_row, 0, current_row,
                              len(df.columns) - 1, title.upper(), title_format)
                        df.to_excel(
                            writer, index=False,
                              header=True, sheet_name='Sheet1', startrow=current_row + 1)

                        # Apply formatting to header and data cells
                        for col_num, value in enumerate(df.columns.values):
                            worksheet.write(current_row + 1, col_num, value, header_format)
                        for row_num in range(current_row + 2, current_row + 2 + df.shape[0]):
                            worksheet.set_row(row_num, cell_format=cell_format)

                        for col_num in range(len(df.columns)):
                            worksheet.set_column(col_num, col_num, 15, cell_format)

                        return current_row + df.shape[0] + 3
                    return current_row

                current_row = write_df_to_excel(writer, df, 'Ship Detail', 0, '#DB4040')
                current_row = write_df_to_excel(
                    writer, stages_df, 'Shipping Stages', current_row, '#DB4040')
                if not split_quantities_df.empty:
                    current_row = write_df_to_excel(
                        writer, split_quantities_df, 'Split Quantities', current_row, '#DB4040')
                # current_row = write_df_to_excel(
                # writer, laytime_df, 'Laytime Calculations', current_row)
                bg_color = '#DB4040'
                if 'ALLOWED TIME' in laytime_df.columns and 'USED TIME' in laytime_df.columns:
                    if any(laytime_df['ALLOWED TIME'] > laytime_df['USED TIME']):
                        bg_color = '#00B400'

                current_row = write_df_to_excel(
                    writer, laytime_df, 'Laytime Calculations', current_row, bg_color)
            excel_buffer.seek(0)

            response = HttpResponse(excel_buffer,
             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'
            return response

        except Exception as e:
            EXCEL_LOGS.error('Error occurred while exporting data to Excel: %s', str(e))
            return HttpResponse(status=500)
####################################################################################################

class GetDashboardData:
    """
    Class for retrieving dashboard data based on user groups and roles.
    """
    def get_dashboard_data(self, user):
        """
        Get dashboard data for the user based on their groups and roles.

        :param user: The user object for whom the dashboard data is requested.
        :return: A list of dictionaries containing dashboard data with keys 'name',
                 'value', and 'is_requester',
                 or None if an error occurs during data retrieval.
        """
        try:
            groups_list = list(
                user.groups.all().exclude(name='default').values_list('name', flat=True))
            approval_groups = getattr(settings, 'APPROVAL_GROUPS', [])
            common_groups = list(set(groups_list).intersection(approval_groups))
            is_requester = 'admin' in groups_list or 'requester' in groups_list
            status_counts = []
            action_counts = []

            if 'admin' in groups_list:
                status_counts = (
                    ShippingDetail.objects.values('status').annotate(count=Count('status'))
                )
                REQUEST.debug("Status counts for admin: %s",status_counts)
                # REQUEST.debug("Status counts for admin: %s", status_counts)

            else:
                for group_name in common_groups:
                    if group_name == 'Unit Finance':
                        shipping_qs = ShippingDetail.objects.filter(
                            status=f'{group_name}',
                              is_deleted=False).values('status').annotate(count=Count('status'))
                        workflow_trans = list(WorkflowTransactions.objects.filter(
                            request_id__in=list(shipping_qs.values_list('pk', flat=True)),
                            approver_user_if_group__iexact=user.username).values_list('request_id',
                                                                                       flat=True))
                        status_counts.extend(shipping_qs.exclude(pk__in=workflow_trans).filter(
                            Q(status=f'{group_name}')
                        ).values('status').annotate(count=Count('status')))
                    else:
                        status_counts.extend(ShippingDetail.objects.filter(
                            Q(status=f'{group_name}')
                        ).values('status').annotate(count=Count('status')))

                    action_counts.extend(
                        WorkflowTransactions.objects.filter(
                            Q(approver_user_if_group__iexact = user.username)
                            ).values('action').annotate(count=Count('action'))
                    )
                    REQUEST.debug("Action_and_counts: %s", action_counts)
                    REQUEST.debug("Status_and_counts: %s", status_counts)

                    status_counts = status_counts + action_counts
            response_data = []
            for status_count in status_counts:
                status_name = status_count.get('status') or status_count.get('action') or None
                count = status_count['count']

                response_data.append({
                    "name": status_name,
                    "value": count,
                    "is_requester": is_requester,
                })
            return response_data
        except Exception as e:
            REQUEST.error("Error in get_dashboard_data: %s", str(e))
            traceback.print_exc()
            return None, None

####################################################################################################

class PDFService:
    """
    Service class for processing data for PDF generation.
    """
    def calculate_time_difference(self, start_date_time, end_date_time, is_included, percentage):
        """
        Calculate the time difference between two datetime objects.

        :param start_date_time: Start datetime in '%Y-%m-%d %H:%M:%S' format.
        :param end_date_time: End datetime in '%Y-%m-%d %H:%M:%S' format.
        :return: Time difference formatted as 'HH:MM:SS'.
        """
        if not is_included:
            return "00:00:00"
        start_date_time = datetime.strptime(start_date_time, '%d-%m-%Y %H:%M')
        end_date_time = datetime.strptime(end_date_time, '%d-%m-%Y %H:%M')

        start_date_time = start_date_time.replace(microsecond=0)
        end_date_time = end_date_time.replace(microsecond=0)

        time_diff = end_date_time - start_date_time
        total_seconds = time_diff.total_seconds() * (percentage/100)
        hours = int(total_seconds // 3600)
        minutes = int (total_seconds % 3600) // 60
        seconds = int(total_seconds % 60)

        time_diff_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        REQUEST.debug("Time difference calculated: %s", time_diff_formatted)
        return time_diff_formatted

    def calculate_total_laytime_used(self, start_date_time, end_date_time, is_included, percentage):
        """
        Calculate the total laytime used based on start and end datetime.

        :param start_date_time: Start datetime in '%Y-%m-%d %H:%M:%S' format.
        :param end_date_time: End datetime in '%Y-%m-%d %H:%M:%S' format.
        :return: Total laytime used in days.
        """
        if not is_included:
            return 0

        start_date_time = datetime.strptime(start_date_time, '%d-%m-%Y %H:%M')
        end_date_time = datetime.strptime(end_date_time, '%d-%m-%Y %H:%M')

        total_laytime_timedelta = end_date_time - start_date_time
        total_laytime_days = (
            total_laytime_timedelta.total_seconds() * (percentage/100))/ (24 * 3600)
        total_laytime_rounded = round(total_laytime_days, 5)
        REQUEST.debug("Total laytime used calculated: %s days", total_laytime_rounded)
        return total_laytime_rounded

    def process_data(self, data):
        """
        Process data for PDF generation, excluding specific fields.

        :param data: Input data dictionary.
        :return: Processed data dictionary or None if an error occurs.
        """
        try:
            if data.get('rate_type') == 'loading':
                data['loading_rate'] = data.pop('discharge_rate')

            ship_detail = {
                field: data.get(field) for field in SHIP_DETAIL_FIELDS if field in data
            }

            if 'demurrage_rate_per_day' in ship_detail:
                ship_detail['demurrage_rate_per_day'] = f"$ {ship_detail['demurrage_rate_per_day']}"
            if 'allowed_time' in ship_detail:
                ship_detail['allowed_time'] = f"{ship_detail['allowed_time']} days"
            if 'turn_time_hours' in ship_detail:
                ship_detail['turn_time_hours'] = f"{ship_detail['turn_time_hours']} hrs"

            if ship_detail.get('rate_type') == 'discharge':
                ship_detail['commenced_discharging_time'] = (
                    ship_detail.pop('commenced_loading_time')
                )
                ship_detail['completed_discharging_time'] = (
                    ship_detail.pop('completed_loading_time')
                )

            stages = data['stages']
            for stage in stages:
                stage['is_included'] = stage.pop('count')

            stages = [{
                **{key: value for key, value in stage.items()
                   if key not in STAGES_FIELDS_TO_EXCLUDE},
                'time_difference_(HH:MM:SS)': PDFService.calculate_time_difference(self,
                    stage['start_date_time'], stage['end_date_time'],
                    stage['is_included'], stage['percentage']),
                'total_laytime_used_(days)': PDFService.calculate_total_laytime_used(self,
                    stage['start_date_time'], stage['end_date_time'],
                    stage['is_included'], stage['percentage'])
            } for stage in stages]

            stages.sort(key=itemgetter('start_date_time'))

            laytime_calculator = {
                field: data['laytime_calculator'][field]
                for field in LAYTIME_CALCULATIONS_FIELDS if field in data['laytime_calculator']
            }

            laytime_calculator['used_time'] = laytime_calculator.pop('actual_time', 0)

            if 'allowed_time' in laytime_calculator:
                laytime_calculator['allowed_time'] = f"{laytime_calculator['allowed_time']} days"
            if 'used_time' in laytime_calculator:
                laytime_calculator['used_time'] = f"{laytime_calculator['used_time']} days"

            if laytime_calculator.get('allowed_time', 0) > laytime_calculator.get('used_time', 0):
                if 'total_time_difference' in laytime_calculator:
                    laytime_calculator['time_saved'] = (
                        f"{laytime_calculator.pop('total_time_difference', 0)} days")
                if 'amount' in laytime_calculator:
                    laytime_calculator['total_despatch'] = (
                        f"$ {laytime_calculator.pop('amount', 0)}")
            else:
                if 'total_time_difference' in laytime_calculator:
                    laytime_calculator['time_exceeded'] = (
                        f"{laytime_calculator.pop('total_time_difference', 0)} days")
                if 'amount' in laytime_calculator:
                    laytime_calculator['total_demurrage'] = (
                        f"$ {laytime_calculator.pop('amount', 0)}")

            split_quantities = data.get('split_quantities', [])
            for sq in split_quantities:
                if 'amount' in sq:
                    sq['amount'] = f"$ {sq['amount']}"

            return {
                'ship_detail': {key: value for key, value in ship_detail.items() 
                                if key not in SHIP_DETAIL_FIELDS_TO_EXCLUDE},
                'stages': [{key: value for key, value in stage.items() 
                            if key not in STAGES_FIELDS_TO_EXCLUDE} for stage in stages],
                'split_quantities': [{key: value for key, value in sq.items() 
                                      if key not in SPLIT_QUANTITIES_FIELDS_TO_EXCLUDE}
                                      for sq in data.get('split_quantities', [])],
                'laytime_calculator': {key: value for key, value in laytime_calculator.items() 
                                       if key not in LAYTIME_CALCULATIONS_FIELDS_TO_EXCLUDE},
            }
        except Exception as e:
            traceback.print_exc()
            return None

    def handle_data_processing(self, model_name, pk=None):
        """
        Handle data processing for PDF generation.

        :param request: HTTP request object.
        :param model_name: Name of the model for data retrieval.
        :param pk: Optional primary key for specific data retrieval.
        :return: Processed data dictionary or None if an error occurs.
        """
        try:
            detail_view_service = DetailViewService()
            data = detail_view_service.retrieve_serialized_instance(pk, model_name)

            if data:
                pdf_service = PDFService()
                processed_data = pdf_service.process_data(data)
                return processed_data

            REQUEST.info("No data found for PDF processing.")
            return None
        except Exception as e:
            REQUEST.error("Error processing data: %s", str(e))
            traceback.print_exc()
            return {'message': f'Error processing the request: {str(e)}'}

####################################################################################################

class BulkApproval:
    """Handles triggering bulk workflow approval for multiple shipping requests."""
    def trigger_bulk_workflow(self, request, data):
        """
        Trigger bulk workflow approval for multiple requests.

        :param request: HTTP request object.
        :param data: Data containing request IDs, remarks, and action for bulk workflow.
        :return: Response data indicating the status of each request and any errors encountered.
        """
        try:
            request_ids = data.get('request_id', [])
            response_data = []
            remarks = data.get('remark')
            action = data.get('action')

            for request_id in request_ids:

                try:
                    req_obj = ShippingDetail.objects.get(id=request_id)

                    approval_button = to_show_approval_button(request, request_id, ShippingDetail)
                    approval_type = indicate_approval_type(request, 'laytime_details',
                                                            'ShippingDetail', request_id)

                    if approval_button and approval_type['approval_type']:

                        trigger_workflow(request, req_obj, remarks, WORKFLOW.get('APP_NAME'),
                                          'shippingdetail', action)
                        response_data.append({
                                'request_id': request_id,
                                'message': 'Success'
                        })
                        REQUEST.info("Workflow triggered successfully for request_id: %s",
                                      request_id)
                    else:
                        REQUEST.info("Skipping workflow trigger for request_id: %s", request_id)
                        response_data.append({
                        'request_id': request_id,
                        'message': "Failure",
                        })

                except Exception as e:
                    error_message = (f"Error triggering workflow for request_id {request_id}:"
                                     f"{str(e)}")
                    REQUEST.error(error_message)
                    traceback.print_exc()
                    response_data.append({
                        'request_id': request_id,
                        'error_message': error_message,
                    })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = f"Error triggering bulk workflow: {str(e)}"
            REQUEST.error(error_message)
            traceback.print_exc()
            return Response({'error': 'Internal Server Error', 'error_message': error_message},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
