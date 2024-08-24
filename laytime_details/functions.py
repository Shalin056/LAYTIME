# C:\Users\shali\Documents\shalin\test-app\laytime_details\functions.py

"""
Utility functions for Laytime Details app.
"""

import traceback
from django.conf import settings
from commons.mail_utils import render_html_message_simple, send_email, \
    prepare_email_message_simple
from .models import ShippingDetail
from workflow.models import WorkflowTransactions


def return_ship_detail(request):
    """
    Return active shipping details.
    """
    user = request.user
    groups_list = list(user.groups.all().exclude(name='default').values_list('name', flat=True))
    approval_groups = getattr(settings, 'APPROVAL_GROUPS', [])
    common_groups = list(set(groups_list).intersection(approval_groups))
    if 'admin' in groups_list:
        return ShippingDetail.objects.filter(is_deleted=False).order_by('-pk')
    else:
        qs_list = ShippingDetail.objects.none()
        for group_name in common_groups:
            if group_name == 'Unit Finance':
                shipping_qs = ShippingDetail.objects.filter(
                    status=f'{group_name}', is_deleted=False)
                workflow_trans = list(WorkflowTransactions.objects.filter(
                    request_id__in=list(shipping_qs.values_list('pk', flat=True)),
                        approver_user_if_group__iexact=request.user.username).values_list(
                            'request_id', flat=True))
                qs_list = qs_list | shipping_qs.exclude(pk__in=workflow_trans)
            else:
                qs_list = qs_list | ShippingDetail.objects.filter(
                    status=f'{group_name}', is_deleted=False).order_by('-pk')
        return qs_list

def return_excel_ship_detail(request):
    ship_details = ShippingDetail.objects.filter(is_deleted=False).order_by('-pk')
    return ship_details

def trigger_email(template, context, subject, to_list, cc_list):
    """
    Trigger email sending.
    
    Args:
        template (str): Email template.
        context (dict): Context data for rendering the template.
        subject (str): Email subject.
        to_list (list): List of recipients.
        cc_list (list): List of recipients for CC.
    """
    try:
        html_content = render_html_message_simple(template, context)
        mail = prepare_email_message_simple(subject, to_list, cc_list, html_content)
        print(mail)
    except Exception as ex:
        traceback.format_exc()
        print(ex)
