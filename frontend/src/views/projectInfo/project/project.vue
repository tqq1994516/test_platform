<template>
  <BasicTable @register="registerTable">
    <template #headerTop>
      <a-alert type="info" show-icon>
        <template #message>
          <template v-if="checkedKeys.length > 0">
            <span>已选中{{ checkedKeys.length }}条记录(可跨页)</span>
            <a-button type="link" @click="checkedKeys = []" size="small">清空</a-button>
          </template>
          <template v-else>
            <span>未选中任何项目</span>
          </template>
        </template>
      </a-alert>
    </template>
    <template #action="{ record }">
      <TableAction :actions="setActions(record)" :dropDownActions="setDropDownActions(record)"></TableAction>
    </template>
    <template #toolbar>
      <a-button type="primary" @click="getFormValues">新增</a-button>
      <a-button type="error" @click="getFormValues">批量删除</a-button>
    </template>
  </BasicTable>
</template>
<script lang="ts" setup>
import { ActionItem, BasicTable, useTable } from '/@/components/Table';
import { getBasicColumns } from './tableData';
import TableAction from '/@/components/Table/src/components/TableAction.vue';
import { projectInfoList } from '/@/api/projectInfo/project/project';
import { ProjectInfoListResult } from '/@/api/projectInfo/projectModel';
import { getUser } from '/@/api/sys/user';
import { ref } from 'vue';
import { getFormConfig } from './tableData';
var user_list = new Map();
const checkedKeys = ref<Array<string | number>>([]);
const [registerTable] = useTable({
  canResize: true,
  title: '项目信息',
  titleHelpMessage: '项目相关信息',
  api: projectInfoList,
  columns: getBasicColumns(),
  formConfig: getFormConfig(),
  afterFetch: resetUsers,
  useSearchForm: true,
  defSort: {
    field: 'name',
    order: 'ascend',
  },
  rowKey: 'id',
  showTableSetting: true,
  loading: true,
  rowSelection: {
    type: 'checkbox',
    selectedRowKeys: checkedKeys.value,
    onChange: onSelectChange,
  },
  actionColumn: {
    width: 280,
    title: '操作',
    dataIndex: 'action',
    slots: { customRender: 'action' },
  },
});
function viewProject(recode: Recordable) {
  console.log(recode);
}
function editProject(recode: Recordable) {
  console.log(recode);
}
function delProject(recode: Recordable) {
  console.log(recode);
}
function copyProject(recode: Recordable) {
  console.log(recode);
}
async function resetUsers(result: ProjectInfoListResult): Promise<ProjectInfoListResult> {
  for (const key in result) {
    for (const master in result[key].masters) {
      if (!user_list.has(result[key].masters[master])) {
        const { results } = await getUser(result[key].masters[master]);
        console.log(results);
        user_list.set(results[0].id, results[0].username);
      }
      result[key].masters[master] = user_list.get(result[key].masters[master]);
    }
    for (const member in result[key].members) {
      if (!user_list.has(result[key].members[member])) {
        const { results } = await getUser(result[key].members[member]);
        user_list.set(results[0].id, results[0].username);
      }
      result[key].members[member] = user_list.get(result[key].members[member]);
    }
    if (!user_list.has(result[key].owner)) {
      const { results } = await getUser(+result[key].owner);
      user_list.set(results[0].id, results[0].username);
    }
    result[key].owner = user_list.get(result[key].owner);
  }
  return result;
}
function setActions(recode: Recordable): ActionItem[] {
  return [
    {
      label: '查看',
      icon: 'carbon:view-filled',
      divider: true,
      onClick: viewProject.bind(null, recode),
    },
    {
      label: '编辑',
      icon: 'akar-icons:edit',
      divider: true,
      onClick: editProject.bind(null, recode),
    },
    { label: '删除', icon: 'fluent:delete-16-regular', onClick: delProject.bind(null, recode) },
  ];
}
function setDropDownActions(recode: Recordable): ActionItem[] {
  return [
    {
      label: '复制',
      icon: 'ant-design:copy-filled',
      onClick: copyProject.bind(null, recode),
    }

  ]
}
function onSelectChange(selectedRowKeys: (string | number)[]) {
  checkedKeys.value = selectedRowKeys;
}
</script>
