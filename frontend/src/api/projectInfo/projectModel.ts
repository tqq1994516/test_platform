import { BasicListResult } from "../baseModel";

export interface ProjectInfoModel {
  name: string;
  description: string;
  masters: string[];
  members: string[];
  owner: string;
  c_time: string;
  u_time: string;
}

export interface ProjectInfoListResult extends BasicListResult {
  results: ProjectInfoModel[];
}