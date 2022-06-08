# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:36
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : serializers.py
# @Project : test_platform
# @Description : serializer file
from srf import DataModelSerializer

from apps.third_system.models import *


class TasksSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Tasks


class BugsSerializer(DataModelSerializer):
    class Meta(DataModelSerializer.Meta):
        model = Bugs
