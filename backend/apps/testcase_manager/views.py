# -*- coding: utf-8 -*-
# @Time : 2022/2/11 11:47
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : views.py
# @Project : test_platform
# @Description : view file
from srf import ModelViewSet

from apps.project_info.models import ProjectInfo, Envs, Versions
from apps.project_info.serializers import ProjectInfoSerializer, EnvsSerializer, VersionsSerializer


class ProjectInfoView(ModelViewSet):
    serializer_class = ProjectInfoSerializer
    queryset = ProjectInfo


class EnvsView(ModelViewSet):
    serializer_class = EnvsSerializer
    queryset = Envs


class VersionsView(ModelViewSet):
    serializer_class = VersionsSerializer
    queryset = Versions
