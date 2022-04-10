# -*- coding: utf-8 -*-
# @Time : 2022/2/11 17:49
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : __init__.py.py
# @Project : test_platform
# @Description : system model
from sanic.blueprints import Blueprint

from apps.system.views import UsersView, AppsView, GroupsView, RolesView, PermissionsView, TagsView
from settings import API_VERSION

PATH = '/system'
NAME = 'system'
system = Blueprint(NAME, PATH, version=API_VERSION[0])
system.add_route(UsersView.as_view(), '/users/<pk:strorempty>', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
system.add_route(AppsView.as_view(), '/apps/<pk:strorempty>', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
system.add_route(GroupsView.as_view(), '/groups/<pk:strorempty>', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
system.add_route(RolesView.as_view(), '/roles/<pk:strorempty>', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
system.add_route(PermissionsView.as_view(), '/permissions/<pk:strorempty>',
                 methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
system.add_route(TagsView.as_view(), '/tags/<pk:strorempty>', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'POST'])
