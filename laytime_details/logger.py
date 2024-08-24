# C:\Users\shali\Documents\shalin\test-app\masters\logger.py

"""
Logger configuration for Laytime Details app.
"""

from .logger_directory import workflow_logger, requests_logger, user_logger, excel_logs

WORKFLOW_LOGS = workflow_logger()
USER_LOGS = user_logger()
REQUEST = requests_logger()
EXCEL_LOGS = excel_logs()
