# -*- coding: utf-8 -*-
# @Time : 2022/2/11 11:47
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : views.py
# @Project : test_platform
# @Description : view file
from srf import ModelViewSet

from apps.system.models import Users, Apps, Groups, Roles, Permissions
from apps.system.serializers import UsersSerializer, AppsSerializer, GroupsSerializer, RolesSerializer, PermissionsSerializer


class UsersView(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users


class AppsView(ModelViewSet):
    serializer_class = AppsSerializer
    queryset = Apps


class GroupsView(ModelViewSet):
    serializer_class = GroupsSerializer
    queryset = Groups


class RolesView(ModelViewSet):
    serializer_class = RolesSerializer
    queryset = Roles


class PermissionsView(ModelViewSet):
    serializer_class = PermissionsSerializer
    queryset = Permissions
