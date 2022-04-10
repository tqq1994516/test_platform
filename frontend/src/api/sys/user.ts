import { defHttp } from '/@/utils/http/axios';
import { LoginParams, LoginResultModel, GetUserInfoModel, MeInfo } from './model/userModel';

import { ErrorMessageMode } from '/#/axios';

enum Api {
  Login = '/auth',
  Logout = '/auth/logout',
  Verify = '/auth/verify',
  Me = '/auth/me',
  Refresh = '/auth/Refresh',
  GetPermCode = '/system/permissions',
}

/**
 * @description: user login api
 */
export function loginApi(params: LoginParams, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<LoginResultModel>(
    {
      url: Api.Login,
      params,
    },
    {
      errorMessageMode: mode,
      joinPrefix: false,
      isTransformResponse: false
    },
  );
}

/**
 * @description: user login api
 */
export function refreshApi(params: LoginParams, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<LoginResultModel>(
    {
      url: Api.Refresh,
      params,
    },
    {
      errorMessageMode: mode,
      joinPrefix: false,
    },
  );
}

export function getPermCode() {
  return defHttp.get<string[]>({ url: Api.GetPermCode})
}

/**
 * @description: getUserInfo
 */
export function getUserInfo() {
  return defHttp.get<MeInfo>({ url: Api.Me }, { errorMessageMode: 'none', joinPrefix: false, isTransformResponse: false, });
}

export function getVerify() {
  return defHttp.get<GetUserInfoModel>({ url: Api.Verify }, { errorMessageMode: 'none', joinPrefix: false, isTransformResponse: false, });
}

export function doLogout() {
  return defHttp.get({ url: Api.Logout, }, { joinPrefix: false, isTransformResponse: false, });
}

// export function testRetry() {
//   return defHttp.get(
//     { url: Api.TestRetry },
//     {
//       retryRequest: {
//         isOpenRetry: true,
//         count: 5,
//         waitTime: 1000,
//       },
//     },
//   );
// }
