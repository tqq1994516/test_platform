# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:15
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : __init__.py.py
# @Project : test_platform
# @Description : project info model
from sanic.blueprints import Blueprint

from settings import API_VERSION
from apps.project_info.views import ProjectInfoView, EnvsView, VersionsView

# 不可使用驼峰写法
PATH = '/project_info'
NAME = 'project_info'
project_info = Blueprint(NAME, PATH, version=API_VERSION[0])
project_info.add_route(ProjectInfoView.as_view(), '/project_info/<pk:strorempty>',
                       methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
project_info.add_route(EnvsView.as_view(), '/envs/<pk:strorempty>', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
project_info.add_route(VersionsView.as_view(), '/versions/<pk:strorempty>',
                       methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
