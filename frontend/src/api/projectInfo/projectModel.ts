import { BasicListResult } from "../baseModel";

export interface ProjectInfoModel {
  name: string;
  description: string;
  masters: string[] | number[];
  members: string[] | number[];
  owner: string | number;
  c_time: string;
  u_time: string;
}

export interface ProjectInfoListResult extends BasicListResult {
  results: ProjectInfoModel[];
}