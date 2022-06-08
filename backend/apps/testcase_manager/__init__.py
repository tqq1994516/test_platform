# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:15
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : __init__.py.py
# @Project : test_platform
# @Description : testcase manager model
from sanic.blueprints import Blueprint

from apps.testcase_manager.views import *
from settings import API_VERSION

# 不可使用驼峰写法
PATH = '/testcase_manager'
NAME = 'testcase_manager'
testcase_manager = Blueprint(NAME, PATH, version=API_VERSION[0])
testcase_manager.add_route(TestcaseSitesView.as_view(), '/testcase_sites/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcasesView.as_view(), '/testcases', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseDetailView.as_view(), '/testcase_detail/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseOperationStepsView.as_view(), '/testcase_operation_steps/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseDependenceView.as_view(), '/testcase_dependence/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseFilesView.as_view(), '/testcase_files/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseCommentsView.as_view(), '/testcase_comments/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseChangeLogsView.as_view(), '/testcase_change_logs/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseExecuteRecordsView.as_view(), '/testcase_execute_records/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseExecuteLogsView.as_view(), '/testcase_execute_logs/<pk:strorempty>',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(testcase_log_read, 'testcase_execute_log_read/', methods=['GET'])
testcase_manager.add_websocket_route(testcase_run, '/testcase_run')

