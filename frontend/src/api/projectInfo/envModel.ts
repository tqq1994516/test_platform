import { BasicListResult } from "../baseModel";
import { SimpleUser } from "../sys/model/userModel";
import { SimpleProject } from "./projectModel";

export interface EnvModel {
  name: string;
  owner: string | number | SimpleUser;
  project: string | number | SimpleProject;
  description: string;
  domain: string;
  c_time: string;
  u_time: string;
}

export interface EnvListResult extends BasicListResult {
  results: EnvironmentModel[];
}