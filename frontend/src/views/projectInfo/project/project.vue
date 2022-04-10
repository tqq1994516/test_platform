<template>
  <BasicTable @register="registerTable">
    <template #action="{ recode }">
      <TableAction :actions="setActions(recode)"></TableAction>
    </template>
  </BasicTable>
</template>
<script lang="ts" setup>
  import { ActionItem, BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from './tableData';
  import TableAction from '/@/components/Table/src/components/TableAction.vue';
  import { projectInfoList } from '/@/api/projectInfo/project/project';
  const [registerTable] = useTable({
    canResize: true,
    title: '项目信息',
    titleHelpMessage: '项目相关信息',
    api: projectInfoList,
    columns: getBasicColumns(),
    defSort: {
      field: 'name',
      order: 'ascend',
    },
    rowKey: 'id',
    showTableSetting: true,
    loading: true,
    rowSelection: {
      type: 'checkbox',
    },
    actionColumn: {
      width: 250,
      title: '操作',
      dataIndex: 'action',
      slots: { customRender: 'action' },
    },
  });
  function viewProject(recode: Recordable) {
    console.log(recode);
  };
  function editProject(recode: Recordable) {
    console.log(recode);
  }
    function delProject(recode: Recordable) {
    console.log(recode);
  }
  function setActions(recode: Recordable): ActionItem[] {
    return [
      { label: '查看', icon: 'carbon:view-filled', divider: true, onClick: viewProject.bind(null, recode) },
      { label: '编辑', icon: 'akar-icons:edit', divider: true, onClick: editProject.bind(null, recode) },
      { label: '删除', icon: 'fluent:delete-16-regular', onClick: delProject.bind(null, recode) },
    ];
  }
</script>
