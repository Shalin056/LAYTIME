# C:\Users\shali\Documents\shalin\test-app\laytime_details\management\commands\workflow_reminder.py

import traceback
from laytime_details.functions import trigger_email
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from laytime_details.models import ShippingDetail, LayTimeCalculator
from workflow.models import WorkflowTransactions, ApprovalLinkSent
from django.utils import timezone
from collections import defaultdict

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Trigger Laytime reminder Mails
        """
        try:
            template = 'REMINDER_MAIL'

            pending_shipping_requests = ShippingDetail.objects.all().exclude(status__in=['Approved', 'Rejected','Draft'])

            next_approver_cases = defaultdict(list)

            for x in pending_shipping_requests:
                workflow_trans = WorkflowTransactions.objects.filter(request_id=x.pk).last()

                next_state = workflow_trans.next_state

                status = x.status

                if status not in ['Approved', 'Rejected']:
                    approver = workflow_trans.approver.strip("[]'\"") if workflow_trans.approver else None

                    last_trans_created_date = workflow_trans.created_date 

                    current_date = timezone.now()

                    time_difference = (current_date - last_trans_created_date).days

                    # if time_difference % 3 == 0:
                    if True:
                        next_approver = eval(workflow_trans.next_approver) if workflow_trans.next_approver else []

                        users = list(User.objects.filter(groups__name__in=next_approver).values_list('email', flat=True))

                        link = list(ApprovalLinkSent.objects.filter(request_id = x.pk).values())[0].get('approval_token')
                        approval_link = 'http://localhost:3000/app/ApprovalForm/' + link

                        bulk_approval_link = 'http://localhost:3000/app'

                        processed_data = list(LayTimeCalculator.objects.filter(shipping_detail_id = x.id).values())[0]

                        context = {
                                 'request_id': x.pk,
                                 'next_state': next_state,
                                 'status': status,
                                 'amount' : processed_data.get('amount'),
                                 'actual_time' : processed_data.get('actual_time'),
                                 'allowed_time' : processed_data.get('allowed_time'),
                                 'approval_link': approval_link,
                                 'bulk_approval_link': bulk_approval_link
                        }

                        next_approver_tuple = tuple(next_approver) if next_approver else ()
                        next_approver_cases[next_approver_tuple].append(context)

            for next_approver, cases in next_approver_cases.items():
                total_pending_cases = len(cases)
                combined_context = {
                    'pending_cases': cases,
                }

                subject = f'Total ({total_pending_cases} cases) of Laytime Calculation requests are pending.'

                trigger_email(template, combined_context, subject,users,[])

        except Exception as ex:
            traceback.print_exc()
            print(ex)