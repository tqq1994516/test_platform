# -*- coding: utf-8 -*-
# @Time : 2022/2/11 11:47
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : views.py
# @Project : test_platform
# @Description : view file
from tortoise.expressions import Q

from srf import ModelViewSet, GenericViewSet

from apps.system.models import Users, Apps, Groups, Roles, Permissions, Tags
from apps.system.serializers import UsersSerializer, AppsSerializer, GroupsSerializer, RolesSerializer, \
    PermissionsSerializer, TagsSerializer, LoginSerializer
from srf.encryption_algorithm import genearteMD5
from srf.status import HttpStatus


class UsersView(ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users


class LoginView(GenericViewSet):
    serializer_class = LoginSerializer
    queryset = Users

    async def post(self, request, *args, **kwargs):
        request.data['password'] = genearteMD5(request.data['password'])
        serializer = self.get_serializer(data=request.data)
        await serializer.is_valid(raise_exception=True)
        users = await self.get_queryset()
        u = await users.filter(
            Q(username=serializer._validated_data['username']) & Q(password=serializer._validated_data['password']))
        if u:
            u.
            await users.update_from_dict()
            return self.success_json_response(msg="登录成功！", data=u.username)

    async def get(self, request, *args, **kwargs):
        instance = await self.get_object()
        serializer = self.get_serializer(instance)
        return self.success_json_response(msg="查询成功！", data=await serializer.data)


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


class TagsView(ModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tags
