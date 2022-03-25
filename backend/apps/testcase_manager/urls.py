# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:48
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : urls.py
# @Project : test_platform
# @Description : ...
from apps.project_info import PATH, NAME
from srf.routes import ViewSetRouter

from apps.project_info.views import ProjectInfoView, EnvsView, VersionsView

route = ViewSetRouter(True)
route.register(ProjectInfoView, PATH, NAME)
route.register(EnvsView, '/envs', 'envs')
route.register(VersionsView, '/versions', 'versions')
urls = [] + route.urls
