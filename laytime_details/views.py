# C:\Users\shali\Documents\shalin\test-app\laytime_details\views.py

"""
Views for Laytime Details app.
"""

import json
import traceback

from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count, Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from api.config_app import QUERY_PARAMS
from api.filters import retrievePage, handleCombinationData, handleFilterData, handleSearchData
from api.serializers import dropdownSerialzer

from commons.backends import WorkflowAuthentication
from commons.functions import get_paginated_queryset
from workflow.models import WorkflowTransactions

from .services import (LaytimeService,
                      DetailViewService,
                      ExcelExportService,
                      FormExcelExportService,
                      GetDashboardData,
                      PDFService,
                      BulkApproval
                      )
from .serializers import ShippingDetailSerializer
from laytime_details.models import *
from .logger import WORKFLOW_LOGS, REQUEST, EXCEL_LOGS

WORKFLOW_MODEL_LIST = settings.__dict__['_wrapped'].__dict__['WORKFLOW_MODEL_LIST']

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class CreateViews(APIView):
    """
    API view for creating and processing shipping details.
    Requires authentication and token authentication.
    """
    def post(self, request):
        """
        Handle POST requests for creating and processing shipping details.

        :param request: HttpRequest object containing the HTTP request.
        :return: Response object containing a JSON response indicating the status of the request.
        :rtype: Response
        """
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')

        try:
            data = request.data
            if not data:
                return Response({'message': 'Data cannot be empty'}, status=400)
            REQUEST.info("POST by -- %s -- DATA -- %s -- IP -- %s",
                          str(user), str(request.data), str(ip_address))
            REQUEST.debug("Request data: %s", data)
            
            # LaytimeService().process_shipping_detail(request, data)
            # REQUEST.info("POST Successfully Executed by -- %s -- IP -- %s",
            #               str(user), str(ip_address))

            # return Response({"message": "Data processed successfully"}, status=200)

            response_data = LaytimeService().process_shipping_detail(request, data)
            if 'errors' in response_data:
                return Response({'message': 'Error processing data', 'errors': response_data['errors']}, status=400)
            
            REQUEST.info("POST Successfully Executed by -- %s -- IP -- %s",
                          str(user), str(ip_address))
            return Response({"message": "Data processed successfully", "data": response_data}, status=200)

        except Exception as e:
            REQUEST.error("POST Error by -- %s -- IP -- %s", str(user), str(ip_address))
            traceback.print_exc()
            return Response({'message': f'Error processing the request: {str(e)}'}, status=500)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class InitiateApprovalView(APIView):
    """
    API view for initiating approval process for shipping details.
    Requires authentication and token authentication.
    """
    def post(self, request, pk):
        """
        Handle POST requests for initiating approval process.

        :param request: HttpRequest object containing the HTTP request.
        :param pk: Primary key of the shipping detail to initiate approval for.
        :return: Response object indicating the status of the request.
        :rtype: Response
        """
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')

        try:
            # return Response({}, status=status.HTTP_200_OK)
            shipping_detail = ShippingDetail.objects.get(id=pk)
            LaytimeService.service_trigger_workflow(self, request, shipping_detail)
            REQUEST.info("Initiate Approval POST by -- %s IP -- %s", str(user), str(ip_address))
            REQUEST.info("Initiate Approval POST Successfully Executed by -- %s -- IP -- %s",
                          str(user), str(ip_address))
            return Response(status=status.HTTP_200_OK)
        except ShippingDetail.DoesNotExist:
            error_message = "ShippingDetail does not exist for the provided ID"
            REQUEST.error("Initiate Approval POST Error by -- %s -- IP -- %s", str(user),
                           str(ip_address))
            return Response({'message': error_message}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_message = f'Error processing Initiate Approval POST: {str(e)}'
            REQUEST.error("Initiate Approval POST Error by -- %s -- IP -- %s. Error: %s",
                           str(user), str(ip_address), error_message)
            traceback_str = traceback.format_exc()
            REQUEST.error("Traceback: %s", traceback_str)
            return Response({'message': error_message, 'traceback': traceback_str},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, WorkflowAuthentication])
class DetailViews(APIView):
    """
    API view for handling detail operations such as retrieval, update, and deletion.
    Requires authentication and token authentication.
    """
    def get(self, request,  model_name, pk=None):
        """
        Handle GET requests for retrieving details.

        :param request: HttpRequest object containing the HTTP request.
        :param model_name: Name of the model to retrieve details from.
        :param pk: Primary key of the detail to retrieve.
        :return: Response object containing retrieved data or error message.
        :rtype: Response
        """
        try:
            if pk is None:
                data = DetailViewService.retrieve_all_serialized_instances(self, model_name)
            else:
                data = DetailViewService.retrieve_serialized_instance(self, pk, model_name)
            if data:
                return Response(data)
            return Response({'message': f'{model_name} not found'}, status=404)
        except Exception as e:
            error_message = f"Error in getting method: {str(e)}"
            # Log the error with the object not found
            REQUEST.error("%s - Object with ID %s in %s not found", error_message, pk, model_name)
            return Response({'error': 'Internal Server Error'},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk, model_name):
        """
        Handle PATCH requests for updating details.

        :param request: HttpRequest object containing the HTTP request.
        :param pk: Primary key of the detail to update.
        :param model_name: Name of the model to update details for.
        :return: Response object indicating the status of the update operation.
        :rtype: Response
        """
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')

        try:
            model_name = 'shipping_detail'
            data = request.data
            data["shipping_detail"]['last_updated_by'] = request.user.username

            updated_data = DetailViewService.update_model_instance(self, pk, model_name, data)

            if updated_data:
                REQUEST.info("PATCH Successfully Executed by -- %s -- IP -- %s", str(user),
                              str(ip_address))
                return Response(updated_data, status=200)
            REQUEST.error("Error updating {model_name} - Object with ID {pk} not found")
            return Response({'message': f'Error updating {model_name}'}, status=400)

        except Exception as e:
            REQUEST.error("PATCH Error by -- %s -- IP -- %s",str(user), str(ip_address))
            traceback.format_exc()
            return Response({'message': f'Error processing the request: {str(e)}'}, status=500)

    def delete(self, request, pk=None, model_name=None):
        """
        Handle DELETE requests for deleting details.

        :param request: HttpRequest object containing the HTTP request.
        :param pk: Primary key of the detail to delete.
        :param model_name: Name of the model to delete details from.
        :return: Response object indicating the status of the delete operation.
        :rtype: Response
        """
        if pk:
            success = DetailViewService.delete_model_instance(self, pk, model_name)
            if success:
                return Response(status=204)
            return Response({'message': f'{model_name} not found'}, status=404)
        data = request.data.get('items', [])
        success = DetailViewService.delete_multiple_model_instances(self, data, model_name)
        if success:
            return Response(status=204)
        return Response({'message': f'{model_name} not found'}, status=404)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class CalculateAllowedTimeView(APIView):
    """
    API view for calculating allowed time.
    Requires authentication and token authentication.
    """
    def post(self, request):
        """
        Handle POST requests for calculating allowed time.

        :param request: HttpRequest object containing the HTTP request.
        :return: JsonResponse object containing the calculated result or error message.
        :rtype: JsonResponse
        """
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')
        try:
            # data = json.loads(request.body)
            data = request.data
            REQUEST.info("CALCULATE_ALLOWED_TIME POST by -- %s -- DATA -- %s -- IP -- %s",
                          str(user), str(request.data), str(ip_address))

            result = LaytimeService.calculate_allowed_time(data)
            return JsonResponse(result)

        except Exception as e:
            error_message = f'Error processing CALCULATE_ALLOWED_TIME POST: {str(e)}'
            REQUEST.error("CALCULATE_ALLOWED_TIME POST Error by -- %s -- IP -- %s. Error: %s",
                           str(user), str(ip_address), error_message)
            traceback_str = traceback.format_exc()
            REQUEST.error("Traceback: %s", traceback_str)
            return JsonResponse({'error': error_message, 'traceback': traceback_str}, status=500)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class CalculateTimeView(APIView):
    """
    API view for calculating laytime details.
    Requires authentication and token authentication.
    """
    def post(self, request):
        """
        Handle POST requests for calculating laytime details.

        :param request: HttpRequest object containing the HTTP request.
        :return: Response object containing the calculated laytime details or error message.
        :rtype: Response
        """
        user = request.user
        print('\n\ntime user: ',user)
        ip_address = request.META.get('REMOTE_ADDR')

        try:
            data = request.data
            shipping_detail = request.data.get('shipping_detail',{})

            stages = request.data.get('stages',[])
            other_data = request.data.get('otherData', {})
            allowed_time = float(other_data.get('allowed_time', 0))
            demurrage_rate_per_day = float(other_data.get('demurrage_rate_per_day', 0))
            despatch_rate_per_day = float(other_data.get('despatch_rate_per_day', 0))
            percentage = float(other_data.get('percentage', 100))

            if not stages:
                error_message = 'Shipping stage details list is empty'
                REQUEST.error("CALCULATE_TIME POST Error by -- %s -- IP -- %s. Error: %s",
                               str(user), str(ip_address), error_message)
                return Response({'message': 'Shipping stage details list is empty'}, status=400)

            # laytime_service = LaytimeService()
            total_minute, amount, actual_time, total_time_difference, is_time_saved = (
                LaytimeService.calculate_time_details(
                self, stages, allowed_time, demurrage_rate_per_day, despatch_rate_per_day
            ))

            calculated_data = {
                'amount': amount,
                'actual_time': actual_time,
                'allowed_time': allowed_time,
                'total_time_difference': total_time_difference,
                'is_time_saved': is_time_saved,
            }
            return_data = {'calculatedData': calculated_data}

            REQUEST.info("CALCULATE_TIME POST by -- %s -- DATA -- %s -- IP -- %s",
                          str(user), str(calculated_data), str(ip_address))
            REQUEST.debug("Request data: %s", data)
            return Response(return_data, status=200)

        except Exception as e:
            error_message = f'Error calculating laytime: {str(e)}'
            REQUEST.error("CALCULATE_TIME POST Error by -- %s -- IP -- %s. Error: %s",
                           str(user), str(ip_address), error_message)
            traceback_str = traceback.format_exc()
            return Response({'message': error_message, 'traceback': traceback_str}, status=500)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class List(APIView):
    """
    API view for handling list operations.
    Requires authentication and token authentication.
    """
    def get(self, request):
        """
        Handle GET requests for retrieving list data.

        :param request: HttpRequest object containing the HTTP request.
        :return: Response object containing the list data or error message.
        :rtype: Response
        """
        model='shipping_detail'

        model_obj = DetailViewService.get_model_class(self, model)
        model_name = model_obj.__name__ if model_obj else None

        page = None
        query_params = dict(request.GET)

        def handle_response(response_data):

            groups_list = list(request.user.groups.all().values_list('name', flat=True))
            is_requester = 'admin' in groups_list or 'requester' in groups_list

            response_data.data["is_requester"] = is_requester
            return response_data

        if 'page' in query_params:
            page, pagesize = retrievePage(query_params)

        if query_params and page is None and "search" not in query_params \
        and "filter" not in query_params:
            response_data = handleDropDownData(query_params, model_name)
            return handle_response(response_data)

        elif 'search' in query_params and 'filter' in query_params:
            response_data = handleCombinationData('laytime_details', model_name,
                                                   request, page, pagesize)
            return handle_response(response_data)

        elif "search" in query_params:
            return handleSearchData('laytime_details', model_name,
                                    request, page, pagesize)
            # response_data = handleSearchData(self, request)
            # return handle_response(response_data)

        elif "filter" in query_params:
            response_data = handleFilterData(request, 'laytime_details', model_name,
                                              page, pagesize)
            return handle_response(response_data)

        else:
            groups_list = list(request.user.groups.all().values_list('name', flat=True))
            approval_groups = getattr(settings, 'APPROVAL_GROUPS', [])
            common_groups = list(set(groups_list).intersection(approval_groups))

            if 'admin' in groups_list:
                qs = ShippingDetail.objects.filter(is_deleted=False).order_by('-pk')
            else:
                qs_list = []
                for group_name in common_groups:
                    if group_name == 'Unit Finance':
                        ports = set(groups_list) & set(['hazira', 'paradip', 'vizag'])

                        for port in ports:
                            shipping_qs = ShippingDetail.objects.filter(status=f'{group_name}',
                                        is_deleted=False).annotate(
                                            split_quantities_count=Count('split_quantities__id'))
                            if shipping_qs.filter(split_quantities_count=0):
                                    shipping_qs = shipping_qs.filter(discharge_port__iexact=port)
                            else:
                                shipping_qs = shipping_qs.filter(
                                    split_quantities__port_name__iexact=port)
                            workflow_trans = list(WorkflowTransactions.objects.filter(
                                request_id__in=list(shipping_qs.values_list('pk', flat=True))
                                ,approver_user_if_group__iexact=request.user.username
                                ).values_list('request_id', flat=True))
                            qs_list.extend(shipping_qs.exclude(pk__in=workflow_trans))
                    else:
                        qs_list.extend(ShippingDetail.objects.filter(
                        status=f'{group_name}', is_deleted=False).order_by('-pk'))
                qs = qs_list
            if not qs:
                qs = ShippingDetail.objects.filter(created_by=request.user.username,
             is_deleted=False).order_by('-pk')
            paged_queryset = get_paginated_queryset(qs, pagesize, page)
            objs = paged_queryset.object_list
            serial = ShippingDetailSerializer(objs, many=True,
                                                context={"request": request, "group": None})
            data = serial.data
            # is_requester = True if 'admin' in groups_list or 'requester' in groups_list else False
            is_requester = bool('admin' in groups_list or 'requester' in groups_list)

            if page is not None:
                # total_count = qs.count()
                total_count = len(qs)
                response = {
                    "total": total_count,
                    "results": data,
                    "is_requester": is_requester
                }
            else:
                response = {"error": "Invalid data"}
            return Response(response, status=status.HTTP_200_OK)

    def patch(self, request, pk, model_name):
        """
        Handle PATCH requests for updating a specific instance in the list.

        :param request: HttpRequest object containing the HTTP request.
        :param pk: Primary key of the instance to update.
        :param model_name: Name of the model to update the instance for.
        :return: Response object indicating the status of the update operation.
        :rtype: Response
        """
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')
        try:
            data = request.data
            model_name = 'shipping_detail'
            updated_data = DetailViewService.update_model_instance(self, pk, model_name, data)

            if updated_data:
                REQUEST.info("PATCH by -- %s -- DATA -- %s -- IP -- %s",
                              str(user), str(request.data), str(ip_address))
                REQUEST.info("PATCH Successfully Executed by -- %s -- IP -- %s",
                              str(user), str(ip_address))
                return Response(updated_data, status=status.HTTP_200_OK)
            REQUEST.error("PATCH Error by -- %s -- IP -- %s. Error updating %s",
                               str(user), str(ip_address), model_name)
            return Response({'message': f'Error updating {model_name}'},
                                 status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            REQUEST.error("PATCH Error by -- %s -- IP -- %s. Error: %s",
                           str(user), str(ip_address), str(e))
            return Response({'message': 'Internal Server Error'},
                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, pk, model_name):
        """
        Handle DELETE requests for deleting a specific instance from the list.

        :param request: HttpRequest object containing the HTTP request.
        :param pk: Primary key of the instance to delete.
        :param model_name: Name of the model to delete the instance from.
        :return: Response object indicating the status of the delete operation.
        :rtype: Response
        """
        success = DetailViewService.delete_model_instance(self, pk, model_name)
        if success:
            return Response(status=204)
        return Response({'message': f'{model_name} not found'}, status=404)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def handleDropDownData(query_params, model, is_requester):
    for item in query_params:
        query_params[item] = query_params[item][0]
    if model._meta.model_name.lower() in WORKFLOW_MODEL_LIST:
        add_attr = {QUERY_PARAMS['is_deleted']: False, 'is_approved': True, 'status': "Approved"}
    else:
        add_attr = {QUERY_PARAMS['is_deleted']: False}
    query_params.update(add_attr)
    objs = model.objects.filter(**query_params).order_by('name').distinct('name')
    serial = dropdownSerialzer(model)
    serializer = serial(objs, many=True)
    response_data = serializer.data

    # Add "is_requester" field to each item in the response
    for item in response_data:
        item["is_requester"] = is_requester
    return Response(serializer.data, status=status.HTTP_200_OK)

####################################################################################################

# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
# def handleSearchData(self, request):
#     """
#     Handle search data based on the provided search query.

#     :param request: HttpRequest object containing the HTTP request.
#     :return: Response object containing the search results or error message.
#     :rtype: Response
#     """
#     model = 'shipping_detail'
#     search_query = request.GET.get("search")
#     page = request.GET.get("page")
#     pagesize = request.GET.get("pageSize")
#     if not model or not search_query:
#         return Response({'error': 'Model and search query are required'},
#                          status=status.HTTP_400_BAD_REQUEST)
#     try:
#         page = int(page) if page else None
#         pagesize = int(pagesize) if pagesize else None
#     except ValueError:
#         return Response({'error': 'Page and pagesize must be integers'},
#                          status=status.HTTP_400_BAD_REQUEST)

    # response = DetailViewService.handle_search_data(self, model, search_query, page, pagesize,)
    # return response

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class ExcelExportView(APIView):
    """
    API view for exporting data to Excel format.
    Requires authentication and token authentication.
    """
    def post(self, request):
        """
        Handle POST requests for exporting data to Excel.

        :param request: HttpRequest object containing the HTTP request.
        :return: Response object containing the exported Excel data or error message.
        :rtype: Response
        """
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')
        try:
            REQUEST.info("ExcelExport POST by -- %s -- DATA -- %s -- IP -- %s",
                          str(user), str(request.body.decode('utf-8')), str(ip_address))
            data = json.loads(request.body.decode('utf-8'))
            EXCEL_LOGS.info("ExcelExport POST - Received data: %s",str(data))
            excel_export_service = ExcelExportService()
            response = excel_export_service.export_excel_data(data)
            return response

        except Exception as e:
            error_message = f"Error exporting Excel data: {str(e)}"
            traceback_str = traceback.format_exc()
            EXCEL_LOGS.error("ExcelExport POST Error - %s",error_message)
            EXCEL_LOGS.error("ExcelExport POST Error - Traceback: %s",traceback_str)
            return JsonResponse({'error': error_message, 'traceback': traceback_str}, status=500)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class FormExcelExportView(APIView):
    """
    API view for exporting specific form data to Excel format.
    Requires authentication and token authentication.
    """
    def post(self,request):
        """
        Handle POST requests for exporting form data to Excel.

        :param request: HttpRequest object containing the HTTP request.
        :return: Response object containing the exported Excel data or error message.
        :rtype: Response
        """
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')
        try:
            REQUEST.info("FormExcelExport POST by -- %s -- DATA -- %s -- IP -- %s",
                          str(user), str(request.body.decode('utf-8')), str(ip_address))
            data = json.loads(request.body.decode('utf-8'))
            EXCEL_LOGS.info("FormExcelExport POST - Received data: %s",str(data))
            form_excel_export_service = FormExcelExportService()
            response = form_excel_export_service.form_export_excel_data(data)
            return response

        except Exception as e:
            error_message = f"Error exporting FormExcel data: {str(e)}"
            traceback_str = traceback.format_exc()
            EXCEL_LOGS.error("FormExcelExport POST Error - %s",error_message)
            EXCEL_LOGS.error("FormExcelExport POST Error - Traceback: %s",traceback_str)
            return JsonResponse({'error': error_message, 'traceback': traceback_str}, status=500)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class Dashboard(APIView):
    """
    API view for fetching dashboard data.
    Requires authentication and token authentication.
    """
    def get(self, request):
        """
        Handle GET requests for fetching dashboard data.

        :param request: HttpRequest object containing the HTTP request.
        :return: Response object containing the dashboard data or error message.
        :rtype: Response
        """
        try:
            user = request.user
            get_dashboard_data = GetDashboardData()
            response_data = get_dashboard_data.get_dashboard_data(user)
            return Response(response_data, status=200)

        except Exception as e:
            error_message = f"Error fetching dashboard data: {str(e)}"
            traceback_str = traceback.format_exc()
            REQUEST.error("Dashboard Error - %s", error_message)
            REQUEST.error("Dashboard Error - Traceback: %s",traceback_str)
            return Response({"error": error_message, 'traceback': traceback_str}, status=500)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class PDF(APIView):
    """
    API view for generating PDF documents.
    Requires authentication and token authentication.
    """
    def get(self, request, model_name, pk=None, **kwargs):
        """
        Handle GET requests for generating PDF documents.

        :param request: HttpRequest object containing the HTTP request.
        :param model_name: Name of the model for which PDF is to be generated.
        :param pk: Primary key of the object (optional).
        :return: Response object containing the generated PDF or error message.
        :rtype: Response
        """
        try:
            pdf_service = PDFService()
            processed_data = pdf_service.handle_data_processing(model_name, pk)

            if processed_data:
                REQUEST.info("PDF GET processed data: %s", str(processed_data))
                return Response(processed_data)
            REQUEST.error("PDF GET Error - %s not found with ID %s", model_name, pk)
            return Response({'message': f'{model_name} not found with ID {pk}'}, status=404)

        except Exception as e:
            error_message = f"Error processing PDF GET request: {str(e)}"
            traceback_str = traceback.format_exc()
            REQUEST.error("PDF GET Error - %s", error_message)
            REQUEST.error("PDF GET Error - Traceback: %s", traceback_str)

            return Response({'message': error_message, 'traceback': traceback_str}, status=500)

####################################################################################################

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication, WorkflowAuthentication])
class BulkApprovalView(APIView):
    """
    API view for bulk approval operations.
    Requires authentication and token authentication, as well as workflow authentication.
    """
    def post(self, request):
        """
        Handle POST requests for bulk approval operations.

        :param request: HttpRequest object containing the HTTP request.
        :return: Response object containing the result of the bulk approval operation
                 or error message.
        :rtype: Response
        """
        try:
            user = request.user
            ip_address = request.META.get('REMOTE_ADDR', None)

            REQUEST.info("BulkApprovalView POST by -- %s IP -- %s",
                          str(user), str(ip_address))
            data = request.data
            WORKFLOW_LOGS.info("BulkApprovalView Workflow data: %s", str(data))
            service = BulkApproval()
            response = service.trigger_bulk_workflow(request, data)
            WORKFLOW_LOGS.info("BulkApprovalView Workflow response: %s", str(response))

            return response

        except Exception as e:
            error_message = f"Error in BulkApprovalView POST: {str(e)}"
            traceback_str = traceback.format_exc()

            WORKFLOW_LOGS.error("BulkApprovalView Error - %s", error_message)
            WORKFLOW_LOGS.error("BulkApprovalView Error - Traceback: %s", traceback_str)
            return JsonResponse({'error': error_message, 'traceback': traceback_str}, status=500)
