import { defHttp } from '/@/utils/http/axios';
import { TagListResult } from './model/tagModel';

enum Api {
  Tags = '/system/tags/',
}

export function getTags(params?: { name: string }) {
    params = {  page: 1, pageSize: 100, ...params, };
    return defHttp.get<TagListResult>({ url: `${Api.Tags}`, params });
  }
