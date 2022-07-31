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
              <span>未选中任何版本</span>
            </template>
          </template>
        </Alert>
      </template>
      <template #action="{ record }">
        <TableAction :actions="setActions(record)" :dropDownActions="setDropDownActions(record)"></TableAction>
      </template>
      <template #toolbar>
        <a-button type="primary" @click="addVersion">新增</a-button>
        <a-button type="error" @click="batchDelVersion">批量删除</a-button>
      </template>
    </BasicTable>
  </div>
</template>
<script lang="ts" setup>
import { ActionItem, BasicTable, useTable } from '/@/components/Table';
import { getBasicColumns } from './data';
import TableAction from '/@/components/Table/src/components/TableAction.vue';
import { versionList } from '/@/api/projectInfo/version/version';
import { VersionListResult } from '/@/api/projectInfo/versionModel';
import { checkUser } from '/@/utils/auth';
import { UserSimpleState } from '/@/store/modules/user';
import { ref } from 'vue';
import { getFormConfig } from './data';
import { Alert } from 'ant-design-vue';
import { useRouter } from 'vue-router';
// TODO：动态formconfig
// TODO: 后台国际化
const router = useRouter();
const checkedKeys = ref<Array<string | number>>([]);
const [registerTable] = useTable({
  canResize: true,
  clickToRowSelect: false,
  title: '版本信息',
  titleHelpMessage: '版本相关信息',
  api: versionList,
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
function addVersion() {
  router.push({
    name: 'VersionDetail',
    params: { action: 'add' },
  });
}
function batchDelVersion() {
  console.log(checkedKeys.value);
}
function viewVersion(record: Recordable) {
  router.push({
    name: 'VersionDetail',
    params: { id: record.id, action: 'view' },
  });
}
function editVersion(record: Recordable) {
  router.push({
    name: 'VersionDetail',
    params: { id: record.id, action: 'edit' },
  });
}
function delVersion(record: Recordable) {
  console.log(record);
}
function copyVersion(record: Recordable) {
  console.log(record);
}
async function resetUsers(result: VersionListResult): Promise<VersionListResult> {
  // 转换用户信息
  for (const key in result) {
    const user_info = ref<UserSimpleState>({});
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
      onClick: viewVersion.bind(null, record),
    },
    {
      label: '编辑',
      icon: 'akar-icons:edit',
      divider: true,
      onClick: editVersion.bind(null, record),
    },
    {
      label: '删除',
      icon: 'fluent:delete-16-regular',
      popConfirm: {
        title: '确定删除该项目吗？',
        placement: 'left',
        confirm: delVersion.bind(null, record),
      },
    },
  ];
}
function setDropDownActions(record: Recordable): ActionItem[] {
  return [
    {
      label: '复制',
      icon: 'ant-design:copy-filled',
      onClick: copyVersion.bind(null, record),
    }

  ]
}
function onSelectChange(selectedRowKeys: (string | number)[]) {
  checkedKeys.value = selectedRowKeys;
}
</script>
