import { BasicListResult } from "../../baseModel";

/**
 * @description: Login interface parameters
 */
export interface LoginParams {
  username: string;
  password: string;
}

export interface GroupInfo {
  id: number;
  name: string;
}

/**
 * @description: Login interface return value
 */
export interface LoginResultModel {
  access_token: string;
  refresh_token: string;
}

/**
 * @description: Get user information return value
 */
export interface GetUserInfoModel {
  groups: GroupInfo[];
  // 用户id
  id: string | number;
  // 用户名
  username: string;
  // 真实名字
  realName?: string;
  // 头像
  avatar?: string;
  // 介绍
  desc?: string;
}

export interface MeInfo {
  me: GetUserInfoModel;
}

export interface UserInfoListResult extends BasicListResult {
  results: GetUserInfoModel[];
}

export interface SimpleUser {
  user_id: number;
  username: string;
}