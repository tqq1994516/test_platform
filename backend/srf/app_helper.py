# -*- coding: utf-8 -*-
# @Time : 2022/3/9 17:01
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : app_helper.py
# @Project : backend
# @Description : ...
"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/4/22 9:53
@DependencyLibrary：无
@MainFunction：无
@FileDoc：
    app_helper.py
    文件说明
@ChangeHistory:
    datetime action why
    example:
    2021/4/22 9:53 change 'Fix bug'

"""
from importlib import import_module
from pathlib import Path

from sanic import Sanic
from sanic.log import logger


from srf.constant import LIST_METHOD_GROUP, DETAIL_METHOD_GROUP
from srf.exceptions import AppStructureError, PluginInitializationFailure


def get_module_urls(module_path) -> list:
    """
    得到app中的urls
    :param module_path:
    :return:
    """
    module_path = '%s.urls' % module_path
    try:
        module = import_module(module_path)
    except ModuleNotFoundError:
        return False, None
    return True, getattr(module, 'urls')


def get_module_models(module_path):
    """
    得到app中的models
    :param module_path:
    :return:
    """
    module_path = '%s.models' % module_path
    try:
        import_module(module_path)
    except ModuleNotFoundError:
        return False, None
    return True, module_path


def get_module_blueprint(module_path, module_name):
    """
    得到app的蓝图
    :param module_path:
    :param module_name:
    :return:
    """
    return getattr(import_module(module_path, module_name), module_name)


def set_route(endpoint, route):
    """为urls中的methods提供缺省参数"""
    if 'methods' not in route:
        if 'list' in route['name']:
            route['methods'] = LIST_METHOD_GROUP['static_method']
        elif 'detail' in route['name']:
            route['methods'] = DETAIL_METHOD_GROUP['dynamic_method']
    endpoint.add_route(**route)


def load_route(app, bp, routes):
    """
    循环添加路由到指定端点

    :param app: app实例
    :param bp: 蓝图实例
    :param routes: 路由列表
    """
    for route in routes:
        is_base = route.pop('is_base', False)
        if is_base:
            set_route(app, route)
        else:
            set_route(bp, route)


class AppsHelper:
    """
    一个app应用加载器
    可以方便快捷的加载和管理apps程序
    """

    def __init__(self, instance, *args, **kwargs):
        self.__get_app(instance, *args, **kwargs)

    def __init(self, instance, *args, **kwargs):
        self.apps = {}
        self.routers = []
        self.models = {}

        logger.info('Start load app.')
        config = instance.config
        app_modules = self.get_app_modules(config)

        for module_name, module_path in app_modules.items():
            # 检查app结构
            logger.info('{}Start loading [{}] application.{}'.format('-' * 15, module_name, '-' * 15))
            try:
                blueprint = get_module_blueprint(module_path, module_name)
            except ModuleNotFoundError as exc:
                raise AppStructureError('未找到 %s 程序' % module_path)
            except AttributeError as exc:
                raise AppStructureError('app程序必须包含 __init__.py 模块。')
            self.apps[module_name] = {
                'bp': blueprint,
                'path': Path(import_module(module_path).__file__).parent
            }
            models_exists, models = get_module_models(module_path)
            if models_exists:
                self.models[module_name] = [models]
                logger.info('\t\tModels finish.')
            else:
                logger.warn('\t\tNot find models.')
            instance.blueprint(blueprint)
            logger.info('\t\tRegistered Blueprint finish.')
        logger.info('The {} applications are loaded.'.format(len(app_modules)))
        instance.ctx.apps = self

    def get_app_modules(self, config):
        app_modules = config.get('APP_MODULES', {})
        if not config.AUTO_LOAD_APPS:
            return app_modules
        apps_path = config.APPS_FOLDER_PATH
        folder_paths = Path(apps_path).iterdir()
        for folder_path in folder_paths:
            if (folder_path / '__init__.py').exists():
                app_modules[folder_path.name] = '%s.%s' % (config.APPS_FOLDER_NAME, folder_path.name)
        return app_modules

    def __get_app(self, instance, *args, **kwargs):
        if isinstance(instance, Sanic):
            if not hasattr(instance.ctx, 'apps'):
                self.__init(instance, *args, **kwargs)
            return instance.ctx.apps
        elif instance(instance, AppsHelper):
            return instance
        raise PluginInitializationFailure('app_helper插件初始化异常')
