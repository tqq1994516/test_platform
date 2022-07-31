import { VersionListResult, VersionModel } from '../versionModel';
import { defHttp } from '/@/utils/http/axios';

enum Api {
  VERSION = '/project_info/envs/',
}

// Get personal center-basic settings

export function versionList() {
  return defHttp.get<VersionListResult>({ url: Api.VERSION }, { joinTime: false });
}


export function version(id: number) {
  return defHttp.get<VersionModel>({ url: `${Api.VERSION}${id}/` });
}

