import { FormProps, FormSchema } from '/@/components/Table';
import { BasicColumn } from '/@/components/Table/src/types/table';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: 'ID',
      dataIndex: 'id',
      fixed: 'left',
      width: 200,
      sorter: true,
    },
    {
      title: '项目名称',
      dataIndex: 'name',
      width: 150,
      sorter: true,
    },
    {
      title: '项目描述',
      dataIndex: 'description',
    },
    {
      title: '管理员',
      dataIndex: 'masters',
      width: 150,
    },
    {
      title: '项目成员',
      dataIndex: 'members',
      width: 150,
    },
    {
      title: '创建者',
      dataIndex: 'owner',
      width: 50,
      defaultHidden: true,
    },
    {
      title: '创建时间',
      dataIndex: 'c_time',
      width: 150,
      defaultHidden: true,
    },
    {
      title: '最后更新时间',
      dataIndex: 'u_time',
      width: 150,
      defaultHidden: true,
    },
  ];
}

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
        field: `master`,
        label: `项目管理员`,
        component: 'ApiSelect',
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
        field: `c_time`,
        label: `创建时间`,
        component: 'RangePicker',
        colProps: {
          xl: 12,
          xxl: 8,
        },
      },
    ],
  };
}