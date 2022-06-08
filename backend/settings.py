# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:13
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : settings.py
# @Project : test_platform
# @Description : project settings
import os


# Web app cofing
from srf.constant import ALL_METHOD

IS_DEV = True
TIME_OUT = 60
APP_NAME = "test_platform"
HOST = '0.0.0.0'
PORT = 8800
DEV = IS_DEV
ACCESS_LOG = IS_DEV
FAST = not IS_DEV
EVENT_AUTOREGISTER = True
KEEP_ALIVE_TIMEOUT = TIME_OUT
REQUEST_TIMEOUT = TIME_OUT
RESPONSE_TIMEOUT = TIME_OUT
OAS_UI_DEFAULT = "swagger"
USER_MODEL = 'apps.system.models.Users'
TTL = 60 * 60 * 8
EXECUTE_LOG_FOLDER = 'execute_log'

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
DB_NAME = APP_NAME
DB_CONNECT_STR = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Redis Config
REDIS_HOST = '121.37.251.10'
REDIS_PORT = 16379
# REDIS_DATABASE = None
# REDIS_SSL = None
REDIS_ENCODING = "utf-8"
REDIS_DECODE_RESPONSES = True
REDIS_PASSWORD = '123456'
REDIS_TTL = TTL
CACHE_REFRESH_PREFIX = "refresh_token_"

# Accessory app config
UPLOAD_PATH = os.path.join(os.getcwd(), 'upload')
OSS_UPLOAD = False
OSS_ID = None
OSS_SECRET = None

# JWT config
SANIC_JWT_REFRESH_TOKEN_ENABLED = True
# SANIC_JWT_EXPIRATION_DELTA = 60 * 10
SANIC_JWT_SECRET = "U#+ivP*,oCX6}3?WC.6|Y"

# cors config
CORS_METHODS = list(ALL_METHOD)

# pulsar config
PULSAR_HOST = '10.10.112.66'
PULSAR_PORT = '6650'
PULSAR_TENANTS = 'pro_used' if not IS_DEV else 'test_used'

# nacos config
NACOS_HOST = '10.10.112.66'
NACOS_PORT = '38848'
NACOS_NAMESPACE = 'test_platform'
