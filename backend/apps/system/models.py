# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:22
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : models.py
# @Project : test_platform
# @Description : models file
from dataclasses import dataclass
from enum import IntEnum

from tortoise import fields

from common.models import DataModel


class TagType(IntEnum):
    OTHER = 99  # 其他


@dataclass
class Users(DataModel):
    username = fields.CharField(50, description="用户名")
    password = fields.CharField(50, description="密码")
    first_name = fields.CharField(50, null=True, description="姓")
    last_name = fields.CharField(50, null=True, description="名")
    mobile = fields.CharField(11, null=True, description="手机号")
    email = fields.CharField(50, null=True, description="邮箱")
    is_active = fields.BooleanField(default=True, description="是否激活")
    is_online = fields.BooleanField(default=False, description="是否在线")
    apps = fields.ManyToManyField("system.Apps", through="t_users_apps", related_name="users_apps", description="开通模块")
    groups = fields.ManyToManyField("system.Groups", through="t_users_groups", related_name="users_apps", description="用户组")
    is_super_master = fields.BooleanField(default=False, description="是否超管")
    is_system_master = fields.BooleanField(default=False, description="是否管理员")

    class Meta:
        table = 't_users'
        table_description = "用户信息表"

    def __str__(self):
        return self.username


@dataclass
class Apps(DataModel):
    name = fields.CharField(50, description="应用名称")
    description = fields.CharField(150, description="应用描述")

    class Meta:
        table = "t_apps"
        table_description = "应用信息表"

    def __str__(self):
        return self.name


@dataclass
class Groups(DataModel):
    name = fields.CharField(50, description="用户组名称")
    description = fields.CharField(150, description="用户组描述")
    roles = fields.ManyToManyField("system.Roles", description="角色")

    class Meta:
        table = "t_groups"
        table_description = "用户组表"

    def __str__(self):
        return self.name


@dataclass
class Roles(DataModel):
    name = fields.CharField(50, description="角色名称")
    description = fields.CharField(150, description="角色描述")
    permission = fields.ManyToManyField("system.Permissions", description="权限")

    class Meta:
        table = "t_roles"
        table_description = "角色表"

    def __str__(self):
        return self.name


@dataclass
class Permissions(DataModel):
    name = fields.CharField(50, description="权限名称")
    description = fields.CharField(150, description="权限描述")
    is_view = fields.BooleanField(default=True, description="是否允许查看")
    is_add = fields.BooleanField(default=True, description="是否允许新增")
    is_edit = fields.BooleanField(default=True, description="是否允许编辑")
    is_del = fields.BooleanField(default=True, description="是否允许删除")

    class Meta:
        table = "t_permissions"
        table_description = "权限表"

    def __str__(self):
        return self.name


@dataclass
class Tags(DataModel):
    name = fields.CharField(50, description="标签名称")
    tag_type = fields.IntEnumField(TagType, description="标签类型")
    description = fields.CharField(150, description="标签描述")

    class Meta:
        table = "t_tags"
        table_description = "标签表"

    def __str__(self):
        return self.name
