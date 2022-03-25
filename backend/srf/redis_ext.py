# -*- coding: utf-8 -*-
# @Time : 2022/3/16 16:52
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : redis_ext.py
# @Project : backend
# @Description : ...
from redis import asyncio as aioredis


class BaseExtension(object):

    def __init__(self, app=None, *args, **kwargs):
        self.app = app

        if app:
            # self._register_extension(app, *args, **kwargs)
            self.init_app(app, *args, **kwargs)

    # def _register_extension(self, app, *args, **kwargs):
    #     setattr(app.ctx, self.extension_name, self)
    #     if not hasattr(app.ctx, "extensions"):
    #         app.ctx.extensions = {}
    #     app.ctx.extensions["redis"] = self

    def init_app(self, app, *args, **kwargs):
        pass

    def get_from_app_config(self, app, parameter, default=None):
        return getattr(app.config, parameter, default)


class RedisExtension(BaseExtension):

    def get_config(self, app):
        connection_uri = (
            self.get_from_app_config(app, 'REDIS_HOST'),
            self.get_from_app_config(app, 'REDIS_PORT'),
        )
        config = {
            "url": f"redis://{connection_uri[0]}:{connection_uri[1]}",
            "db": self.get_from_app_config(app, 'REDIS_DATABASE', None),
            "password": self.get_from_app_config(app, 'REDIS_PASSWORD', None),
            "ssl": self.get_from_app_config(app, 'REDIS_SSL', None),
            "encoding": self.get_from_app_config(app, 'REDIS_ENCODING', None),
            "decode_responses": self.get_from_app_config(app, 'REDIS_DECODE_RESPONSES', True)
        }
        return config

    def init_app(self, app, *args, **kwargs):

        @app.before_server_start
        async def aioredis_configure(app_inner, _loop):
            config = self.get_config(app_inner)
            pool = aioredis.ConnectionPool.from_url(config['url'])
            config.pop('url')
            config['connection_pool'] = pool
            redis = aioredis.Redis(connection_pool=pool)
            app_inner.ctx.redis = redis

        @app.after_server_stop
        async def aioredis_free_resources(app_inner, _loop):
            aioredis_pool = app_inner.ctx.redis

            if aioredis_pool:
                await aioredis_pool.close()
