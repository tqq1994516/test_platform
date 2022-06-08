# -*- coding: utf-8 -*-
# @Time : 2022/2/11 11:47
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : views.py
# @Project : test_platform
# @Description : view file
from srf import ModelViewSet
from apps.third_system.serializers import *


class TasksView(ModelViewSet):
    serializer_class = TasksSerializer
    queryset = Tasks


class BugsView(ModelViewSet):
    serializer_class = BugsSerializer
    queryset = Bugs
