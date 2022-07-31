import { projectInfoList } from '/@/api/projectInfo/project';
import { FormProps } from '/@/components/Table';
import { BasicColumn } from '/@/components/Table/src/types/table';
import { FormSchema } from '/@/components/Form';
import { ref, h, unref, H } from 'vue';
import { useDebounceFn } from '@vueuse/core';
import { DescItem } from '/@/components/Description/index';

const colProps = {
  offset: 2,
};
const formColProps = {
  xl: 6,
  xxl: 4,
};
const descSpan = 12;
const tagParams = ref({});
function tagOnSearch(value: string) {
  tagParams.value = {
    name: `@${value}`,
  };
}
const params = ref({});
function onSearch(value: string) {
  params.value = {
    name: `@${value}`,
  };
}

export const schemas: FormSchema[] = [
  {
    field: 'version_num',
    component: 'Input',
    label: '版本号',
    required: true,
    rules: [
      { required: true, message: '请输入版本号', trigger: 'blur' },
      { min: 1, max: 120, message: '长度不能大于50', trigger: 'blur' }
    ]
  },
  {
    field: 'project',
    component: 'ApiSelect',
    label: '关联项目',
    colProps,
    componentProps: {
      filterOption: true,
      maxTagCount: 'responsive',
      showSearch: true,
      resultField: 'results',
      labelField: 'name',
      valueField: 'id',
      params: params,
      allowClear: true,
      onSearch: useDebounceFn(onSearch, 300),
      api: projectInfoList,
    },
  },
  {
    field: 'is_newest',
    component: 'Switch',
    label: '是否最新',
  },
  {
    field: 'is_activate',
    component: 'Switch',
    label: '是否激活',
  },
  {
    field: 'start_time',
    component: 'DatePicker',
    label: '开始时间',
  },
  {
    field: 'end_time',
    component: 'DatePicker',
    label: '结束时间'
  }
];

export const descSchemas: DescItem[] = [
  {
    field: 'version_num',
    label: '版本号',
    span: descSpan,
  },
  {
    field: 'project',
    label: '关联项目',
    span: descSpan,
  },
  {
    field: 'is_newest',
    label: '是否最新',
    span: descSpan,
  },
  {
    field: 'is_activate',
    label: '是否激活',
    span: descSpan,
  }
];

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
      title: '版本号',
      dataIndex: 'version_num',
      width: 250,
      sorter: true,
    },
    {
      title: '关联项目',
      dataIndex: 'project',
      width: 250,
    },
    {
      title: '开始时间',
      dataIndex: 'start_time',
      width: 250,
    },
    {
      title: '结束时间',
      dataIndex: 'end_time',
      width: 250,
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
  return {
    labelWidth: 100,
    schemas: [
      {
        field: `id`,
        label: `版本号ID`,
        component: 'Input',
        colProps: formColProps,
      },
      {
        field: `version_num`,
        label: `版本号`,
        component: 'Input',
        colProps: formColProps,
      },
      {
        field: `project`,
        label: `关联项目`,
        component: 'ApiSelect',
        colProps: formColProps,
        componentProps: {
          filterOption: false,
          showSearch: true,
          resultField: "results",
          labelField: "name",
          valueField: "id",
          params: params,
          allowClear: true,
          onSearch: useDebounceFn(onSearch, 300),
          api: projectInfoList
        },
      },
      {
        field: `is_newest`,
        label: `是否最新`,
        component: 'Checkbox',
        colProps: formColProps,
      },
      {
        field: `is_activate`,
        label: `是否激活`,
        component: 'Checkbox',
        colProps: formColProps,
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
