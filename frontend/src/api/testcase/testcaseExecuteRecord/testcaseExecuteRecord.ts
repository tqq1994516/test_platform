import { TestcaseExecuteRecord, TestcaseExecuteRecordParams, TestcaseExecuteLogParams, TestcaseExecuteLogReadParams, TestcaseExecuteLog } from '../testcaseModel';
import { ErrorMessageMode } from '/#/axios';
import { defHttp } from '/@/utils/http/axios';

enum Api {
  MODEL = '/testcase_manager/',
  TESTCASE_EXECUTE_RECORD = 'testcase_execute_records/',
  TESTCASE_EXECUTE_LOG = 'testcase_execute_logs/',
  TESTCASE_EXECUTE_LOG_READ = 'testcase_execute_log_read/'
}

export const addTestcaseExecuteRecord = (params: TestcaseExecuteRecordParams, mode: ErrorMessageMode = 'modal') => {
    return defHttp.post<TestcaseExecuteRecord>({
      url: Api.MODEL + Api.TESTCASE_EXECUTE_RECORD,
      params,
    }, 
    {
      errorMessageMode: mode,
    })
}

export const addTestcaseExecuteLog = (params: TestcaseExecuteLogParams, mode: ErrorMessageMode = 'modal') => {
  return defHttp.post<TestcaseExecuteLog>({
    url: Api.MODEL + Api.TESTCASE_EXECUTE_LOG,
    params,
  },
  {
    errorMessageMode: mode,
  })
}

export const loadTestcaseExecuteLog = (params: TestcaseExecuteLogReadParams,mode: ErrorMessageMode = 'modal') => {
  return defHttp.get({
    url: Api.MODEL + Api.TESTCASE_EXECUTE_LOG_READ,
    responseType: 'arraybuffer',
    params,
  },
  {
    errorMessageMode: mode,
    isTransformResponse: false,
    isReturnNativeResponse: true,
  })
}