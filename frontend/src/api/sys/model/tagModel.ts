import { BasicListResult } from "../../baseModel";
/**
 * @description: Get user information return value
 */
export interface GetTagModel {
    name: string;
    color: string;
    id: string | number;
    tag_type: string | number;
    description?: string;
    c_time: string;
    u_time: string;
    owner: string | number;
}

export interface TagListResult extends BasicListResult {
    results: GetTagModel[];
  }