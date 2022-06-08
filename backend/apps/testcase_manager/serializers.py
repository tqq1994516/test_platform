# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import DataModelSerializer

from apps.testcase_manager.models import *


class TestcaseSitesSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseSites


class TestcasesSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Testcases


class TestcaseDetailSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseDetail


class TestcaseOperationStepsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseOperationSteps


class TestcaseDependenceSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseDependence


class TestcaseFilesSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseFiles


class TestcaseCommentsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseComments


class TestcaseChangeLogsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseChangeLogs


class TestcaseExecuteRecordsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseExecuteRecords


class TestcaseExecuteLogsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = TestcaseExecuteLogs
