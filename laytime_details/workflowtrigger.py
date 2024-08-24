# C:\Users\shali\Documents\shalin\test-app\laytime_details\workflowtrigger.py

"""
Module for triggering workflow on objects and updating their status.
"""

from workflow.services import approval_workflow

def trigger_workflow(request, request_obj, remarks, app, model, action):
    """
    Triggers workflow on passed object & save status on the requested object
    :param request: Http request object
    :param request_obj: the object on whcih workflow to be triggered
    :param remarks: remarks coming from UI
    :param app: app name <str>
    :param model: model name <str>
    :param action: action performed <Init / Approve /Reject>
    :return: None
    :rtype: None
    """
    request_status, workflow_completed = approval_workflow(app=app, model=model,
                                                           pk=request_obj.pk, action=action,
                                                           remarks=remarks,
                                                           request=request,
                                                           requesting_approvers=request.data.
                                                           get('approval_type'))
    request_obj.status = request_status
    request_obj.is_approved = True if request_status == 'Approved' else False
    print(remarks)
    request_obj.save()
