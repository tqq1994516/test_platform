<template>
  <div>
    <BasicTable @register="registerTable">
      <template #action="{ record, column }">
        <TableAction :actions="createActions(record, column)" />
      </template>
    </BasicTable>
    <a-button block class="mt-5" type="dashed" @click="handleAdd"> 新增成员 </a-button>
  </div>
</template>
<script lang="ts" setup>
import {
  BasicTable,
  useTable,
  TableAction,
  BasicColumn,
  ActionItem,
  EditRecordRow,
} from '/@/components/Table';
import { getUsers } from '/@/api/sys/user';
import { ref, unref } from 'vue';
import { useDebounceFn } from '@vueuse/core';
const props = defineProps<{
  members?: any[],
}>();
const params = ref({});
function onSearch(value: string) {
  params.value = {
    username: `@${value}`,
  };
}
const columns: BasicColumn[] = [
  {
    title: '成员姓名',
    dataIndex: 'name',
    editRow: true,
    editComponent: 'ApiSelect',
    editComponentProps: {
      filterOption: false,
      showSearch: true,
      resultField: 'results',
      labelField: 'username',
      valueField: 'id',
      params: params,
      allowClear: true,
      immediate: false,
      onSearch: useDebounceFn(onSearch, 300),
      api: getUsers,
    },
  },
];

const [registerTable, { getDataSource, deleteTableDataRecord, setTableData }] = useTable({
  columns: columns,
  showIndexColumn: false,
  actionColumn: {
    width: 160,
    title: '操作',
    dataIndex: 'action',
    slots: { customRender: 'action' },
  },
  pagination: false,
  dataSource: unref(props.members),
});
defineExpose({ getDataSource, setTableData })
function delMember(record: EditRecordRow) {
  deleteTableDataRecord(record.key)
}
function saveMember(record: EditRecordRow) {
  record.onEdit?.(false, true);
}
function handleAdd() {
  const addRow: EditRecordRow = {
    name: '',
    editable: true,
    isNew: true,
    key: `${Date.now()}`,
  };
  const data = getDataSource();
  data.push(addRow);
  setTableData(data);
}
function createActions(record: EditRecordRow, column: BasicColumn): ActionItem[] {
  if (!record.editable) {
    return [
      {
        label: '删除',
        icon: 'fluent:delete-16-regular',
        popConfirm: {
          title: '确定删除该项目吗？',
          placement: 'left',
          confirm: delMember.bind(null, record),
        },
      },
    ];
  }
  return [
    {
      label: '保存',
      icon: 'bx:save',
      onClick: saveMember.bind(null, record),
    },
    {
      label: '删除',
      icon: 'fluent:delete-16-regular',
      popConfirm: {
        title: '确定删除该项目吗？',
        placement: 'left',
        confirm: delMember.bind(null, record),
      },
    },
  ];
}
</script>
