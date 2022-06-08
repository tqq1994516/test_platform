import { BasicResult } from "../baseModel";


export interface TestcaseExecuteRecordParams {
    testcase: number;
    execute_time: number;
    execute_result: string;
    execute_type: number;
}

export interface TestcaseExecuteLogParams {
    testcase: number;
    execute_record: number;
    execute_log: any;
}

export interface TestcaseExecuteLogReadParams {
    id: number;
}

export interface TestcaseExecuteRecord extends BasicResult {
    testcase: number;
    execute_time: string|number;
    execute_result: string;
    execute_type: number;
}

export interface TestcaseExecuteLog extends BasicResult {
    id: number;
    testcase: number;
    execute_record: number;
    log_path: string;
}