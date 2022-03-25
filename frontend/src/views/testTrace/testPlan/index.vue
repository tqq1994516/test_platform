<template>
  <BasicTable @register="registerTable" />
</template>

<script lang="ts" setup>
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '../../demo/table/tableData';
  import { demoListApi } from '/@/api/demo/table';
  import { t } from '/@/hooks/web/useI18n';

  const title = t('routes.testTrace.testTrace.title');
  const registerTable = useTable({
    title: title,
    api: demoListApi,
    columns: getBasicColumns(),
  });

  // function changeLoading() {
  //   setLoading(true);
  //   setTimeout(() => {
  //     setLoading(false);
  //   }, 1000);
  // }
</script>
