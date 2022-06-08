# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:15
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : __init__.py.py
# @Project : test_platform
# @Description : third system model
from sanic.blueprints import Blueprint

from apps.third_system.views import *
from settings import API_VERSION

# 不可使用驼峰写法
PATH = '/third_system'
NAME = 'third_system'
third_system = Blueprint(NAME, PATH, version=API_VERSION[0])
third_system.add_route(TasksView.as_view(), '/tasks/<pk:strorempty>', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
third_system.add_route(BugsView.as_view(), '/bugs/<pk:strorempty>', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
