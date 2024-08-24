# # C:\Users\shali\Documents\shalin\test-app\masters\views.py

# import json
# import traceback

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.dateparse import parse_datetime, parse_date
# from django.utils.decorators import method_decorator

# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication

# from datetime import datetime, timedelta
# from dateutil import parser
# from dateutil.parser import parse
# from masters.constants import WORKFLOW

# from masters.workflowtrigger import trigger_workflow
# from .services import LaytimeService,DetailViewService, CalculateAllowedTimeService, ExcelExportService, FormExcelExportService
# from .serializers import ShippingDetailSerializer, ShippingStageSerializer, LayTimeCalculatorSerializer, SplitQuantitySerializer
# from .logger import WORKFLOW_LOGS, USER_LOGS, REQUEST

# #########################################################################################################################################

# import traceback

# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])  
# class CreateViews(APIView):
         
#     def post(self, request):
#         print("\n-------------------------------- SHIPPING_DETAIL ----------------------------------------")
#         try:
#             data = request.data
#             LaytimeService.process_shipping_detail(data, request)

#             REQUEST.info("Shipping detail POST by User -- {} -- IP --{}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#             USER_LOGS.info("Shipping detail POST successfully by User -- {} -- IP --{}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#             REQUEST.debug(f"Data received in the request: {data}")

#             return Response({"message": "Data processed successfully"}, status=200)
#         except Exception as e:
#             traceback_str = traceback.print_exc()
            
#             REQUEST.info("POST Error by -- {} -- IP -- {}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#             REQUEST.error('Error occurred while processing shipping detail: {}'.format(e), exc_info=True)

#             return Response({'message': f'Error processing the request: {str(e)}', 'traceback': traceback_str}, status=500)

# #########################################################################################################################################

# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# class DetailViews(APIView): 
#     def get(self, request,  model_name, pk=None):
#         try:
#             if pk is None:
#                 # Retrieve all instances
#                 data = DetailViewService.retrieve_all_serialized_instances(model_name)
#             else:
#                 # Retrieve a single instance by primary key
#                 data = DetailViewService.retrieve_serialized_instance(pk, model_name)

#             if data:
#                 # REQUEST.info(f"Data retrieved successfully for {model_name} by User -- {str(request.user)} -- IP -- {request.META.get('REMOTE_ADDR')}")
#                 # USER_LOGS.info(f"Data retrieved successfully for {model_name} by User -- {str(request.user)} -- IP -- {request.META.get('REMOTE_ADDR')}")
#                 return Response(data)
#             else:
#                 REQUEST.info(f"{model_name} not found by User -- {str(request.user)} -- IP -- {request.META.get('REMOTE_ADDR')}")
#                 USER_LOGS.info(f"{model_name} not found by User -- {str(request.user)} -- IP -- {request.META.get('REMOTE_ADDR')}")
#                 return Response({'message': f'{model_name} not found'}, status=404)
#         except Exception as e:
#             # Log the error
#             REQUEST.error(f"An error occurred while retrieving {model_name}: {str(e)}")
#             USER_LOGS.error(f"An error occurred while retrieving {model_name}: {str(e)}")
#             return Response({'message': f'Error retrieving {model_name}: {str(e)}'}, status=500)
        
#     def patch(self, request, pk, model_name):
#         print("\n-------------------------------- UPDATE ----------------------------------------")
#         model_name = 'shipping_detail'
#         data = request.data

#         try:
#             REQUEST.info("Data received successfully by User -- {} -- IP --{}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#             USER_LOGS.info("Data received successfully by User -- {} -- IP --{}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#             REQUEST.debug(f"Data received in the request: {data}")

#             updated_data = DetailViewService.update_model_instance(pk, model_name, data)

#             if updated_data:
#                 REQUEST.info("PATCHED successfully by User -- {} -- IP --{}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#                 USER_LOGS.info("PATCHED successfully by User -- {} -- IP --{}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#                 REQUEST.debug(f"PATCHED Data received in the request: {data}")
#                 return Response(updated_data, status=200)
#             return Response({'message': f'Error updating {model_name}'}, status=400)
        
#         except Exception as e:
#             REQUEST.error(f"PATCH Error by User -- {str(request.user)} -- IP -- {request.META.get('REMOTE_ADDR')}: {str(e)}")
#             USER_LOGS.error(f"An error occurred: {str(e)}")
#             return Response({'message': f'Error updating {model_name}: {str(e)}'}, status=500)

#     def delete(self, request, pk=None, model_name=None):
#         if pk:
#             # Delete a single instance
#             success = DetailViewService.delete_model_instance(pk, model_name)
#             if success:
#                 REQUEST.info("DELETED {} from model -- {} successfully by User -- {} -- IP --{}".format(pk, model_name,str(request.user), request.META.get('REMOTE_ADDR')))
#                 USER_LOGS.info("DELETED {} from model -- {} successfully by User -- {} -- IP --{}".format(pk, model_name,str(request.user), request.META.get('REMOTE_ADDR')))
#                 return Response(status=204)
#             return Response({'message': f'{model_name} not found'}, status=404)
#         else:
#             # Delete multiple instances
#             data = request.data.get('items', [])
#             success = DetailViewService.delete_multiple_model_instances(data, model_name)
#             if success:
#                 deleted_items = ', '.join(str(item) for item in data)
#                 REQUEST.info("Multiple records DELETED successfully by User -- {} -- IP --{}. Deleted records: {}".format(str(request.user), request.META.get('REMOTE_ADDR'), deleted_items))
#                 USER_LOGS.info("Multiple records DELETED successfully by User -- {} -- IP --{}. Deleted records: {}".format(str(request.user), request.META.get('REMOTE_ADDR'), deleted_items))
#                 return Response(status=204)
#             return Response({'message': f'{model_name} not found'}, status=404)

# #########################################################################################################################################

# class CalculateAllowedTimeView(APIView):
#     @permission_classes([IsAuthenticated])
#     @authentication_classes([TokenAuthentication])
#     def post(self, request):
#         print("\n-------------------------------- CALCULATE_ALLOWED_TIME ----------------------------------------")
#         try:
#             data = json.loads(request.body)
#             result = CalculateAllowedTimeService.calculate_allowed_time(data)
#             REQUEST.info("Allowed time calculated successfully by User -- {} -- IP -- {}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#             USER_LOGS.info("Allowed time calculated successfully by User -- {} -- IP -- {}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#             return JsonResponse(result)
#         except Exception as e:
#             traceback_str = traceback.print_exc()
#             REQUEST.error("Error occurred while calculating allowed time by User -- {} -- IP -- {}".format(str(request.user), request.META.get('REMOTE_ADDR')))
#             return JsonResponse({'message': f'Error calculating allowed time: {str(e)}', 'traceback': traceback_str}, status=500)

# #########################################################################################################################################
      
# class CalculateTimeView(APIView):
#     @permission_classes([IsAuthenticated])
#     @authentication_classes([TokenAuthentication]) 
#     def post(self, request):
#         try:
#             print("\n-------------------------------- CALCULATE_TIME ----------------------------------------")
#             request.data
#             request.data.get('shipping_detail',{})
#             # Extract necessary data from the request

#             stages = request.data.get('stages',[])
#             other_data = request.data.get('otherData', {})
#             allowed_time = float(other_data.get('allowed_time', 0)) 
#             demurrage_rate_per_day = float(other_data.get('demurrage_rate_per_day', 0))
#             despatch_rate_per_day = float(other_data.get('despatch_rate_per_day', 0))
#             percentage = float(other_data.get('percentage', 100))

#             if not stages:
#                 return Response({'message': 'Shipping stage details list is empty'}, status=400)
            
#             # Call the calculate_time_details function
#             total_minute, amount, actual_time, total_time_difference, is_time_saved = LaytimeService.calculate_time_details(
#                 stages, allowed_time, demurrage_rate_per_day, despatch_rate_per_day, percentage
#             )

#             return Response({'calculatedData': {
#                 'amount': amount,
#                 'actual_time': actual_time,
#                 'allowed_time': allowed_time,
#                 'total_time_difference': total_time_difference,
#                 'is_time_saved': is_time_saved,
#             }}, status=200)

#         except Exception as e:
#             traceback.print_exc()
#             REQUEST.error("Error calculating laytime: {}".format(str(e)))
#             return Response({'message': 'Error calculating laytime'}, status=500)

# #########################################################################################################################################

# from api.filters import genericSearch, genericfilter, retrievePage, handleCombinationData, handleFilterData
# from django.conf import settings
# from api.config_app import QUERY_PARAMS
# from api.serializers import getGenericSerializer, GenericSerializerField, dropdownSerialzer
# from commons.functions import get_paginated_queryset
# from .models import ShippingDetail, ShippingStage, SplitQuantity, LayTimeCalculator
# WORKFLOW_MODEL_LIST = settings.__dict__['_wrapped'].__dict__['WORKFLOW_MODEL_LIST']

# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# class List(APIView):
#     def get(self, request):
#         """
#         GET for all i.e /list
#         :param request: the request object
#         :param app: the app name coming from decorator
#         :param model: the model name coming from decorator
#         :return: all the objects of the model
#         """
#         try:
#             model='shipping_detail'

#             # Retrieve the correct app and model using a common utility function
#             model_obj = DetailViewService.get_model_class(model)

#             page = None
#             query_params = dict(request.GET)
#             REQUEST.debug("Received query parameters: {}".format(query_params))
#             USER_LOGS.debug("Received query parameters: {}".format(query_params))

#             if 'page' in query_params:
#                 page, pagesize = retrievePage(query_params)
#                 REQUEST.debug("Page: {}".format(page))
#                 REQUEST.debug("Page size: {}".format(pagesize))

#             if query_params and page is None and "search" not in query_params and "filter" not in query_params:
#                 # Use a common function to handle dropdown data based on the provided query parameters
#                 return handleDropDownData(query_params, model_obj)
                
#             elif 'search' in query_params and 'filter' in query_params:
#                 # Use a common function to handle combination data (search and filter)
#                 return handleCombinationData(model, request, page, pagesize)
                
#             elif "search" in query_params:
#                 # Use a common function to handle search data
#                 print(request)
#                 print(request.GET)
#                 return handleSearchData(request)
                
#             elif "filter" in query_params:
#                 # Use a common function to handle filter data
#                 return handleFilterData(request, 'masters', 'ShippingDetail', page, pagesize)
            
#             else:
#                 groups_list = list(request.user.groups.all().values_list('name', flat=True))
#                 REQUEST.debug("User groups: {}".format(groups_list))
#                 USER_LOGS.debug("User groups: {}".format(groups_list))

#                 if 'admin' in groups_list:
#                     qs = ShippingDetail.objects.filter(is_deleted=False).order_by('-pk')
#                 else:
#                     qs = ShippingDetail.objects.filter(created_by=request.user.username, is_deleted=False).order_by('-pk')
#                 REQUEST.debug("Query set: {}".format(qs))

#                 paged_queryset = get_paginated_queryset(qs, pagesize, page)
#                 REQUEST.debug("Paged queryset: {}".format(paged_queryset))

#                 objs = paged_queryset.object_list
#                 serial = ShippingDetailSerializer(objs, many=True,  context={"request": request, "group": None})
#                 REQUEST.debug("Serializer: {}".format(serial))
#                 data = serial.data
                
#                 if page is not None:
#                         total_count = len(qs)
#                         response = {
#                             "total": total_count,
#                             "results": data
#                         }
#                 else:
#                     response = {"error": "Invalid data"}
#                 return Response(response, status=status.HTTP_200_OK)
#         except Exception as e:
#             REQUEST.error("Error occurred in List API: {}".format(str(e)))
#             return Response({'message': 'Error fetching data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def patch(self, request, pk, model_name):
#         try:
#             data = request.data
#             print('\nuser in update: ', request.user)
#             model_name = 'shipping_detail'
#             updated_data = DetailViewService.update_model_instance(pk, model_name, data)

#             if updated_data:
#                 REQUEST.info("Data updated successfully: {}".format(updated_data))
#                 USER_LOGS.info("Data updated successfully: {}".format(updated_data))
#                 return Response(updated_data, status=status.HTTP_200_OK)
#             return Response({'message': f'Error updating {model_name}'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             REQUEST.error("Error occurred while updating data: {}".format(str(e)))
#             return Response({'message': 'Error updating data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#     def delete(self, pk, model_name):
#         try:
#             success = DetailViewService.delete_model_instance(pk, model_name)
#             if success:
#                 REQUEST.info("Data deleted successfully")
#                 USER_LOGS.info("Data deleted successfully")
#                 return Response(status=204)
#             return Response({'message': f'{model_name} not found'}, status=404) 
#         except Exception as e:
#             REQUEST.error("Error occurred while deleting data: {}".format(str(e)))
#             return Response({'message': 'Error deleting data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])      
# def handleDropDownData(query_params, model):
#     for item in query_params:
#         query_params[item] = query_params[item][0]
#     if model._meta.model_name.lower() in WORKFLOW_MODEL_LIST:
#         add_attr = {QUERY_PARAMS['is_deleted']: False, 'is_approved': True, 'status': "Approved"}
#     else:
#         add_attr = {QUERY_PARAMS['is_deleted']: False}
#     query_params.update(add_attr)
#     objs = model.objects.filter(**query_params).order_by('name').distinct('name')
#     serial = dropdownSerialzer(model)
#     serializer = serial(objs, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# #########################################################################################################################################

# from django.db.models import Q, IntegerField, CharField, DateField, FloatField, DecimalField, DateTimeField, ManyToManyField
# from django.apps import apps
# from django.http import HttpRequest
# from rest_framework import status
# from rest_framework.response import Response

# def handleSearchData(request):
#     model = 'shipping_detail'
#     print('\nmodel: ',model)
#     search_query = request.GET.get("search")
#     print('\nmodel: ',search_query)
#     page = request.GET.get("page")
#     print('\nmodel: ',page)
#     pagesize = request.GET.get("pageSize")
#     print('\nmodel: ',pagesize)

#     if not model or not search_query:
#         return Response({'error': 'Model and search query are required'}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         page = int(page) if page else None
#         pagesize = int(pagesize) if pagesize else None
#     except ValueError:
#         return Response({'error': 'Page and pagesize must be integers'}, status=status.HTTP_400_BAD_REQUEST)

#     response = DetailViewService.handle_search_data(model, search_query, page, pagesize)
#     return response
      
# # @permission_classes([IsAuthenticated])
# # @authentication_classes([TokenAuthentication])
# # def get_fields(model):
# #     model_fields = []
# #     for field in model._meta.get_fields():
# #         if isinstance(field, (IntegerField, CharField, DateField, FloatField, DecimalField, DateTimeField)):
# #             model_fields.append(field.name)
# #         elif isinstance(field, ManyToManyField):
# #             model_fields.append(field.name)
# #             related_model = field.related_model
# #             model_fields.extend([f"{field.name}__{related_field.name}" for related_field in related_model._meta.get_fields()])

# #     return model_fields

# # @permission_classes([IsAuthenticated])
# # @authentication_classes([TokenAuthentication])
# # def handleSearchData(model, request, page, pagesize):
# #     try:
# #         model_obj = DetailViewService.get_model_class(model)
# #     except Exception as e:
# #         return Response({'error': f'Error getting model class: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #     queryset = model_obj.objects.filter(is_deleted=False).distinct('id')

# #     search_query = request.GET.get("search")
# #     print('\nsearch query: ', search_query)
# #     if not search_query:
# #         return Response({'message': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)

# #     model_fields = get_fields(model_obj)
# #     or_conditions = Q()

# #     for field in model_fields:
# #         lookup = f"{field}"
# #         if "__" in lookup:
# #             related_model_name = lookup.split("__")[0]

# #             related_field_name = lookup.split("__")[1]

# #             try:
# #                 related_model = model_obj._meta.get_field(related_model_name).related_model
# #                 related_field = related_model._meta.get_field(related_field_name)
# #             except Exception as e:
# #                 return Response({'error': f'Error accessing related model or field: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #             if isinstance(related_field, (CharField, DateField, FloatField, DecimalField, DateTimeField)) and not related_field.is_relation and not related_field.auto_created:
# #                 lookup += "__icontains"
# #             else:
# #                 continue
# #         else:
# #             try:
# #                 fields = model_obj._meta.get_field(field)
# #                 if isinstance(fields, (IntegerField, CharField, DateField, FloatField, DecimalField, DateTimeField)):
# #                     lookup += "__icontains"
# #                     print('\nlook up: ', lookup)
# #                 else:
# #                     continue
# #             except Exception as e:
# #                 return Response({'error': f'Error accessing field: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #         or_conditions |= Q(**{lookup: search_query})

# #     try:
# #         filtered_queryset = queryset.filter(or_conditions)
# #     except Exception as e:
# #         return Response({'error': f'Error filtering queryset: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #     if page is not None and pagesize is not None:
# #         try:
# #             total_count = filtered_queryset.count()

# #             start_index = (page - 1) * pagesize

# #             end_index = start_index + pagesize

# #             paginated_queryset = filtered_queryset[start_index:end_index]

# #             serializer = DetailViewService.get_serializer(model_obj)(paginated_queryset, many=True)

# #             response = {
# #                 "total": total_count,
# #                 "results": serializer.data
# #             }
# #             return Response(response, status=status.HTTP_200_OK)
# #         except Exception as e:
# #             return Response({'error': f'Error paginating results: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #     try:
# #         serializer = DetailViewService.get_serializer(model_obj)(filtered_queryset, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
# #     except Exception as e:
# #         return Response({'error': f'Error serializing queryset: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# #########################################################################################################################################

# from django.http import JsonResponse

# class ExcelExportView(APIView):
#     @permission_classes([IsAuthenticated])
#     @authentication_classes([TokenAuthentication])
#     @staticmethod
#     def post(request):
#         if request.method == 'POST':
#             try:
#                 data = json.loads(request.body.decode('utf-8'))
#                 response = ExcelExportService.export_excel_data(data)
#                 return response

#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)

#         return JsonResponse({'error': 'Invalid request method'}, status=400)
    
# class FormExcelExportView(APIView):
#     @permission_classes([IsAuthenticated])
#     @authentication_classes([TokenAuthentication])
#     @staticmethod
#     def post(request):
#         if request.method == 'POST':
#             try:
#                 data = json.loads(request.body.decode('utf-8'))
#                 response = FormExcelExportService.form_export_excel_data(data)
#                 return response

#             except Exception as e:
#                 return JsonResponse({'error': str(e)}, status=500)

#         return JsonResponse({'error': 'Invalid request method'}, status=400)


# #########################################################################################################################################
