# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import DataModelSerializer

from apps.project_info.models import *


class ProjectInfoSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = ProjectInfo


class EnvsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Envs


class VersionsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Versions
