import { ProjectInfoListResult, ProjectInfoModel } from '../projectModel';
import { defHttp } from '/@/utils/http/axios';

enum Api {
  PROJECT_INFO = '/project_info/project_info/',
}

// Get personal center-basic settings

export const projectInfoList = () =>
  defHttp.get<ProjectInfoListResult>({ url: Api.PROJECT_INFO }, { joinTime: false });
