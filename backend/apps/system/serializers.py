# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import ModelSerializer

from apps.system.models import Users, Groups, Roles, Apps, Permissions, Tags


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        read_only_fields = 'id'
        exclude = ('password', 'is_online')


class AppsSerializer(ModelSerializer):
    class Meta:
        model = Apps
        read_only_fields = 'id'


class GroupsSerializer(ModelSerializer):
    class Meta:
        model = Groups
        read_only_fields = 'id'


class RolesSerializer(ModelSerializer):
    class Meta:
        model = Roles
        read_only_fields = 'id'


class PermissionsSerializer(ModelSerializer):
    class Meta:
        model = Permissions
        read_only_fields = 'id'


class TagsSerializer(ModelSerializer):
    class Meta:
        model = Tags
        read_only_fields = 'id'
