import { BasicListResult } from "../baseModel";
import { SimpleUser } from "../sys/model/userModel";

export interface Tag {
  id: number;
  name: string;
  color: string;
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

export interface SimpleProject {
  project_id: number;
  name: string;
}