<template>
    <div>
        <PageWrapper :title="title" @back="goBack">
            <template #extra>
                <a-button key="1" @click="goEdit" type="primary">编辑</a-button>
            </template>
            <Card title="基础信息" :bordered="false">
                <Description @register="register" />
            </Card>
        </PageWrapper>
    </div>
</template>
<script lang="ts" setup>
import { Card } from 'ant-design-vue';
import MemberTable from './viewMemberTable.vue';
import { PageWrapper } from '/@/components/Page';
import { useGo } from '/@/hooks/web/usePage';
import { useRoute } from 'vue-router';
import { descSchemas } from './data';
import { ref } from 'vue';
import { Description, useDescription } from '/@/components/Description/index';
import { version } from '/@/api/projectInfo/version/version';

const route = useRoute();
const go = useGo();
const title = ref('版本详情');
async function versionInfo() {
    return await version(route.params.id);
}

const [register] = useDescription({
    title: title.value,
    schema: descSchemas,
    column: 24,
    data: await versionInfo(),

});


// 页面左侧点击返回链接时的操作
function goBack() {
    // 返回项目列表页
    go('/projectInfo/version');
}

function goEdit() {
    go('/projectInfo/version/edit/' + route.params.id);
}
</script>