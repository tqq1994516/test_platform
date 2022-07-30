import { FormProps } from '/@/components/Table';

export function getFormConfig(): Partial<FormProps> {
  return {
    labelWidth: 100,
    schemas: [
      {
        field: `id`,
        label: `项目ID`,
        component: 'Input',
        colProps: {
          xl: 6,
          xxl: 4,
        },
      },
      {
        field: `name`,
        label: `项目名称`,
        component: 'Input',
        colProps: {
          xl: 6,
          xxl: 4,
        },
      },
      {
        field: `member`,
        label: `项目成员`,
        component: 'ApiSelect',
        colProps: {
          xl: 6,
          xxl: 4,
        },
      },
      {
        field: `master`,
        label: `项目管理员`,
        component: 'ApiSelect',
        colProps: {
          xl: 6,
          xxl: 4,
        },
      },
      {
        field: `owner`,
        label: `创建人`,
        component: 'ApiSelect',
        colProps: {
          xl: 6,
          xxl: 4,
        },
      },
      {
        field: `c_time`,
        label: `创建时间`,
        component: 'RangePicker',
        colProps: {
          xl: 6,
          xxl: 4,
        },
      },
    ],
  };
}