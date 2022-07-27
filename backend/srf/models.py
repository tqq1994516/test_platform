# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:41
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @Project : test_platform
# @Description : baseModels
from tortoise import Model, fields
from tortoise.fields.relational import ManyToManyRelation
from tortoise.queryset import QuerySet
from datetime import datetime


class BaseModel(Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.id

    id = fields.BigIntField(pk=True, default=1, null=False, unique=True, index=True, description="id 主键")
    is_delete = fields.BooleanField(default=False, description="是否删除")
    c_time = fields.DatetimeField(auto_now_add=True, null=True, description='创建时间')
    u_time = fields.DatetimeField(auto_now=True, null=True, description='最后更新时间')

    async def to_dict(self):
        res = {}
        for k in self._meta.fields:
            # fk m2m原始字段不进行返回，time转str
            if isinstance(getattr(self, k), (QuerySet, ManyToManyRelation)):
                continue
            else:
                if isinstance(getattr(self, k), datetime):
                    res[k] = getattr(self, k).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    res[k] = getattr(self, k)
        return res


class DataModel(BaseModel):
    class Meta:
        abstract = True

    owner = fields.ForeignKeyField("system.Users", null=True, description="创建者")
