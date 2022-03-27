import importlib

from tortoise.expressions import Q

from apps import app
from apps.system.models import Permissions, Models, Users
from srf.encryption_algorithm import genearteMD5


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
    superadmin = await Users.filter(username="superadmin").first()
    for name in apps:
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
    superadmin = await Users.filter(username="superadmin").first()
    for app_name, perms in all_perm_dict.items():
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
