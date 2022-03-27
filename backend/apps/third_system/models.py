# -*- coding: utf-8 -*-
# @Time : 2022/2/10 18:22
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : models.py
# @Project : test_platform
# @Description : models file

from tortoise import fields

from srf.models import DataModel


class Tasks(DataModel):
    name = fields.CharField(50, description="需求名称")

    class Meta:
        table = 't_tasks'
        table_description = "需求信息表"

    def __str__(self):
        return self.name


class Bugs(DataModel):
    name = fields.CharField(50, description="缺陷名称")

    class Meta:
        table = 't_bugs'
        table_description = "缺陷信息表"

    def __str__(self):
        return self.name
