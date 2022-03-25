# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import ModelSerializer

from apps.project_info.models import ProjectInfo, Envs, Versions


class ProjectInfoSerializer(ModelSerializer):
    class Meta:
        model = ProjectInfo
        read_only_fields = 'id'


class EnvsSerializer(ModelSerializer):
    class Meta:
        model = Envs
        read_only_fields = 'id'


class VersionsSerializer(ModelSerializer):
    class Meta:
        model = Versions
        read_only_fields = 'id'
