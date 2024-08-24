# # C:\Users\shali\Documents\shalin\test-app\masters\services.py

# from .models import ShippingDetail, ShippingStage, SplitQuantity, LayTimeCalculator
# from .serializers import ShippingDetailSerializer, ShippingStageSerializer, LayTimeCalculatorSerializer, SplitQuantitySerializer
# from .workflowtrigger import trigger_workflow
# from dateutil import parser
# from datetime import timedelta
# from django.utils import timezone
# from .constants import WORKFLOW
# import traceback
# from .logger import WORKFLOW_LOGS, USER_LOGS, REQUEST, EXCEL_LOGS

# from rest_framework import status
# from rest_framework.response import Response
# from django.db.models import Q
# from django.db.models import Q, IntegerField, CharField, DateField, FloatField, DecimalField, DateTimeField, ManyToManyField
# from django.apps import apps
# from django.http import HttpRequest
# from rest_framework import status
# from rest_framework.response import Response


# class LaytimeService:
#     @staticmethod
#     def process_shipping_detail(data, request):
#         try:

#             form_values_data = data['shipping_detail']
#             form_values_data['created_by'] = request.user.username
#             REQUEST.info('Created by -- {} -- IP -- {}'.format(form_values_data['created_by'],str(request.META.get('REMOTE_ADDR'))))
#             USER_LOGS.info('Created by -- {} -- IP -- {}'.format(form_values_data['created_by'],str(request.META.get('REMOTE_ADDR'))))

#             stages_data = form_values_data.pop('stages', None)
#             split_quantities_data = form_values_data.pop('split_quantities', None)
#             remaining_cargo_qty = form_values_data.pop('remaining_cargo_qty', None)
#             form_values_data['bl_date'] = parser.parse(form_values_data['bl_date']).date()

#             numeric_fields = ['turn_time_hours', 'demurrage_rate_per_day', 'despatch_rate_per_day', 'cargo_qty',
#                                'discharge_rate', 'allowed_time']
#             for field in numeric_fields:
#                 form_values_data[field] = float(form_values_data[field])

#             existing_shipping_detail = ShippingDetail.objects.filter(**form_values_data).first()

#             if existing_shipping_detail:
#                 shipping_detail_serializer = ShippingDetailSerializer(existing_shipping_detail, data=form_values_data)
#             else:
#                 shipping_detail_serializer = ShippingDetailSerializer(data=form_values_data)

#             if shipping_detail_serializer.is_valid():
#                 REQUEST.info('Shipping detail serializer is valid')
#                 shipping_detail = shipping_detail_serializer.save()

#                 shipping_stages = LaytimeService.process_shipping_stages(stages_data, shipping_detail)

#                 if split_quantities_data:
#                     split_quantities = LaytimeService.process_split_quantities(split_quantities_data, shipping_detail)
#                     SplitQuantity.objects.bulk_create(split_quantities)

#                 ShippingStage.objects.bulk_create(shipping_stages)

#                 LaytimeService.calculate_laytime(data, stages_data, shipping_detail.id)

#                 trigger_workflow(request, shipping_detail, WORKFLOW.get('INITIATED'),
#                                  WORKFLOW.get('APP_NAME'), WORKFLOW.get('MODEL_NAME'),
#                                  WORKFLOW.get('INIT'))
                
#                 if existing_shipping_detail:
#                     return shipping_detail, shipping_stages, split_quantities if split_quantities_data else None
#                 else:
#                     return shipping_detail.id, shipping_stages, split_quantities if split_quantities_data else None
#             else:
#                 REQUEST.error('Shipping detail serializer has errors: {}'.format(shipping_detail_serializer.errors))
#         except Exception as e:
#             REQUEST.error("Error processing shipping detail: {}".format(str(e)))
#             traceback.print_exc()
#         return None, None, None
    
# ###############################################################################################################################################

#     @staticmethod
#     def process_shipping_stages(stage_details_data, shipping_detail):
#         try:
#             shipping_stages = []

#             for detail in stage_details_data:
#                 if (
#                     detail and
#                     detail.get('count') and
#                     detail.get('stage_name') and
#                     detail.get('end_date_time') and
#                     detail.get('start_date_time') and
#                     detail.get('percentage') 
#                 ):
#                     existing_stage = ShippingStage.objects.filter(
#                         count=detail['count'],
#                         stage_name=detail['stage_name'],
#                         start_date_time=parser.parse(detail['start_date_time']),
#                         end_date_time=parser.parse(detail['end_date_time']),
#                         percentage = detail['percentage'],
#                         shipping_detail=shipping_detail
#                     ).first()

#                     if existing_stage:
#                         REQUEST.debug(f"Shipping stage already exists for shipping detail {shipping_detail.id}. Skipping creation.")
#                         REQUEST.debug(f"Stage '{existing_stage.stage_name}' already exists")
#                         # shipping_stages.append(existing_stage)
#                     else:
#                         stage_data = {
#                                 'count': detail['count'],
#                                 'stage_name': detail['stage_name'],
#                                 'start_date_time': parser.parse(detail['start_date_time']),
#                                 'end_date_time': parser.parse(detail['end_date_time']),
#                                 'percentage': detail['percentage'],
#                                 'shipping_detail': shipping_detail,
#                             }
#                         shipping_stage = ShippingStage(**stage_data)
#                         shipping_stages.append(shipping_stage)

#             return shipping_stages
#         except Exception as e:
#             REQUEST.error(f"Error processing shipping stage: {str(e)}")
#             traceback.print_exc() 
        

# ###############################################################################################################################################

#     @staticmethod
#     def process_split_quantities(split_details_data, shipping_detail):
#         split_quantities = []

#         for split_detail in split_details_data:
#             if (
#                 split_detail and
#                 split_detail.get('port_name') and
#                 split_detail.get('cargo_quantity') and
#                 split_detail.get('amount')
#             ):
#                 remaining_cargo_qty = split_detail.get('remaining_cargo_qty', None)

#                 existing_quantity = SplitQuantity.objects.filter(
#                     port_name=split_detail['port_name'],
#                     cargo_quantity=split_detail['cargo_quantity'],
#                     amount=split_detail['amount'],
#                     remaining_cargo_qty=remaining_cargo_qty,
#                     shipping_detail=shipping_detail
#                 ).first()

#                 if existing_quantity:
#                     REQUEST.debug(f"Split quantity already exists for shipping detail {shipping_detail.id}. Skipping creation.")
#                 else:
#                     split_data = {
#                         'port_name': split_detail['port_name'],
#                         'cargo_quantity': split_detail['cargo_quantity'],
#                         'amount': split_detail['amount'],
#                         'remaining_cargo_qty': remaining_cargo_qty,
#                         'shipping_detail': shipping_detail,
#                     }
#                     split_quantity = SplitQuantity(**split_data)
#                     split_quantities.append(split_quantity)

#         return split_quantities

# ###############################################################################################################################################

#     @staticmethod
#     # Include the calculate_time_details function here
#     def calculate_time_details(stage_details, allowed_time, demurrage_rate_per_day, despatch_rate_per_day, percentage):
#         total_minute = 0
#         amount = 0
#         actual_time = 0
#         total_time_difference = 0
#         is_time_saved = False
        
#         for each_stage in stage_details:
#             if (
#                 each_stage and
#                 each_stage.get('count') and
#                 each_stage.get('end_date_time') and
#                 each_stage.get('start_date_time')
#             ):
#                 # Convert string representations to datetime objects
#                 start_datetime = parser.parse(each_stage['start_date_time'])
#                 end_datetime = parser.parse(each_stage['end_date_time'])

#                 difference_in_minutes = int((end_datetime - start_datetime).total_seconds() / 60)  * (each_stage['percentage']/100)
#                 total_minute += difference_in_minutes

#         if total_minute and allowed_time and demurrage_rate_per_day and despatch_rate_per_day:
#             actual_time = round(total_minute / (24 * 60), 5)
#             total_time_difference = round(abs(allowed_time - actual_time), 5)

#             if allowed_time < actual_time:
#                 is_time_saved = False
#                 amount = round(total_time_difference * demurrage_rate_per_day, 5)
#             else:
#                 is_time_saved = True
#                 amount = round(total_time_difference * despatch_rate_per_day, 5)

#         return total_minute, amount, actual_time, total_time_difference, is_time_saved

#     @staticmethod
#     def calculate_laytime(data,stage_details_data,shipping_id):
#         print('\n-------------------------Process_Calculate_Laytime--------------------------')
#         try:    
#             calculated_data=[]

#             percentage = data.get("percentage", 100) / 100
#             # Extract required data from the input
#             allowed_time = float(data['shipping_detail']['allowed_time'])
#             demurrage_rate_per_day = float(data['shipping_detail']['demurrage_rate_per_day'])
#             despatch_rate_per_day = float(data['shipping_detail']['despatch_rate_per_day'])
            
#             # Call the calculate_time_details function
#             total_minute, amount, actual_time, total_time_difference, is_time_saved = LaytimeService.calculate_time_details(
#                 stage_details_data, allowed_time, demurrage_rate_per_day, despatch_rate_per_day, percentage
#             )

#             shipping_detail_instance = ShippingDetail.objects.get(id=shipping_id)
#             print('\nshipping_detail_instance: ',shipping_detail_instance)

#             shipping_detail_instance_id = shipping_detail_instance.id
#             print('\nshipping_detail_instance_id: ',shipping_detail_instance_id)

#             # Create or update LayTimeCalculator instance
#             laytime_calculator_data = {
#                 'shipping_detail': shipping_detail_instance_id,
#                 'amount': round(amount, 2),
#                 'actual_time': actual_time,
#                 'allowed_time': allowed_time,
#                 'total_time_difference': total_time_difference,
#                 'is_time_saved': is_time_saved,
#             }

#             laytime_calculator_serializer = LayTimeCalculatorSerializer(data=laytime_calculator_data)
#             if laytime_calculator_serializer.is_valid():
#                 laytime_calculator = laytime_calculator_serializer.save()
#                 calculated_data.append(laytime_calculator)

#                 shipping_detail_instance.save()
#             else:
#                 REQUEST.error(f"Error validating laytime calculator serializer: {laytime_calculator_serializer.errors}")

#             return calculated_data    

#         except Exception as e:
#             REQUEST.error(f"Error calculating laytime: {str(e)}")
#             return {'message': 'Error calculating laytime', 'error': str(e)}, 500

# ###############################################################################################################################################

# class CalculateAllowedTimeService:
#     @classmethod
#     def calculate_allowed_time(cls, data):
#         try:
#             cargo_qty = float(data.get("cargoQty", 0))
#             discharge_rate = float(data.get("dischRate", 0))

#             # Perform the calculation to get allowed time
#             allowed_time = (cargo_qty / discharge_rate) if discharge_rate != 0 else 0

#             REQUEST.info("Allowed time calculated successfully: cargoQty={}, dischRate={}, allowed_time={}".format(cargo_qty, discharge_rate, allowed_time))
#             USER_LOGS.info("Allowed time calculated successfully: cargoQty={}, dischRate={}, allowed_time={}".format(cargo_qty, discharge_rate, allowed_time))

#             return {'success': True, 'data': {'allowed_time': allowed_time}}

#         except Exception as e:
#             REQUEST.error("Error calculating allowed time: {}".format(str(e)))  
#             return {'success': False, 'message': 'Error calculating allowed time.'}

# ###############################################################################################################################################

# class DetailViewService:
    
#     @staticmethod
#     def get_queryset(model_class):
#         return model_class.objects.filter(is_deleted=False)
        
#     @staticmethod
#     def get_model_class(model_name):
#         model_classes = {
#             'shipping_detail': ShippingDetail,
#             'shipping_stage': ShippingStage,
#             'split_quantity': SplitQuantity,
#             'laytime_calculator': LayTimeCalculator,
#         }
#         return model_classes.get(model_name)

#     @staticmethod
#     def get_serializer(model_class):
#         serializers = {
#             ShippingDetail: ShippingDetailSerializer,
#             ShippingStage: ShippingStageSerializer,
#             SplitQuantity: SplitQuantitySerializer,
#             LayTimeCalculator: LayTimeCalculatorSerializer,
#         }
#         return serializers.get(model_class)

#     @classmethod
#     def retrieve_model_instance(cls, pk, model_name):
#         model_class = cls.get_model_class(model_name)
#         instance = cls.get_queryset(model_class).filter(pk=pk, is_deleted=False).first()
#         if instance:
#             return instance
#         else:
#             REQUEST.warning("Model instance not found for pk: {}, model: {}".format(pk, model_name))
#             USER_LOGS.warning("Model instance not found for pk: {}, model: {}".format(pk, model_name))
#             return None
#         # return cls.get_queryset(model_class).filter(pk=pk, is_deleted=False).first()

#     @staticmethod
#     def retrieve_all_serialized_instances(model_name):
#         model_class = DetailViewService.get_model_class(model_name)
#         queryset = DetailViewService.get_queryset(model_class)
#         serializer = DetailViewService.get_serializer(model_class)

#         serialized_data = [serializer(instance).data for instance in queryset]
#         return serialized_data
    
#     @staticmethod
#     def retrieve_serialized_instance( pk, model_name):
#         model_class = DetailViewService.get_model_class(model_name)
#         instance = DetailViewService.get_queryset(model_class).filter(pk=pk, is_deleted=False).first()

#         if instance:
#             serializer = DetailViewService.get_serializer(instance.__class__)(instance)
#             return serializer.data
#         else:
#             REQUEST.warning("Model instance not found for pk: {}, model: {}".format(pk, model_name))
#             USER_LOGS.warning("Model instance not found for pk: {}, model: {}".format(pk, model_name))
#             return None
    
#     @classmethod
#     def update_model_instance(cls, pk, model_name, data):
#         try: 
#             data = data
            
#             model_class = cls.get_model_class(model_name)
#             serializer_class = cls.get_serializer(model_class)
#             instance = cls.retrieve_model_instance(pk, model_name)

#             if instance:
#                 extracted_data = data.get('shipping_detail', {})
#                 extracted_stages = extracted_data.get('stages', [])
#                 extracted_split_quantities = extracted_data.get('split_quantities', [])

#                 serializer = serializer_class(instance, data=extracted_data, partial=True)

#                 if serializer.is_valid():
#                     updated_obj = serializer.save()
                    
#                     # Update nested fields
#                     if extracted_stages:
#                         instance.stages.all().delete()
#                         for stage_data in extracted_stages:
#                             stage_data.update({'shipping_detail': updated_obj})
#                             instance.stages.create(**stage_data)

#                     if extracted_split_quantities:
#                         instance.split_quantities.all().delete()
#                         for split_quantities in extracted_split_quantities:
#                             split_quantities.update({'shipping_detail': updated_obj})
#                             instance.split_quantities.create(**split_quantities)
#                     REQUEST.info("Model instance updated successfully: {}".format(updated_obj))
#                     USER_LOGS.info("Model instance updated successfully: {}".format(updated_obj))                                    
#                     return serializer.data
#                 else:
#                     REQUEST.error("Serializer errors: {}".format(serializer.errors))
#                     USER_LOGS.error("Serializer errors: {}".format(serializer.errors))
#                     return serializer.errors
#             else:
#                 REQUEST.warning("Model instance not found for pk: {}, model: {}".format(pk, model_name))
#                 USER_LOGS.warning("Model instance not found for pk: {}, model: {}".format(pk, model_name))
#                 return None
        
#         except Exception as e:
#             REQUEST.error("Error updating model instance: {}".format(str(e)))
#             USER_LOGS.error("Error updating model instance: {}".format(str(e)))
#             traceback.print_exc()

#     @classmethod
#     def delete_model_instance(cls, pk, model_name):
#         try:
#             model_instance = cls.retrieve_model_instance(pk, model_name)
#             if model_instance:
#                 model_instance.is_deleted = True
#                 model_instance.save()
#                 REQUEST.info("Model instance deleted successfully")
#                 USER_LOGS.info("Model instance deleted successfully")
#                 return True
#             else:
#                 REQUEST.warning("Model instance not found for pk: {}, model: {}".format(pk, model_name))
#                 USER_LOGS.warning("Model instance not found for pk: {}, model: {}".format(pk, model_name))
#                 return False
#         except Exception as e:
#             REQUEST.error("Error deleting model instance: {}".format(str(e)))
#             USER_LOGS.error("Error deleting model instance: {}".format(str(e)))
#             return False
        
#     @staticmethod
#     def delete_multiple_model_instances(pk_list, model_name):
#         try:
#             model_class = DetailViewService.get_model_class(model_name)

#             # Soft delete for each instance in the list
#             for pk in pk_list:
#                 instance = model_class.objects.filter(pk=pk).first()
#                 if instance:
#                     instance.is_deleted = True
#                     instance.save()
#             REQUEST.info("Multiple model instances deleted successfully")
#             USER_LOGS.info("Multiple model instances deleted successfully")
#             return True
#         except Exception as e:
#             REQUEST.error("Error deleting multiple model instances: {}".format(str(e)))
#             USER_LOGS.error("Error deleting multiple model instances: {}".format(str(e)))
#             return False

#     @staticmethod
#     def get_model_fields(model):
#         model_fields = []
#         for field in model._meta.get_fields():
#             if isinstance(field, (IntegerField, CharField, DateField, FloatField, DecimalField, DateTimeField)):
#                 model_fields.append(field.name)
#             elif isinstance(field, ManyToManyField):
#                 model_fields.append(field.name)
#                 related_model = field.related_model
#                 model_fields.extend([f"{field.name}__{related_field.name}" for related_field in related_model._meta.get_fields()])
#         return model_fields

#     @staticmethod
#     def filter_queryset(model_obj, search_query):
#         model_fields = DetailViewService.get_model_fields(model_obj)
#         or_conditions = Q()

#         for field in model_fields:
#             lookup = f"{field}"
#             if "__" in lookup:
#                 related_model_name = lookup.split("__")[0]
#                 related_field_name = lookup.split("__")[1]

#                 try:
#                     related_model = model_obj._meta.get_field(related_model_name).related_model
#                     related_field = related_model._meta.get_field(related_field_name)
#                 except Exception as e:
#                     raise Exception(f'Error accessing related model or field: {str(e)}')

#                 if isinstance(related_field, (CharField, DateField, FloatField, DecimalField, DateTimeField)) and not related_field.is_relation and not related_field.auto_created:
#                     lookup += "__icontains"
#                 else:
#                     continue
#             else:
#                 try:
#                     fields = model_obj._meta.get_field(field)
#                     if isinstance(fields, (IntegerField, CharField, DateField, FloatField, DecimalField, DateTimeField)):
#                         lookup += "__icontains"
#                     else:
#                         continue
#                 except Exception as e:
#                     raise Exception(f'Error accessing field: {str(e)}')

#             or_conditions |= Q(**{lookup: search_query})

#         queryset = model_obj.objects.filter(is_deleted=False).distinct('id')
#         filtered_queryset = queryset.filter(or_conditions)
#         return filtered_queryset

#     @staticmethod
#     def paginate_results(filtered_queryset, page, pagesize):
#         total_count = filtered_queryset.count()

#         start_index = (page - 1) * pagesize
#         end_index = start_index + pagesize

#         paginated_queryset = filtered_queryset[start_index:end_index]
#         return total_count, paginated_queryset

#     @staticmethod
#     def serialize_data(model_obj, queryset):
#         serializer = DetailViewService.get_serializer(model_obj)(queryset, many=True)
#         return serializer.data

#     @staticmethod
#     def handle_search_data(model, search_query, page=None, pagesize=None):
#         try:
#             model_obj = DetailViewService.get_model_class(model)
#         except Exception as e:
#             return Response({'error': f'Error getting model class: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         try:
#             filtered_queryset = DetailViewService.filter_queryset(model_obj, search_query)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         if page is not None and pagesize is not None:
#             try:
#                 total_count, paginated_queryset = DetailViewService.paginate_results(filtered_queryset, page, pagesize)
#                 serialized_data = DetailViewService.serialize_data(model_obj, paginated_queryset)
#                 response = {"total": total_count, "results": serialized_data}
#                 return Response(response, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'error': f'Error paginating results: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         try:
#             serialized_data = DetailViewService.serialize_data(model_obj, filtered_queryset)
#             return Response(serialized_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': f'Error serializing queryset: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# ###############################################################################################################################################

# import json
# import pandas as pd
# import openpyxl
# import numpy as np
# from django.http import JsonResponse, HttpResponse
# from io import BytesIO

# '''
# To get the ship detail, stages, split Quantites 
# and Laytime calculations IN ONE ROW in excel
# '''
# class ExcelExportService:
#     @staticmethod
#     def export_excel_data(data):
#         try:
#             results = data.get('results', [])
#             columns = data.get('columns', [])

#             # Create a DataFrame from the data
#             df = pd.DataFrame(results)
#             EXCEL_LOGS.info('DataFrame created from data: {}'.format(df))

#             # Extracting 'stages', 'split_quantities', and 'laytime_calculator' from 'results'
#             stages_data = [([{key: value for key, value in stage.items() if key not in ['count', 'is_deleted', 'shipping_detail']} 
#                              for stage in result.get('stages', [])])
#                            for result in results]
            
#             split_quantities_data = [([{key: value for key, value in split.items() if key not in ['remaining_cargo_qty', 'shipping_detail', 'is_deleted']} 
#                                        for split in result.get('split_quantities', [])])
#                                      for result in results]
            
#             laytime_calculator_data = []
#             for result in results:
#                 laytime_calculator = result.get('laytime_calculator', {})
#                 if isinstance(laytime_calculator, dict):
#                     laytime_calculator_data.append({key: value for key, value in laytime_calculator.items() if key not in ['is_time_saved', 'shipping_detail', 'is_deleted']})
            
#             # Creating DataFrames for 'stages', 'split_quantities', and 'laytime_calculator'
#             max_stage_count = max(len(stage) for stage in stages_data)
#             stage_dfs = []
#             for stages in stages_data:
#                 stage_dict = {}
#                 for i in range(max_stage_count):
#                     prefix = f"Stage{i}_"
#                     if i < len(stages):
#                         stage = stages[i]
#                         for key, value in stage.items():
#                             # Convert boolean values to proper representation
#                             if isinstance(value, bool):
#                                 value = str(value).capitalize()  # Convert to string representation
#                             stage_dict[prefix + key] = value
#                     else:
#                         for key in stages[0].keys():
#                             stage_dict[prefix + key] = np.nan
#                 stage_dfs.append(pd.DataFrame([stage_dict]))

#             new_df1 = pd.concat(stage_dfs, ignore_index=True)
#             EXCEL_LOGS.info('DataFrame created for stages: {}'.format(new_df1))
            
#             max_split_count = max(len(split) for split in split_quantities_data)
#             split_dfs = []
#             for splits in split_quantities_data:
#                 split_dict = {}
#                 for i in range(max_split_count):
#                     prefix = f"Split{i}_"
#                     if i < len(splits):
#                         split = splits[i]
#                         for key, value in split.items():
#                             # Convert boolean values to proper representation
#                             if isinstance(value, bool):
#                                 value = str(value).capitalize()  # Convert to string representation
#                             split_dict[prefix + key] = value
#                     else:
#                         for key in splits[0].keys():
#                             split_dict[prefix + key] = np.nan
#                 split_dfs.append(pd.DataFrame([split_dict]))

#             new_df2 = pd.concat(split_dfs, ignore_index=True)
#             EXCEL_LOGS.info('DataFrame created for split quantities: {}'.format(new_df2))
            
#             new_df3 = pd.concat([pd.DataFrame(laytime, index=[0]) for laytime in laytime_calculator_data], ignore_index=True)
#             EXCEL_LOGS.info('DataFrame created for laytime calculator: {}'.format(new_df3))

#             # Concatenate the DataFrames horizontally
#             df_concatenated = pd.concat([df, new_df1, new_df2, new_df3], axis=1)

#             # Drop unnecessary columns
#             df_concatenated.drop(['stages', 'split_quantities', 'laytime_calculator', 'is_deleted'], axis=1, inplace=True)

#             # Create a BytesIO buffer to store the Excel file
#             excel_buffer = BytesIO()

#             # Save the DataFrame to an Excel file
#             df_concatenated.to_excel(excel_buffer, index=False)

#             excel_buffer.seek(0)

#             # Save the Excel buffer to HttpResponse
#             response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             response['Content-Disposition'] = 'attachment; filename=data_export.xlsx'
#             response.write(excel_buffer.read())

#             EXCEL_LOGS.info('Excel data exported successfully')
#             return response

#         except Exception as e:
#             EXCEL_LOGS.error('Error exporting Excel data: {}'.format(str(e)))
#             import traceback
#             traceback.print_exc()
#             return JsonResponse({'error': str(e)}, status=500)
        
# '''
# To get the tables of ship detail, stages, split Quantites 
# and Laytime calculations SEPERATELY in excel
# '''
# class FormExcelExportService:
#     @staticmethod
#     def form_export_excel_data(data):
#         try:
#             results = [data]
#             EXCEL_LOGS.info('Received results: {}'.format(results))
        
#             # Extracting 'stages', 'split_quantities', and 'laytime_calculator' from 'results'
#             stages_data = [results.get('stages', []) for results in results]
#             EXCEL_LOGS.info('Extracted stages data: {}'.format(stages_data))

#             split_quantities_data = [results.get('split_quantities', []) for results in results]
#             EXCEL_LOGS.info('Extracted split quantities data: {}'.format(split_quantities_data))
            
#             laytime_calculator_data = [[results.get('laytime_calculator', []) for results in results]]
#             EXCEL_LOGS.info('Extracted laytime calculator data: {}'.format(laytime_calculator_data))

#             # Create a DataFrame from the data
#             df = pd.DataFrame(results)
#             EXCEL_LOGS.info('DataFrame created from data: {}'.format(df))

#             print('\nshape: ',df.shape)
            
#             # Creating DataFrames for 'stages', 'split_quantities', and 'laytime_calculator'
#             new_df1 = pd.DataFrame([stage for stages in stages_data for stage in stages])
#             new_df2 = pd.DataFrame([split for splits in split_quantities_data for split in splits])
#             new_df3 = pd.DataFrame([laytime for laytimes in laytime_calculator_data for laytime in laytimes])
            
#             EXCEL_LOGS.info('DataFrame created for stages: {}'.format(new_df1))
#             EXCEL_LOGS.info('DataFrame created for split quantities: {}'.format(new_df2))
#             EXCEL_LOGS.info('DataFrame created for laytime calculator: {}'.format(new_df3))

#             # Sort the DataFrames based on 'Shipping_detail' field
#             df.sort_values(by='id')
#             new_df1.sort_values(by='shipping_detail')
#             new_df2.sort_values(by='shipping_detail')
#             new_df3.sort_values(by='shipping_detail')

            
#             df = df.drop(['stages', 'split_quantities', 'laytime_calculator', 'is_deleted'], axis=1)
#             new_df1 = new_df1.drop(['count', 'is_deleted'], axis=1)
#             new_df2 = new_df2.drop(['remaining_cargo_qty', 'is_deleted'], axis=1)
#             new_df3 = new_df3.drop(['is_time_saved', 'is_deleted'], axis=1)

#             # Create a BytesIO buffer to store the Excel file
#             excel_buffer = BytesIO()

#             # Save all DataFrames to a single Excel file with one line skipped between them
#             with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
#                 current_row = 0

#                 # Iterate through unique Shipping_detail values
#                 for shipping_detail_id in df['id'].unique():
#                     # Leave a row
#                     current_row += 1

#                     # Add a row to print 'Ship Detail' title with bold style
#                     pd.DataFrame(['Ship Detail']).to_excel(writer, index=False, header=False, sheet_name='Sheet1', startrow=current_row, startcol=0)
                    
#                     # Add bold style to the first row
#                     worksheet = writer.sheets['Sheet1']

#                     cell_format = writer.book.add_format({'bold': True, 'bg_color': 'red'})

#                     # Set the width of the cells to 25 for the entire sheet
#                     cell_format_1 = writer.book.add_format({'valign': 'vcenter', 'align': 'center'})
                    
#                     for col_num, value in enumerate(['Ship Detail'], start=0):
#                         worksheet.write(current_row, col_num, value, cell_format)

#                     for sheet in writer.sheets.values():
#                         for col_num in range(len(df.columns.values)):
#                             sheet.set_column(col_num, col_num, 25)
                    
#                     df[df['id'] == shipping_detail_id].to_excel(writer, index=False, header=True, sheet_name='Sheet1', startrow=current_row+1, startcol=0, )
                    
#                     # Update the current row position
#                     current_row += df[df['id'] == shipping_detail_id].shape[0] + 3  

#                     # Add a row to display 'Shipping Stages' using pandas and bold style
#                     pd.DataFrame(['Shipping Stages']).to_excel(writer, index=False, header=False, sheet_name='Sheet1', startrow=current_row, startcol=0)
                    
#                     # Add bold style to the row
#                     for col_num, value in enumerate(['Shipping Stages'], start=0):
#                         worksheet.write(current_row, col_num, value, cell_format)

#                     for sheet in writer.sheets.values():
#                         for col_num in range(len(new_df1.columns.values)):
#                             sheet.set_column(col_num, col_num + len(df.columns) + 2, 25, cell_format_1)

#                     # Print Shipping Stages data
#                     new_df1[new_df1['shipping_detail'] == shipping_detail_id].to_excel(writer, startrow=current_row + 1, index=False, header=True, startcol=0)

#                     # Update the current row position
#                     current_row += new_df1[new_df1['shipping_detail'] == shipping_detail_id].shape[0] + 3  # +3 for the blank row, 'Shipping Stages' row, and one more blank row

#                     # Add a row to display 'Split Quantities' using pandas and bold style
#                     pd.DataFrame(['Split Quantities']).to_excel(writer, index=False, header=False, sheet_name='Sheet1', startrow=current_row, startcol=0)
                    
#                     # Add bold style to the row
#                     for col_num, value in enumerate(['Split Quantities'], start=0):
#                         worksheet.write(current_row, col_num, value, cell_format)

#                     for sheet in writer.sheets.values():
#                         for col_num in range(len(new_df2.columns.values)):
#                             sheet.set_column(col_num, col_num + len(df.columns) + 2, 25, cell_format_1) 

#                     # Print Split Quantities data
#                     new_df2[new_df2['shipping_detail'] == shipping_detail_id].to_excel(writer, startrow=current_row + 1, index=False, header=True, startcol=0)

#                     # Update the current row position
#                     current_row += new_df2[new_df2['shipping_detail'] == shipping_detail_id].shape[0] + 3  # +3 for the blank row, 'Split Quantities' row, and one more blank row

#                     # Add a row to display 'Laytime Calculations' using pandas and bold style
#                     pd.DataFrame(['Laytime Calculations']).to_excel(writer, index=False, header=False, sheet_name='Sheet1', startrow=current_row, startcol=0)
                    
#                     # Add bold style to the row
#                     for col_num, value in enumerate(['Laytime Calculations'], start=0):
#                         worksheet.write(current_row, col_num, value, cell_format)

#                     for sheet in writer.sheets.values():
#                         for col_num in range(len(new_df3.columns.values)):
#                             sheet.set_column(col_num, col_num + len(df.columns) + 2, 25, cell_format_1)

#                     # Print Laytime Calculations data
#                     new_df3[new_df3['shipping_detail'] == shipping_detail_id].to_excel(writer, startrow=current_row + 1, index=False, header=True, startcol=0)

#                     # Update the current row position
#                     current_row += new_df3[new_df3['shipping_detail'] == shipping_detail_id].shape[0] + 3  # +3 for the blank row, 'Laytime Calculations' row, and one more blank row

#             excel_buffer.seek(0)

#             # Save the Excel buffer to HttpResponse
#             response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             response['Content-Disposition'] = 'attachment; filename=data_export.xlsx'
#             response.write(excel_buffer.read())

#             return response

#         except Exception as e:
#             EXCEL_LOGS.error('Error exporting Excel data: {}'.format(str(e)))
#             import traceback
#             traceback.print_exc()
#             return JsonResponse({'error': str(e)}, status=500)





























































































































































# # class LaytimeService:
# #     @staticmethod
# #     def process_shipping_detail(data):
# #         try:
# #             # Extract shipping detail data from the input
# #             form_values_data = data['shipping_detail']
# #             print('\nShip Detail data: ', form_values_data)

# #             stages_data = form_values_data.pop('stages', None)
# #             print('\nShipping stage details data: ', stages_data)

# #             split_quantities_data = form_values_data.pop('split_quantities', None)
# #             print('\nSplit quantity details data: ', split_quantities_data)

# #             remaining_cargo_qty = form_values_data.pop('remaining_cargo_qty', None)

# #             form_values_data['bl_date'] = parser.parse(form_values_data['bl_date']).date()
            
# #             # form_values_data['nor_tendered'] = parser.parse(form_values_data['nor_tendered'])
# #             # form_values_data['commenced_loading_time'] = parser.parse(form_values_data['commenced_loading_time'])
# #             # form_values_data['completed_loading_time'] = parser.parse(form_values_data['completed_loading_time'])

# #             # Convert numeric fields to float
# #             numeric_fields = ['turn_time_hours', 'demurrage_rate_per_day', 'despatch_rate_per_day', 'cargo_qty',
# #                               'discharge_rate', 'allowed_time']
# #             for field in numeric_fields:
# #                 form_values_data[field] = float(form_values_data[field])

# #             # Check if the shipping detail already exists
# #             existing_shipping_detail = ShippingDetail.objects.filter(**form_values_data).first()
            
# #             print('\nExisting_shipping_detail: ', existing_shipping_detail)

# #             if existing_shipping_detail:
# #                 # Update existing shipping detail
# #                 shipping_detail_serializer = ShippingDetailSerializer(existing_shipping_detail, data=form_values_data)

# #                 if shipping_detail_serializer.is_valid():
# #                     print('\nIs Valid existing shipping_detail_serializer: ',shipping_detail_serializer.is_valid())
# #                     print('\nExisting shipping_detail_serializer: ', shipping_detail_serializer)
# #                     shipping_detail = shipping_detail_serializer.save()
# #                     shipping_id = shipping_detail.id
# #                     print(f"\nShippingDetail ID: {shipping_id}")
                    

# #                     # Process and create shipping stages and split quantities
# #                     shipping_stages = LaytimeService.process_shipping_stages(stages_data, shipping_detail)
# #                     print('\nShipping_stages: ', shipping_stages)
# #                     split_quantities = LaytimeService.process_split_quantities(split_quantities_data, shipping_detail)
# #                     print('\nSplit_quantities: ', split_quantities)

# #                     ShippingStage.objects.bulk_create(shipping_stages)
# #                     shipping_detail.stages.set(shipping_stages)
# #                     shipping_detail.save()
# #                     SplitQuantity.objects.bulk_create(split_quantities)
# #                     shipping_detail.split_quantities.set(split_quantities)
# #                     shipping_detail.save()
                    
# #                     laytime = LaytimeService.calculate_laytime(data, stages_data, shipping_id)
# #                     print('\nLay_time: ', laytime)

# #                     return shipping_detail, shipping_stages, split_quantities
# #                 else:
# #                     print('\nshipping_detail_serializer errors:', shipping_detail_serializer.errors)
# #             else:
# #                 # If it doesn't exist, create a new one
# #                 shipping_detail_serializer = ShippingDetailSerializer(data=form_values_data)

# #                 if shipping_detail_serializer.is_valid():
# #                     print('\nIs Valid shipping_detail_serializer: ',shipping_detail_serializer.is_valid())
# #                     print('\nShipping_detail_serializer: ', shipping_detail_serializer)
# #                     shipping_detail = shipping_detail_serializer.save()
# #                     shipping_id = shipping_detail.id

# #                     shipping_stages = LaytimeService.process_shipping_stages(stages_data, shipping_detail)
# #                     print('\nShipping_stages: ', shipping_stages)
# #                     split_quantities = LaytimeService.process_split_quantities(split_quantities_data, shipping_detail)
# #                     print('\nSplit_quantities: ', split_quantities)

# #                     ShippingStage.objects.bulk_create(shipping_stages)
# #                     shipping_detail.stages.set(shipping_stages)
# #                     shipping_detail.save()
# #                     SplitQuantity.objects.bulk_create(split_quantities)
# #                     shipping_detail.split_quantities.set(split_quantities)
# #                     shipping_detail.save()

# #                     laytime = LaytimeService.calculate_laytime(data, stages_data, shipping_id)
# #                     print('\nLayTime: ', laytime)
                    
                    
# #                     return shipping_id, shipping_stages, split_quantities
# #                 else:
# #                     print('\nshipping_detail_serializer errors:', shipping_detail_serializer.errors)

# #         except Exception as e:
# #             print(f"Error processing shipping detail: {str(e)}")
# #             traceback.print_exc() 
# #             return None, None, None
