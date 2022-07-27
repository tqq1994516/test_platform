import { FormSchema } from '/@/components/Form';
import { ref, h, unref, H } from 'vue';
import { useDebounceFn } from '@vueuse/core';
import { DescItem } from '/@/components/Description/index';
import { Tag } from 'ant-design-vue';
import { getUsers } from '/@/api/sys/user';
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
      { min: 1, max: 120, message: '长度不能大于120', trigger: 'blur' }
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
