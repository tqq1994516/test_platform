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


class TestcaseType(IntEnum):
    FUNCTIONAL = 1  # 功能
    INTERFACE = 2  # 接口
    PERFORMANCE = 3  # 性能
    SAFE = 4  # 安全
    OTHER = 99  # 其他


class PriorityType(IntEnum):
    HIGH = 1  # 高
    MIDDLE = 2  # 中
    LOW = 3  # 低


class LevelType(IntEnum):
    L0 = 0  # L0
    L1 = 1  # L1
    L2 = 2  # L2
    L3 = 3  # L3
    L4 = 4  # L4
    L5 = 5  # L5


class ReviewType(IntEnum):
    REVIEWED = 1  # 已评审
    TOREVIEW = 2  # 待评审
    TOEDIT = 3  # 待修改
    INREVIEW = 4  # 评审中
    INEDIT = 5  # 修改中
    DISCARD = 6  # 废弃


class ResultType(IntEnum):
    NOTSTARTED = 1  # 未开始
    EXECUTING = 2  # 执行中
    PENDDING = 3  # 待决策
    BLOCK = 4  # 阻塞
    SKIP = 5  # 跳过
    IGNORE = 6  # 忽略
    PSSS = 7  # 通过
    FAIL = 8  # 失败


class OperationStepType(IntEnum):
    TEXT = 1  # 文本描述
    STEP = 2  # 步骤描述


class TestcaseSites(DataModel):
    name = fields.CharField(50, unique=True, description="用例集名称")
    description = fields.CharField(150, default='', null=True, description="用例集描述")
    project = fields.ForeignKeyField("project_info.ProjectInfo", null=True, description="所属项目")
    priority = fields.IntEnumField(PriorityType, default=2, description="优先级")
    tags = fields.ManyToManyField("system.Tags", description="标签")

    class Meta:
        table = 't_testcase_sites'
        table_description = "用例集信息表"

    def __str__(self):
        return self.name


class Testcases(DataModel):
    name = fields.CharField(50, description="用例名称")
    testcase_type = fields.IntEnumField(TestcaseType, description="用例类型")
    testcase_site = fields.ForeignKeyField("testcase_manager.TestcaseSites", null=True, description="所属用例集")
    priority = fields.IntEnumField(PriorityType, default=2, description="优先级")
    tags = fields.ManyToManyField("system.Tags", description="标签")
    review = fields.IntEnumField(ReviewType, default=2, description="评审状态")
    result = fields.IntEnumField(ResultType, default=1, description="执行状态")
    level = fields.IntEnumField(LevelType, default=0, description="用例级别")
    executors = fields.ManyToManyField("system.Users", through='t_testcase_executors',
                                       related_name="testcase_executors", description="执行人")

    class Meta:
        table = 't_testcases'
        table_description = "用例信息表"

    def __str__(self):
        return self.name


class TestcaseDetail(DataModel):
    testcase = fields.ForeignKeyField("testcase_manager.Testcases", null=True, description="关联用例")
    precondition = fields.TextField(default="", null=True, description="前置条件")
    operation_steps_type = fields.IntEnumField(OperationStepType, description="操作步骤类型")
    operation_steps = fields.TextField(default="", description="文本操作步骤")
    related_testcases = fields.ManyToManyField("testcase_manager.Testcases", through='t_testcase_detail_testcases',
                                               related_name="testcase_detail_testcases", description="关联用例")
    related_tasks = fields.ManyToManyField("third_system.Tasks", through='t_testcase_detail_tasks',
                                           related_name="testcase_detail_tasks", description="关联需求")
    related_bugs = fields.ManyToManyField("third_system.Bugs", through='t_testcase_detail_bugs',
                                          related_name="testcase_detail_bugs", description="关联缺陷")

    class Meta:
        table = 't_testcase_detail'
        table_description = "用例详情表"


class TestcaseOperationSteps(DataModel):
    testcase = fields.ForeignKeyField("testcase_manager.Testcases", null=True, description="关联用例")
    operation_steps = fields.TextField(default='', description="分步操作步骤")
    sort = fields.IntField(default=0, description="排序")

    class Meta:
        table = 't_testcase_operation_steps'
        table_description = "用例操作步骤表"


class TestcaseDependence(DataModel):
    testcase = fields.ForeignKeyField("testcase_manager.Testcases", null=True, description="关联用例")
    is_front = fields.BooleanField(default=True, description="是否前置")
    is_back = fields.BooleanField(default=False, description="是否后置")
    sort = fields.IntField(default=0, description="排序")

    class Meta:
        table = 't_testcase_dependence'
        table_description = "用例关系表"


class TestcaseFiles(DataModel):
    testcase = fields.ForeignKeyField("testcase_manager.Testcases", null=True, description="关联用例")
    file_path = fields.CharField(max_length=200, description="文件地址")

    class Meta:
        table = 't_testcase_files'
        table_description = "用例附件表"


class TestcaseComments(DataModel):
    testcase = fields.ForeignKeyField("testcase_manager.Testcases", null=True, description="关联用例")
    comment = fields.TextField(default='', description="备注")

    class Meta:
        table = 't_testcase_comments'
        table_description = "用例备注表"


class TestcaseChangeLogs(DataModel):
    testcase = fields.ForeignKeyField("testcase_manager.Testcases", null=True, description="关联用例")
    change_field = fields.CharField(max_length=50, description="修改字段")
    before = fields.TextField(default="", description="修改前")
    after = fields.TextField(default="", description="修改后")

    class Meta:
        table = 't_testcase_change_logs'
        table_description = "用例变更历史表"
