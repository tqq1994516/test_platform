# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:22
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : models.py
# @Project : test_platform
# @Description : models file
from dataclasses import dataclass

from tortoise import fields

from common.models import DataModel


@dataclass
class ProjectInfo(DataModel):
    name = fields.CharField(50, description="项目名称")
    description = fields.TextField(description="项目描述")
    masters = fields.ManyToManyField("system.Users", through='t_project_masters', related_name="project_masters", description="管理员")
    members = fields.ManyToManyField("system.Users", through='t_project_members', related_name="project_members", description="项目成员")

    class Meta:
        table = 't_project_info'
        table_description = "项目信息表"

    def __str__(self):
        return self.name


@dataclass
class Envs(DataModel):
    name = fields.CharField(50, description="环境名称")
    description = fields.TextField(description="环境描述")
    domain = fields.CharField(150, description="环境域名")
    project = fields.ForeignKeyField("project_info.ProjectInfo", description="所属项目")

    class Meta:
        table = 't_envs'
        table_description = "运行环境表"

    def __str__(self):
        return self.name


@dataclass
class Versions(DataModel):
    version_num = fields.CharField(50, description="版本号")
    start_time = fields.DatetimeField(null=True, description="开始时间")
    end_time = fields.DatetimeField(null=True, description="结束时间")
    is_activate = fields.BooleanField(default=True, description="是否激活")
    is_newest = fields.BooleanField(default=True, description="是否最新")
    project = fields.ForeignKeyField("project_info.Envs", description="所属项目")

    class Meta:
        table = 't_versions'
        table_description = "软件版本表"

    def __str__(self):
        return self.version_num
