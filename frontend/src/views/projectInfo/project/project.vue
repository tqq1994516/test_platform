<template>
  <div>
    <BasicTable @register="registerTable">
      <template #headerTop>
        <Alert type="info" show-icon>
          <template #message>
            <template v-if="checkedKeys.length > 0">
              <span>已选中{{ checkedKeys.length }}条记录(可跨页)</span>
              <a-button type="link" @click="checkedKeys = []" size="small">清空</a-button>
            </template>
            <template v-else>
              <span>未选中任何项目</span>
            </template>
          </template>
        </Alert>
      </template>
      <template #tags="{ record }">
        <span>
          <Tag v-for="tag in record.tags" :key="tag.id" :color="tag.color">{{ tag.name }}</Tag>
        </span>
      </template>
      <template #action="{ record }">
        <TableAction :actions="setActions(record)" :dropDownActions="setDropDownActions(record)"></TableAction>
      </template>
      <template #toolbar>
        <a-button type="primary" @click="addProject">新增</a-button>
        <a-button type="error" @click="batchDelProject">批量删除</a-button>
      </template>
    </BasicTable>
  </div>
</template>
<script lang="ts" setup>
import { ActionItem, BasicTable, useTable } from '/@/components/Table';
import { getBasicColumns } from './data';
import TableAction from '/@/components/Table/src/components/TableAction.vue';
import { projectInfoList } from '/@/api/projectInfo/project/project';
import { ProjectInfoListResult } from '/@/api/projectInfo/projectModel';
import { checkUser } from '/@/utils/auth';
import { useUsersStore, UserSimpleState } from '/@/store/modules/user';
import { ref } from 'vue';
import { getFormConfig } from './data';
import { Alert, Tag } from 'ant-design-vue';
import { useRouter } from 'vue-router';
// TODO：动态formconfig
// TODO: 后台国际化
const usersStore = useUsersStore();
const router = useRouter();
const checkedKeys = ref<Array<string | number>>([]);
const [registerTable] = useTable({
  canResize: true,
  clickToRowSelect: false,
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
  tableSetting: {
    redo: true,
    size: true,
    setting: true,
    fullScreen: true,
  },
  rowSelection: {
    type: 'checkbox',
    selectedRowKeys: checkedKeys,
    onChange: onSelectChange,
  },
  actionColumn: {
    width: 280,
    title: '操作',
    dataIndex: 'action',
    fixed: 'right',
    slots: { customRender: 'action' },
  },
});
function addProject() {
  router.push({
    name: 'ProjectDetail',
    params: { action: 'add' },
  });
}
function batchDelProject() {
  console.log(checkedKeys.value);
}
function viewProject(record: Recordable) {
  router.push({
    name: 'ProjectDetail',
    params: { id: record.id, action: 'view' },
  });
}
function editProject(record: Recordable) {
  router.push({
    name: 'ProjectDetail',
    params: { id: record.id, action: 'edit' },
  });
}
function delProject(record: Recordable) {
  console.log(record);
}
function copyProject(record: Recordable) {
  console.log(record);
}
async function resetUsers(result: ProjectInfoListResult): Promise<ProjectInfoListResult> {
  // 转换用户信息
  for (const key in result) {
    const user_info = ref<UserSimpleState>({});
    for (const master in result[key].masters) {
      await checkUser(result[key].masters[master]['user_id'], user_info);
      result[key].masters[master] = user_info.value['username'];
    }
    for (const member in result[key].members) {
      await checkUser(result[key].members[member]['user_id'], user_info);
      result[key].members[member] = user_info.value['username'];
    }
    await checkUser(result[key].owner['user_id'], user_info);
    result[key].owner = user_info.value['username'];
  }
  return result;
}

function setActions(record: Recordable): ActionItem[] {
  return [
    {
      label: '查看',
      icon: 'carbon:view-filled',
      divider: true,
      onClick: viewProject.bind(null, record),
    },
    {
      label: '编辑',
      icon: 'akar-icons:edit',
      divider: true,
      onClick: editProject.bind(null, record),
    },
    {
      label: '删除',
      icon: 'fluent:delete-16-regular',
      popConfirm: {
        title: '确定删除该项目吗？',
        placement: 'left',
        confirm: delProject.bind(null, record),
      },
    },
  ];
}
function setDropDownActions(record: Recordable): ActionItem[] {
  return [
    {
      label: '复制',
      icon: 'ant-design:copy-filled',
      onClick: copyProject.bind(null, record),
    }

  ]
}
function onSelectChange(selectedRowKeys: (string | number)[]) {
  checkedKeys.value = selectedRowKeys;
}
</script>
