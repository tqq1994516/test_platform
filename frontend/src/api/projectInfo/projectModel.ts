import { BasicListResult } from "../baseModel";

export interface Tag {
  id: number;
  name: string;
  color: string;
}

export interface SimpleUser {
  user_id: number;
  username: string;
}

export interface ProjectInfoModel {
  name: string;
  description: string;
  masters: string[] | number[] | SimpleUser[];
  members: string[] | number[] | SimpleUser[];
  owner: string | number | SimpleUser;
  status: number | string;
  tags: number[] | string[] | Tag[];
  c_time: string;
  u_time: string;
}

export interface ProjectInfoListResult extends BasicListResult {
  results: ProjectInfoModel[];
}