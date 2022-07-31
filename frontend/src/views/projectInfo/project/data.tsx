import { getUsers } from '/@/api/sys/user';
import { FormProps } from '/@/components/Table';
import { BasicColumn } from '/@/components/Table/src/types/table';
import { FormSchema } from '/@/components/Form';
import { ref, h, unref, H } from 'vue';
import { useDebounceFn } from '@vueuse/core';
import { DescItem } from '/@/components/Description/index';
import { Tag } from 'ant-design-vue';
import { getTags } from '/@/api/sys/tag';

const colProps = {
  offset: 2,
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
    username: `@${value}`,
  };
}

export const schemas: FormSchema[] = [
  {
    field: 'name',
    component: 'Input',
    label: '项目名称',
    required: true,
    rules: [
      { required: true, message: '请输入项目名称', trigger: 'blur' },
      { min: 1, max: 120, message: '长度不能大于50', trigger: 'blur' }
    ]
  },
  {
    field: 'masters',
    component: 'ApiSelect',
    label: '项目负责人',
    colProps,
    componentProps: {
      filterOption: true,
      mode: 'multiple',
      maxTagCount: 'responsive',
      showSearch: true,
      resultField: 'results',
      labelField: 'username',
      valueField: 'id',
      params: params,
      allowClear: true,
      onSearch: useDebounceFn(onSearch, 300),
      api: getUsers,
    },
  },
  {
    field: 'tags',
    component: 'ApiSelect',
    label: '项目标签',
    colProps,
    componentProps: {
      filterOption: true,
      mode: 'multiple',
      maxTagCount: 'responsive',
      showSearch: true,
      resultField: 'results',
      labelField: 'name',
      valueField: 'id',
      params: tagParams,
      allowClear: true,
      onSearch: useDebounceFn(tagOnSearch, 300),
      api: getTags,
    },
  },
  {
    field: 'description',
    component: 'InputTextArea',
    label: '项目描述',
    colProps: {
      span: 24,
    },
    componentProps: {
      placeholder: '请输入你项目描述',
      rows: 4,
      showCount: true,
    },
  },
];

export const descSchemas: DescItem[] = [
  {
    field: 'name',
    label: '项目名称',
    span: descSpan,
  },
  {
    field: 'masters',
    label: '项目负责人',
    span: descSpan,
    render: (val: any) => {
      const masters = ref('');
      for (const v of val) {
        if (val.length == 1) {
          masters.value = masters.value.concat(v.username)
        } else {
          masters.value = masters.value.concat(v.username, ',')
        }
      }
      return masters.value;
    }
  },
  {
    field: 'tags',
    label: '项目标签',
    render: (val: any) => {
      const tags = ref<H[]>([])
      for (const v of val) {
        tags.value.push(h(Tag, { color: v.color }, v.name))
      }
      return tags.value;
    },
    span: 24,
  },
  {
    field: 'description',
    label: '项目描述',
    span: 24,
  },
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
