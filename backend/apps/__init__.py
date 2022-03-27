# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:12
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : __init__.py.py
# @Project : test_platform
# @Description : ...
import importlib
import logging
from pathlib import Path

from sanic import Sanic
from sanic_babel import Babel
from sanic_jwt import Initialize
from tortoise.contrib.sanic import register_tortoise

from srf.redis_tool import set_value, get_value
from srf.app_helper import AppsHelper
from srf.request import SRFRequest
from srf.authentication import JWTAuthentication
from srf.redis_ext import RedisExtension
from settings import APP_NAME, API_VERSION

logging.basicConfig(filename="access.log")

config_name = 'settings.py'
cfg_name = 'translation_config.cfg'


def create_app():
    """工厂函数"""
    sanic_app = Sanic(name=APP_NAME, request_class=SRFRequest)
    sanic_app.update_config(Path.cwd() / config_name)
    sanic_app.update_config(Path.cwd() / cfg_name)
    Babel(sanic_app, configure_jinja=False)
    AppsHelper(sanic_app)
    RedisExtension(sanic_app)

    def store_refresh_token(user_id, refresh_token, *args, **kwargs):
        key = f'refresh_token_{user_id}'
        set_value(sanic_app.ctx.redis, key, refresh_token)

    def retrieve_refresh_token(request, user_id, *args, **kwargs):
        key = f'refresh_token_{user_id}'
        return get_value(sanic_app.ctx.redis, key)

    Initialize(sanic_app, authenticate=JWTAuthentication.authenticate, store_refresh_token=store_refresh_token,
               retrieve_refresh_token=retrieve_refresh_token)
    register_tortoise(
        sanic_app, db_url=sanic_app.config.get('DB_CONNECT_STR'), modules=sanic_app.ctx.apps.models
        , generate_schemas=True
    )
    return sanic_app


app = create_app()
app.ext.openapi.describe(APP_NAME + " API", version=API_VERSION, description='用以web查看调试系统api')

# 此为迁移配置
TORTOISE_ORM = {
    "connections": {"default": app.config.get('DB_CONNECT_STR')},
    "apps": {
        "models": {
            "models": ['aerich.models'],
            "default_connection": "default",
        },
    },
}
for name, val in app.ctx.apps.models.items():
    TORTOISE_ORM['apps'][name] = {
        "models": val,
        "default_connection": "default",
    }

# 延时加载
importlib.import_module('signals')
