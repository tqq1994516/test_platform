import { getUsers } from '/@/api/sys/user';
import { ref } from 'vue';
import { FormProps } from '/@/components/Table';
import { BasicColumn } from '/@/components/Table/src/types/table';
import { useDebounceFn } from '@vueuse/core';

export function getBasicColumns(): BasicColumn[] {
  return [
    {
      title: 'ID',
      dataIndex: 'id',
      fixed: 'left',
      width: 80,
      sorter: true,
    },
    {
      title: '项目名称',
      dataIndex: 'name',
      width: 250,
      sorter: true,
    },
    {
      title: '项目描述',
      dataIndex: 'description',
    },
    {
      title: '项目标签',
      dataIndex: 'tags',
      width: 200,
      slots: { customRender: 'tags' },
    },
    {
      title: '项目状态',
      dataIndex: 'status',
      width: 80,
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
      width: 100,
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
  const params = ref({});
  function onSearch(value: string) {
    params.value = {
      "username": `@${value}`,
    }
  }
  
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
        componentProps: {
          filterOption: false,
          showSearch: true,
          resultField: "results",
          labelField: "username",
          valueField: "id",
          params: params,
          allowClear: true,
          onSearch: useDebounceFn(onSearch, 300),
          api: getUsers
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
        componentProps: {
          filterOption: false,
          showSearch: true,
          resultField: "results",
          labelField: "username",
          valueField: "id",
          params: params,
          allowClear: true,
          onSearch: useDebounceFn(onSearch, 300),
          api: getUsers
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
