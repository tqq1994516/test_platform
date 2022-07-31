<template>
    <div>
        <PageWrapper :title="title" @back="goBack">
            <Card title="基础信息" :bordered="false">
                <BasicForm @register="register" />
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
import type { SelectProps } from 'ant-design-vue';
import MemberTable from './memberTable.vue';
import { PageWrapper } from '/@/components/Page';
import { useRoute } from 'vue-router';
import { useGo } from '/@/hooks/web/usePage';
import { schemas } from './data';
import { ref, watchEffect } from 'vue';
import { BasicForm, useForm } from '/@/components/Form';
import { version } from '/@/api/projectInfo/version/version';

const route = useRoute();
const title = ref('编辑版本');
const tableRef = ref<{ getDataSource: () => any, setTableData: (data: any) => any } | null>(null);
const mastersOptions = ref<SelectProps['options']>([]);
const tagsOptions = ref<SelectProps['options']>([]);

async function versionInfo() {
    return await version(route.params.id);
}

const [register, { validate, resetFields, setFieldsValue }] = useForm({
    layout: 'vertical',
    baseColProps: {
        span: 6,
    },
    schemas: schemas,
    showActionButtonGroup: false,
});
watchEffect(
    async () => {
        setFieldsValue(await project())
    }
)
function reset() {
    resetFields()
    tableRef.value?.setTableData([])
}
async function submitAll() {
    try {
        if (tableRef.value) {
            console.log('table data:', tableRef.value?.getDataSource());
        }

        const [values] = await Promise.all([validate()]);
        console.log('form data:', values);
    } catch (error) { }
}
const go = useGo();
// 页面左侧点击返回链接时的操作
function goBack() {
    // 返回项目列表页
    go('/projectInfo/version');
}
</script>