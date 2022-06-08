export interface BasicListResult {
  total: number;
  next: string;
  next_page_num: number;
  previous: string;
  previous_num: number;
  results: any[];
}

export interface BasicResult {
  id: number;
  c_time: string|number;
  u_time: string|number;
  owner: string|number;
}