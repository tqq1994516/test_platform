# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import DataModelSerializer

from apps.system.models import *


class UsersSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Users
        exclude = ('password', 'is_online', 'is_deleted')


class AppsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Apps


class GroupsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Groups


class RolesSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Roles


class PermissionsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Permissions


class TagsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Tags
