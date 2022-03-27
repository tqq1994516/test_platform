# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:48
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : urls.py
# @Project : test_platform
# @Description : ...
from srf.routes import ViewSetRouter

from apps.testcase_manager.views import TestcaseSitesView, TestcasesView, TestcaseDetailView, \
    TestcaseOperationStepsView, TestcaseDependenceView, TestcaseFilesView, TestcaseCommentsView, TestcaseChangeLogsView

route = ViewSetRouter(True)
route.register(TestcaseSitesView, '/testcase_sites', 'testcase_sites')
route.register(TestcasesView, '/testcases', 'testcases')
route.register(TestcaseDetailView, '/testcase_detail', 'testcase_detail')
route.register(TestcaseOperationStepsView, '/testcase_operation_steps', 'testcase_operation_steps')
route.register(TestcaseDependenceView, '/testcase_dependence', 'testcase_dependence')
route.register(TestcaseFilesView, '/testcase_files', 'testcase_files')
route.register(TestcaseCommentsView, '/testcase_comments', 'testcase_comments')
route.register(TestcaseChangeLogsView, '/testcase_change_logs', 'testcase_change_logs')
urls = [] + route.urls
