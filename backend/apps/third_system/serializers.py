# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import ModelSerializer

from apps.third_system.models import Tasks, Bugs


class TasksSerializer(ModelSerializer):
    class Meta:
        model = Tasks
        read_only_fields = 'id'


class BugsSerializer(ModelSerializer):
    class Meta:
        model = Bugs
        read_only_fields = 'id'
