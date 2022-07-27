<template>
  <div>
    <BasicTable @register="registerTable">
    </BasicTable>
  </div>
</template>
<script lang="ts" setup>
import {
  BasicTable,
  useTable,
  BasicColumn,
} from '/@/components/Table';
import { unref } from 'vue';
const props = defineProps<{
  members: any[],
}>();

const columns: BasicColumn[] = [
  {
    title: '成员姓名',
    dataIndex: 'name',
  },
];
const [registerTable] = useTable({
  columns: columns,
  showIndexColumn: false,
  pagination: false,
  dataSource: unref(props.members),
});
</script>
