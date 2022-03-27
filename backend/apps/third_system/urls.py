# -*- coding: utf-8 -*-
# @Time : 2022/2/11 13:48
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : urls.py
# @Project : test_platform
# @Description : ...
from srf.routes import ViewSetRouter

from apps.third_system.views import TasksView, BugsView

route = ViewSetRouter(True)
route.register(TasksView, '/tasks', 'tasks')
route.register(BugsView, '/bugs', 'bugs')
urls = [] + route.urls
