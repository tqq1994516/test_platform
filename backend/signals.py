import importlib
import json
import os
from srf.nacos_ext.nacos_plugin import nacos_client
from tasks import nacos_beat

from tortoise.expressions import Q

from apps import app
from apps.system.models import Permissions, Models, Users, Roles, Groups
from settings import *
from srf.encryption_algorithm import genearteMD5
from srf.mq_ext.pulsar_plugin import pulsar_producer, UiSelectorSchema


def collection_permissions():
    app_models = {}
    for app_name, module_path in app.ctx.apps.models.items():
        app_models[app_name] = []
        classes = importlib.import_module(module_path[0])
        for c in dir(classes):
            if c[0].isupper() and 'Type' not in c and c != 'DataModel' and c != 'IntEnum':
                app_models[app_name].append(c)
    model_permissions = {}
    for app_name, module_name in app_models.items():
        model_permissions[app_name] = []
        for m in module_name:
            model_permissions[app_name].append("view_" + m)
            model_permissions[app_name].append("add_" + m)
            model_permissions[app_name].append("edit_" + m)
            model_permissions[app_name].append("del_" + m)
    return model_permissions


@app.before_server_start
async def prepare_run_env(app, loop):
    if not os.path.exists(EXECUTE_LOG_FOLDER):
        os.makedirs(EXECUTE_LOG_FOLDER)


@app.before_server_start
async def create_superadmin(app, loop):
    if not await Users.exists(username="superadmin"):
        superadmin = {
            "username": "superadmin",
            "password": "123456",
            "is_super_master": True,
            "is_system_master": True
        }
        superadmin['password'] = genearteMD5(superadmin['password'])
        user = await Users.create(**superadmin)


@app.before_server_start
async def load_model(app, loop):
    """在服务器启动时加载model"""
    apps = app.ctx.apps.apps.keys()
    for name in apps:
        superadmin = await Users.filter(username="superadmin").first()
        if not await Models.exists(name=name):
            model = {
                "name": name,
                "description": name + " model",
                "owner": superadmin
            }
            models = await Models.create(**model)


@app.before_server_start
async def load_permission(app, loop):
    """在服务器启动时加载权限"""
    all_perm_dict = collection_permissions()
    for app_name, perms in all_perm_dict.items():
        superadmin = await Users.filter(username="superadmin").first()
        pk = await Models.filter(name=app_name).first()
        for p in perms:
            if not await Permissions.exists(Q(models=pk.id) & Q(name=p)):
                p_temp = p.split('_')
                permission = {
                    "name": p,
                    "description": "can " + p_temp[0] + " " + p_temp[1],
                    "models": pk,
                    "owner": superadmin
                }
                perm = await Permissions.create(**permission)


@app.before_server_start
async def load_role(app, loop):
    """在服务器启动时加载角色"""
    if not await Roles.exists(name='superadmin'):
        superadmin = await Users.filter(username="superadmin").first()
        permissions = await Permissions.all()
        role = {
            "name": "superadmin",
            "description": "超级管理员",
            "owner": superadmin
        }
        roles = await Roles.create(**role)
        await roles.permissions.add(*permissions)


@app.before_server_start
async def load_group(app, loop):
    """在服务器启动时加载用户组"""
    if not await Groups.exists(name='superadminGroup'):
        superadmin = await Users.filter(username="superadmin").first()
        superrole = await Roles.filter(name='superadmin')
        group = {
            "name": "superadminGroup",
            "description": "超级管理员组",
            "owner": superadmin
        }
        groups = await Groups.create(**group)
        await groups.roles.add(*superrole)


@app.before_server_start
async def update_superadmin_info(app, loop):
    """在服务器启动时加载用户组"""
    superadmin = await Users.filter(username="superadmin").first()
    supergroup = await Groups.filter(name="superadminGroup")
    await superadmin.groups.add(*supergroup)


# @app.before_server_start
async def create_nacose_service(app, loop):
    """在服务器启动时初始化nacos命名空间、服务及实例并开始后台beat"""
    res = nacos_client.get_namespace()[0]
    namespace_exists = False
    if res['code'] == 200:
        for namespace in res['data']:
            if namespace['namespace'] == NACOS_NAMESPACE:
                namespace_exists = True
                break
            else:
                continue
    else:
        raise Exception("get namespace error")
    if not namespace_exists:
        res = nacos_client.create_namespace(NACOS_NAMESPACE, NACOS_NAMESPACE, "test platform")[0]
        if not res:
            raise Exception("create namespace error")
    res = nacos_client.get_service(NACOS_NAMESPACE, NACOS_SERVICENAME, groupName=NACOS_GROUP)[0]
    if 'service not found' in res:
        res = nacos_client.create_service(NACOS_SERVICENAME, namespaceId=NACOS_NAMESPACE, groupName=NACOS_GROUP)[0]
        if 'ok' not in res:
            raise Exception("create service error")
    await create_nacose_instance()


async def create_nacose_instance():
    ip = '192.168.145.128'
    res = nacos_client.register_instance(ip, PORT, NACOS_SERVICENAME, namespaceId=NACOS_NAMESPACE, groupName=NACOS_GROUP, enabled=True, healthy=True, ephemeral=NACOS_EPHEMERAL)[0]
    if 'ok' not in res:
        raise Exception("create instance error")
    await send_nacos_beat(NACOS_SERVICENAME, beat={"ip": ip, "port": PORT}, groupName=NACOS_GROUP, ephemeral=NACOS_EPHEMERAL)


# @app.before_server_start
async def create_nacose_config(app, loop):
    """在服务器启动时将mysql及redis共享至nacos配置"""
    res = nacos_client.get_config('redis', NACOS_GROUP, NACOS_NAMESPACE)[0]
    if 'config data not exist' in res:
        res = nacos_client.publish_config('redis', NACOS_GROUP, {"host": REDIS_HOST, "port": REDIS_PORT, "password": REDIS_PASSWORD}, NACOS_NAMESPACE)
        if res['code'] != 200:
            raise Exception("create config error")
    res = nacos_client.get_config('mysql', NACOS_GROUP, NACOS_NAMESPACE)[0]
    if 'config data not exist' in res:
        res = nacos_client.publish_config('mysql', NACOS_GROUP, {"host": DB_HOST, "port": DB_NAME, "username": DB_USER, "password": REDIS_PASSWORD, "db": DB_NAME}, NACOS_NAMESPACE)
        if res['code'] != 200:
            raise Exception("create config error")

async def send_nacos_beat(
    serviceName: str,
    beat: dict,
    groupName: str = None,
    ephemeral: bool = None
):
    """_summary_

    Args:
        serviceName (str): 服务名称
        beat (dict): 心跳信息
        groupName (str, optional): 组名称. Defaults to None.
        ephemeral (bool, optional): 是否临时实例. Defaults to None.
    """
    app.add_task(nacos_beat(serviceName, beat, groupName, ephemeral), name='nacos_heartbeat')


@app.signal('testcase.run.<exec>')
async def my_custom_action(exec, **context):
    """
    自定义信号
    :param exec:
    :param context:
    :return:
    """
    context['request_id'] = str(context['request_id'])
    pulsar_producer(f'{exec=}', message=UiSelectorSchema(**context))


@app.signal('testcase.result.<status>')
def my_custom_action(status, **context):
    """
    自定义信号
    :param status:
    :param context:
    :return:
    """
    print(status)
    print(context)
