# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:15
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : __init__.py.py
# @Project : test_platform
# @Description : testcase manager model
from sanic.blueprints import Blueprint

# 不可使用驼峰写法
from apps.testcase_manager.views import TestcaseSitesView, TestcasesView, TestcaseDetailView, \
    TestcaseOperationStepsView, TestcaseDependenceView, TestcaseFilesView, TestcaseCommentsView, TestcaseChangeLogsView
from settings import API_VERSION

PATH = '/testcase_manager'
NAME = 'testcase_manager'
testcase_manager = Blueprint(NAME, PATH, version=API_VERSION[0])
testcase_manager.add_route(TestcaseSitesView.as_view(), '/testcase_sites',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcasesView.as_view(), '/testcases', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseDetailView.as_view(), '/testcase_detail',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseOperationStepsView.as_view(), '/testcase_operation_steps',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseDependenceView.as_view(), '/testcase_dependence',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseFilesView.as_view(), '/testcase_files',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseCommentsView.as_view(), '/testcase_comments',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
testcase_manager.add_route(TestcaseChangeLogsView.as_view(), '/testcase_changelogs',
                           methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
