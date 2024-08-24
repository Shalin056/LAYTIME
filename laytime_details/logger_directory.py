# C:\Users\shali\Documents\shalin\test-app\masters\logger_directory.py

"""
Create the LOGGER Objects
for now i.e
Requests Logger , User Logger
"""
import os

from django.conf import settings
from logging_essar import init_logging

def requests_logger():
    """
    :return Returns the Requests Logger Objects: 
    """
    return init_logging(log_name='REQ_LOGS', log_level="DEBUG", rotation_criteria='time',
                        enable_mailing=False, rotate_interval=1, rotate_when='d',
                        backup_count=30, log_directory=os.path.join(settings.BASE_DIR, 'logs'))

def user_logger():
    """
    :return Returns the User Logger Object: 
    """
    return init_logging(log_name='USER_LOGS', log_level="DEBUG", rotation_criteria='time',
                        enable_mailing=False , rotate_interval=1, rotate_when='d',
                        backup_count=30, log_directory=os.path.join(settings.BASE_DIR, 'logs'))

# def request_data_post_logger():
#     """
#     :return Returns the Requests DATA Logger Objects:
#     """
#     return init_logging(log_name='REQ_POST_LOGS', log_level="DEBUG", rotation_criteria='time',
                        # enable_mailing=False, rotate_interval=1, rotate_when='d', backup_count=30,
                        # log_directory=os.path.join(settings.BASE_DIR, 'logs'))

def excel_logs():
    """
    Logs for Excel Import Export
    :return Returns the Excel Logger Objects:
    """
    return init_logging(log_name='EXCEL_LOGS', log_level="DEBUG", rotation_criteria='time',
                        enable_mailing=False, rotate_interval=1, rotate_when='d', backup_count=30,
                        log_directory=os.path.join(settings.BASE_DIR, 'logs'))

def workflow_logger():
    """
    Logs for Workflow
    :return Returns the Workflow Logger Objects:
    """
    return init_logging(log_name='WORKFLOW_LOGS', log_level="DEBUG", rotation_criteria='time',
                        enable_mailing=False, rotate_interval=1, rotate_when='d', backup_count=30,
                        log_directory=os.path.join(settings.BASE_DIR, 'logs'))
