# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:22
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : models.py
# @Project : test_platform
# @Description : models file
from enum import IntEnum
from os import defpath

from tortoise import fields

from srf.models import DataModel


class TagType(IntEnum):
    OTHER = 99  # 其他


class GenderType(IntEnum):
    MALE = 0  # 男
    FEMALE = 1  # 女
    OTHER = 99  # 未知


class Users(DataModel):
    username = fields.CharField(50, unique=True, description="用户名")
    password = fields.CharField(50, description="密码")
    first_name = fields.CharField(50, null=True, description="姓")
    last_name = fields.CharField(50, null=True, description="名")
    mobile = fields.CharField(11, null=True, unique=True, description="手机号")
    email = fields.CharField(50, null=True, description="邮箱")
    gender = fields.IntEnumField(GenderType, default=1, description="性别")
    is_active = fields.BooleanField(default=True, description="是否激活")
    is_online = fields.BooleanField(default=False, description="是否在线")
    apps = fields.ManyToManyField("system.Apps", through="t_users_apps", related_name="users_apps", description="开通应用")
    models = fields.ManyToManyField("system.Models", through="t_users_models", related_name="users_models",
                                    description="开通模块")
    groups = fields.ManyToManyField("system.Groups", through="t_users_groups", related_name="users_groups",
                                    description="用户组")
    is_super_master = fields.BooleanField(default=False, description="是否超管")
    is_system_master = fields.BooleanField(default=False, description="是否管理员")

    class Meta:
        table = 't_users'
        table_description = "用户信息表"

    def __str__(self):
        return self.username

    async def to_dict(self):
        return {"user_id": self.id, "username": self.username, "groups": await self.groups.all().values('id', 'name')}


class Apps(DataModel):
    name = fields.CharField(50, unique=True, description="应用名称")
    description = fields.CharField(150, default='', null=True, description="应用描述")

    class Meta:
        table = "t_apps"
        table_description = "应用信息表"

    def __str__(self):
        return self.name


class Models(DataModel):
    name = fields.CharField(50, unique=True, description="模块名称")
    description = fields.CharField(150, default='', null=True, description="模块描述")

    class Meta:
        table = "t_models"
        table_description = "模块信息表"

    def __str__(self):
        return self.name


class Groups(DataModel):
    name = fields.CharField(50, unique=True, description="用户组名称")
    description = fields.CharField(150, default='', null=True, description="用户组描述")
    roles = fields.ManyToManyField("system.Roles", description="角色")

    class Meta:
        table = "t_groups"
        table_description = "用户组表"

    def __str__(self):
        return self.name


class Roles(DataModel):
    name = fields.CharField(50, unique=True, description="角色名称")
    description = fields.CharField(150, default='', null=True, description="角色描述")
    permissions = fields.ManyToManyField("system.Permissions", description="权限")

    class Meta:
        table = "t_roles"
        table_description = "角色表"

    def __str__(self):
        return self.name


class Permissions(DataModel):
    name = fields.CharField(50, description="权限名称")
    description = fields.CharField(150, default='', null=True, description="权限描述")
    models = fields.ForeignKeyField("system.Models", null=True, description="所属模块")

    class Meta:
        table = "t_permissions"
        table_description = "权限表"

    def __str__(self):
        return self.name


class Tags(DataModel):
    name = fields.CharField(50, unique=True, description="标签名称")
    color = fields.CharField(50, default='red', null=True, description="标签颜色")
    tag_type = fields.IntEnumField(TagType, description="标签类型")
    description = fields.CharField(150, default='', null=True, description="标签描述")

    class Meta:
        table = "t_tags"
        table_description = "标签表"

    def __str__(self):
        return self.name
