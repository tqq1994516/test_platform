# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import DataModelSerializer

from apps.system.models import *
from srf.fields import SerializerMethodField


class UsersSerializer(DataModelSerializer):
    true_name = SerializerMethodField()

    class Meta(DataModelSerializer.Meta):
        model = Users
        exclude = ('password', 'is_online', 'is_deleted')

    async def get_true_name(self, obj):
        return obj.first_name + obj.last_name


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
