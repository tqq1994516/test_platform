import { BasicListResult } from "../baseModel";
import { SimpleUser } from "../sys/model/userModel";
import { SimpleProject } from "./projectModel";

export interface VersionModel {
  version_num: string;
  is_activate: number;
  is_newest: number;
  owner: string | number | SimpleUser;
  project: string | number | SimpleProject;
  start_time: string;
  end_time: string;
  c_time: string;
  u_time: string;
}

export interface VersionListResult extends BasicListResult {
  results: VersionModel[];
}