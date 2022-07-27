<template>
    <div>
        <PageWrapper :title="title" @back="goBack">
            <template #extra>
                <a-button key="1" @click="goEdit" type="primary">编辑</a-button>
            </template>
            <Card title="基础信息" :bordered="false">
                <Description @register="register" />
            </Card>
            <Card title="成员管理" :bordered="false">
                <MemberTable :members.sync="members" />
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
import { descSchemas } from './formData';
import { ref } from 'vue';
import { Description, useDescription } from '/@/components/Description/index';
import { projectInfo } from '/@/api/projectInfo/project/project';

const route = useRoute();
const go = useGo();
const title = ref('项目详情');
const members = ref([])
async function project() {
    const res = await projectInfo(route.params.id);
    for (const member of res.members) {
        members.value.push({name: member.username})
    }
    return res
}

const [register] = useDescription({
    title: title.value,
    schema: descSchemas,
    column: 24,
    data: await project(),

});


// 页面左侧点击返回链接时的操作
function goBack() {
    // 返回项目列表页
    go('/projectInfo/project');
}

function goEdit() {
    go('/projectInfo/project/edit/' + route.params.id);
}
</script>