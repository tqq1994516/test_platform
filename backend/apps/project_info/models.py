# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:22
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : models.py
# @Project : test_platform
# @Description : models file

from enum import IntEnum
from tortoise import fields

from srf.models import DataModel


class StatusType(IntEnum):
    INIT = 1  # 立项
    LTS = 2  # 长期维护
    PERFECT = 3  # 完善


class ProjectInfo(DataModel):
    name = fields.CharField(50, unique=True, description="项目名称")
    description = fields.TextField(default='', null=True, description="项目描述")
    masters = fields.ManyToManyField("system.Users", through='t_project_masters', related_name="project_masters",
                                     description="管理员")
    members = fields.ManyToManyField("system.Users", through='t_project_members', related_name="project_members",
                                     description="项目成员")
    status = fields.IntEnumField(StatusType, default=1, description="项目状态")
    tags = fields.ManyToManyField("system.Tags", description="标签")

    class Meta:
        table = 't_project_info'
        table_description = "项目信息表"
        depth = 1

    def __str__(self):
        return self.name


class Envs(DataModel):
    name = fields.CharField(50, description="环境名称")
    description = fields.TextField(default='', null=True, description="环境描述")
    domain = fields.CharField(150, unique=True, description="环境域名")
    project = fields.ForeignKeyField("project_info.ProjectInfo", null=True, description="所属项目")

    class Meta:
        table = 't_envs'
        table_description = "运行环境表"

    def __str__(self):
        return self.name


class Versions(DataModel):
    version_num = fields.CharField(50, description="版本号")
    start_time = fields.DatetimeField(null=True, description="开始时间")
    end_time = fields.DatetimeField(null=True, description="结束时间")
    is_activate = fields.BooleanField(default=True, description="是否激活")
    is_newest = fields.BooleanField(default=True, description="是否最新")
    project = fields.ForeignKeyField("project_info.Envs", null=True, description="所属项目")

    class Meta:
        table = 't_versions'
        table_description = "软件版本表"

    def __str__(self):
        return self.version_num
