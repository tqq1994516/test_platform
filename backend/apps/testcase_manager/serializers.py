# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import ModelSerializer

from apps.testcase_manager.models import TestcaseSites, Testcases, TestcaseDetail, TestcaseOperationSteps, \
    TestcaseDependence, TestcaseFiles, TestcaseComments, TestcaseChangeLogs


class TestcaseSitesSerializer(ModelSerializer):
    class Meta:
        model = TestcaseSites
        read_only_fields = 'id'


class TestcasesSerializer(ModelSerializer):
    class Meta:
        model = Testcases
        read_only_fields = 'id'


class TestcaseDetailSerializer(ModelSerializer):
    class Meta:
        model = TestcaseDetail
        read_only_fields = 'id'


class TestcaseOperationStepsSerializer(ModelSerializer):
    class Meta:
        model = TestcaseOperationSteps
        read_only_fields = 'id'


class TestcaseDependenceSerializer(ModelSerializer):
    class Meta:
        model = TestcaseDependence
        read_only_fields = 'id'


class TestcaseFilesSerializer(ModelSerializer):
    class Meta:
        model = TestcaseFiles
        read_only_fields = 'id'


class TestcaseCommentsSerializer(ModelSerializer):
    class Meta:
        model = TestcaseComments
        read_only_fields = 'id'


class TestcaseChangeLogsSerializer(ModelSerializer):
    class Meta:
        model = TestcaseChangeLogs
        read_only_fields = 'id'
