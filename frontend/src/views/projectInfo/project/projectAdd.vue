<template>
    <div>
        <PageWrapper :title="title" @back="goBack">
            <Card title="基础信息" :bordered="false">
                <BasicForm @register="register" />
            </Card>
            <Card title="成员管理" :bordered="false">
                <MemberTable ref="tableRef" :members="members" />
            </Card>
            <template #rightFooter>
                <Space>
                    <a-button @click="reset">重置</a-button>
                    <a-button type="primary" @click="submitAll"> 提交 </a-button>
                </Space>
            </template>
        </PageWrapper>
    </div>
</template>
<script lang="ts" setup>
// TODO: validate
import { Card, Space } from 'ant-design-vue';
import MemberTable from './memberTable.vue';
import { PageWrapper } from '/@/components/Page';
import { useGo } from '/@/hooks/web/usePage';
import { schemas } from './formData';
import { ref } from 'vue';
import { BasicForm, useForm } from '/@/components/Form';

const title = ref('新增项目');
const members = ref([])
const tableRef = ref<{ getDataSource: () => any, setTableData: (data: any) => any } | null>(null);

const [register, { validate, resetFields }] = useForm({
    layout: 'vertical',
    baseColProps: {
        span: 6,
    },
    schemas: schemas,
    showActionButtonGroup: false,
});

async function submitAll() {
    try {
        if (tableRef.value) {
            console.log('table data:', tableRef.value.getDataSource());
        }

        const [values] = await Promise.all([validate()]);
        console.log('form data:', values);
    } catch (error) { }
}
function reset() {
    resetFields()
    tableRef.value?.setTableData([])
}
const go = useGo();
// 页面左侧点击返回链接时的操作
function goBack() {
    // 返回项目列表页
    go('/projectInfo/project');
}
</script>