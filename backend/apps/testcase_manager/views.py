# -*- coding: utf-8 -*-
# @Time : 2022/2/11 11:47
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : views.py
# @Project : test_platform
# @Description : view file
from srf import ModelViewSet

from apps.testcase_manager.models import TestcaseSites, Testcases, TestcaseDetail, TestcaseOperationSteps, \
    TestcaseDependence, TestcaseFiles, TestcaseComments, TestcaseChangeLogs
from apps.testcase_manager.serializers import TestcaseSitesSerializer, TestcasesSerializer, TestcaseDetailSerializer, \
    TestcaseOperationStepsSerializer, TestcaseDependenceSerializer, TestcaseFilesSerializer, TestcaseCommentsSerializer, \
    TestcaseChangeLogsSerializer


class TestcaseSitesView(ModelViewSet):
    serializer_class = TestcaseSitesSerializer
    queryset = TestcaseSites


class TestcasesView(ModelViewSet):
    serializer_class = TestcasesSerializer
    queryset = Testcases


class TestcaseDetailView(ModelViewSet):
    serializer_class = TestcaseDetailSerializer
    queryset = TestcaseDetail


class TestcaseOperationStepsView(ModelViewSet):
    serializer_class = TestcaseOperationStepsSerializer
    queryset = TestcaseOperationSteps


class TestcaseDependenceView(ModelViewSet):
    serializer_class = TestcaseDependenceSerializer
    queryset = TestcaseDependence


class TestcaseFilesView(ModelViewSet):
    serializer_class = TestcaseFilesSerializer
    queryset = TestcaseFiles


class TestcaseCommentsView(ModelViewSet):
    serializer_class = TestcaseCommentsSerializer
    queryset = TestcaseComments


class TestcaseChangeLogsView(ModelViewSet):
    serializer_class = TestcaseChangeLogsSerializer
    queryset = TestcaseChangeLogs
