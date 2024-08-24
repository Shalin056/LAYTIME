# C:\Users\shali\Documents\shalin\test-app\laytime_details\urls.py

"""
URL configuration for Laytime Details app.
"""

from django.urls import path
from .views import (CreateViews,
                    InitiateApprovalView,
                    DetailViews,
                    CalculateAllowedTimeView,
                    CalculateTimeView,
                    List,
                    ExcelExportView,
                    FormExcelExportView,
                    Dashboard,
                    PDF,
                    BulkApprovalView)

urlpatterns = [
    path('create/', CreateViews.as_view(),name = 'create_views'),
    path('initiate-approval/<int:pk>/', InitiateApprovalView.as_view(), name='initiate_approval'),
    path('detail/<str:model_name>/<int:pk>/', DetailViews.as_view(), name = 'details_views'),
    path('detail/<str:model_name>/', DetailViews.as_view(), name='all_details_views'),
    path('calculate-allowed-time/', CalculateAllowedTimeView.as_view(),
          name='calculate_allowed_time'),
    path('calculate-time/', CalculateTimeView.as_view(), name='calculate_time'),
    path('list/', List.as_view(), name='list_view'),
    path('excel-export/', ExcelExportView.as_view(), name='excel_export'),
    path('form-excel-export/', FormExcelExportView.as_view(), name='form_excel_export' ),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('pdf/<str:model_name>/<int:pk>/', PDF.as_view(), name = 'pdf'),
    path('bulkApproval/', BulkApprovalView.as_view(), name = 'bulkapproval')
]
