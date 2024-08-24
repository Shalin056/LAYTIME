# C:\Users\shali\Documents\shalin\test-app\laytime_details\workflowmails.py\

"""
Module for triggering laytime emails in the workflow.
"""

import traceback
from django.contrib.auth.models import User
from workflow.models import WorkflowTransactions
from .functions import trigger_email
from .models import ShippingDetail
from .services import (PDFService)
from .logger import WORKFLOW_LOGS

def trigger_laytime_mails(approval_entry, trans_obj, groups=None):
    """
    Trigger laytime emails based on the approval entry and transaction object.

    Parameters:
    - approval_entry: The approval entry related to the workflow.
    - trans_obj: The transaction object representing the current state of the workflow.
    - groups: Optional parameter specifying user groups.

    Returns:
    None
    """

    try:
        template = 'APPROVED_MAIL'
        request_id = trans_obj.request_id
        action = trans_obj.action
        next_state = trans_obj.next_state
        remark = trans_obj.remarks
        subject = f'The Laytime Calculation request {request_id} is {next_state}.'
        next_approver_name = ''
        approval_link = ''
        initiator=''
        shipping_obj = ShippingDetail.objects.get(id=trans_obj.request_id)
        # subject = f'{'Despatch' if shipping_obj.laytime_calculator.is_time_saved else 'Demurrage'} Approval - {shipping_obj.vessel} - {shipping_obj.bl_date}'

        if trans_obj.action == 'Init':
            current_approver_name = trans_obj.approver
        else:
            current_approver_name = trans_obj.approver[0]

        if trans_obj.next_state == 'Unit Finance':
            if shipping_obj.split_quantities.all().count() > 0:
                split_ports = list(
                    shipping_obj.split_quantities.all().values_list(
                        'port_name', flat=True))
            else:
                split_ports = [shipping_obj.discharge_port]

            split_ports = [x.lower() for x in split_ports]
            approver_user = User.objects.get(username__iexact=approval_entry.approver)
            group_list = list(approver_user.groups.filter(
                name__in=['hazira', 'vizag', 'paradip']).values_list('name', flat=True))
            for i in group_list:
                if i not in split_ports:
                    return

        if trans_obj.current_state == 'Unit Finance':
            trans = WorkflowTransactions.objects.filter(
                request_id=shipping_obj.pk, current_state='Unit Finance')
            stages_count = shipping_obj.split_quantities.all().count() if shipping_obj.split_quantities.all().count() > 0 else 1
            if stages_count > 1 and stages_count != trans.count():
                return

        initiator = ShippingDetail.objects.get(id = trans_obj.request_id).created_by

        if approval_entry:
            next_approver_name = User.objects.get(username__iexact=approval_entry.approver).username

            approval_link='http://localhost:3000/app/ApprovalForm/' + approval_entry.approval_token

        pdf_service = PDFService()
        processed_data = pdf_service.handle_data_processing(
            model_name = 'shipping_detail', pk=trans_obj.request_id)

        context = {'current_approver_name': current_approver_name,
                    'approver_name': next_approver_name or initiator, 
                    'request_id': request_id,  
                    'action': action, 
                    'approval_link': approval_link if trans_obj.next_state not in ['Approved', 'Rejected'] else '',
                    'ship_detail': processed_data['ship_detail'],
                    'stages': processed_data['stages'],
                    'split_quantities': processed_data['split_quantities'],
                    'laytime': processed_data['laytime_calculator'],
                    'next_state': next_state,
                    'remark': remark,
                    'initiator': initiator,
                    }

        WORKFLOW_LOGS.info("Triggering laytime mails.")
        WORKFLOW_LOGS.debug("Context: %s", context)

        trigger_email(template, context, subject, ['admin@gmail.com'], [])

    except Exception as ex:
        WORKFLOW_LOGS.error("Error in trigger_laytime_mails: %s", ex)
        traceback.print_exc()
        print(ex)
