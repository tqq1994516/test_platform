# -*- coding: utf-8 -*-
# @Time : 2022/2/11 11:47
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : views.py
# @Project : test_platform
# @Description : view file
import asyncio
import os
import aiofiles
from datetime import datetime

from sanic.response import file_stream

from settings import EXECUTE_LOG_FOLDER
from srf import ModelViewSet
from apps.testcase_manager.serializers import *


class TestcaseSitesView(ModelViewSet):
    serializer_class = TestcaseSitesSerializer
    queryset = TestcaseSites


class TestcasesView(ModelViewSet):
    serializer_class = TestcasesSerializer
    queryset = Testcases


class TestcaseDetailView(ModelViewSet):
    serializer_class = TestcaseDetailSerializer
    queryset = TestcaseDetail


class TestcaseOperationStepsView(ModelViewSet):
    serializer_class = TestcaseOperationStepsSerializer
    queryset = TestcaseOperationSteps


class TestcaseDependenceView(ModelViewSet):
    serializer_class = TestcaseDependenceSerializer
    queryset = TestcaseDependence


class TestcaseFilesView(ModelViewSet):
    serializer_class = TestcaseFilesSerializer
    queryset = TestcaseFiles


class TestcaseCommentsView(ModelViewSet):
    serializer_class = TestcaseCommentsSerializer
    queryset = TestcaseComments


class TestcaseChangeLogsView(ModelViewSet):
    serializer_class = TestcaseChangeLogsSerializer
    queryset = TestcaseChangeLogs


class TestcaseExecuteRecordsView(ModelViewSet):
    serializer_class = TestcaseExecuteRecordsSerializer
    queryset = TestcaseExecuteRecords


class TestcaseExecuteLogsView(ModelViewSet):
    serializer_class = TestcaseExecuteLogsSerializer
    queryset = TestcaseExecuteLogs

    async def create(self, request, *args, **kwargs):
        execute_log = request.data.pop('execute_log')
        execute_record = request.data['execute_record']
        log_path = EXECUTE_LOG_FOLDER + os.sep + str(execute_record) + '.log'
        with open(log_path, 'w', encoding='utf-8') as log:
            for step in execute_log.values():
                operation_time = datetime.fromtimestamp(int(step['result']['time']/1000)) if step['result'].get('time') else ''
                operation_object = f"'{step['by']}:{step['value']}'" if step['by'] and step['value'] else ''
                operation_action = f"'{step['action']['type']}'"
                operation_action_val = f" value:'{step['action']['value']}'" if step['action'].get('value') else ''
                operation_result = step['result'].get('result')
                if operation_time:
                    line = f"{operation_time} ---- {operation_object} perform {operation_action}{operation_action_val} --- result:{operation_result}."
                else:
                    line = f"{operation_object} perform {operation_action}{operation_action_val} not perform!"
                log.write(line + '\r\n')
        request.data['log_path'] = log_path
        return await super().create(request, *args, **kwargs)


async def testcase_log_read(request):
    log_id = request.data['id'][0]
    log = await TestcaseExecuteLogs.filter(id=log_id).first().values()
    log_path = log['log_path']
    return await file_stream(log_path)


async def testcase_run(request, ws):
    task_name = f"receiver:{request.id}"
    app = request.app
    # app.add_task(test_consumer(request.id), name=task_name)
    try:
        while True:
            message = await ws.recv()
            if not message:
                break
            elif message == '1':
                result = await exec_operation(app, request.id, message, task_name)
                # await ws.send({'result': result})
    except asyncio.CancelledError:
        print(f"{task_name} cancel")
    # finally:
    #     await app.cancel_task(task_name)
    #     app.purge_tasks()


async def exec_operation(app, request_id, message, task_name):
    await app.dispatch(f'testcase.run.ui_test', context={"request_id": request_id, "method": '2', "path": message})
    # await app.event('testcase.result.*')
    # return True
