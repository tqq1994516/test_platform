# -*- coding: utf-8 -*-
# @Time : 2022/2/11 17:49
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : __init__.py.py
# @Project : test_platform
# @Description : system model
from sanic.blueprints import Blueprint

from settings import API_VERSION

PATH = '/system'
NAME = 'system'
system = Blueprint(NAME, PATH, version=API_VERSION[0])
