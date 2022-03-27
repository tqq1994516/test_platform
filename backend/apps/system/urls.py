# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:48
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : urls.py
# @Project : test_platform
# @Description : ...
from srf.routes import ViewSetRouter

from apps.system.views import UsersView, AppsView, GroupsView, RolesView, PermissionsView, TagsView

route = ViewSetRouter(True)
route.register(UsersView, '/users', 'users')
route.register(AppsView, '/apps', 'apps')
route.register(GroupsView, '/groups', 'groups')
route.register(RolesView, '/roles', 'roles')
route.register(PermissionsView, '/permissions', 'permissions')
route.register(TagsView, '/tags', 'tags')
urls = [] + route.urls
