# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:41
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @Project : test_platform
# @Description : baseModels
from tortoise import Model, fields


class BaseModel(Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.id

    id = fields.BigIntField(pk=True, default=1, null=False, unique=True, index=True, description="id 主键")
    c_time = fields.DatetimeField(auto_now_add=True, null=True, description='创建时间')
    u_time = fields.DatetimeField(auto_now=True, null=True, description='最后更新时间')


class DataModel(BaseModel):
    class Meta:
        abstract = True

    owner = fields.ForeignKeyField("system.Users", null=True, description="创建者")
