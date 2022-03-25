# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:13
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : settings.py
# @Project : test_platform
# @Description : project settings
import os

# Web app cofing
from srf.authentication import JWTAuthentication

IS_DEBUG = True
APP_NAME = "test_platform"
HOST = '0.0.0.0'
PORT = 8800
DEBUG = IS_DEBUG
ACCESS_LOG = IS_DEBUG
AUTO_RELOAD = True

# Apps config
AUTO_LOAD_APPS = True
APPS_FOLDER_NAME = 'apps'
APPS_FOLDER_PATH = os.path.join(os.getcwd(), APPS_FOLDER_NAME)
API_VERSION = '1.0.0'

# ORM Config
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_HOST = '121.37.251.10'
DB_PORT = '63306'
DB_NAME = 't_sp'
DB_CONNECT_STR = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Redis Config
REDIS_HOST = '121.37.251.10'
REDIS_PORT = 16379
# REDIS_DATABASE = None
# REDIS_SSL = None
REDIS_ENCODING = "utf-8"
REDIS_DECODE_RESPONSES = True
# REDIS_PASSWORD = ''

# Accessory app config
UPLOAD_PATH = os.path.join(os.getcwd(), 'upload')
OSS_UPLOAD = False
OSS_ID = None
OSS_SECRET = None

# JWT config
SANIC_JWT_AUTHORIZATION_HEADER = JWTAuthentication.keyword
SANIC_JWT_REFRESH_TOKEN_ENABLED = True
SANIC_JWT_SECRET = "U#+ivP*,oCX6}3?WC.6|Y"

CORS_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
]
CORS_ALLOW_HEADERS = [JWTAuthentication.keyword]
