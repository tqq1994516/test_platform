<template>
    <PageWrapper title="测试用例详情" subTitle="测试用例编辑/查看" contentBackground @back="() => $router.go(-1)">
        <template #extra>
            <a-button key="1" v-show="status === '编辑'" @click="toggleStatus">{{ status }}</a-button>
            <a-button key="1" v-show="status === '查看'" type="dashed" @click="toggleStatus">{{ status }}</a-button>
            <a-button key="2" type="primary" @click="save">保存</a-button>
            <a-button key="3" type="primary" danger @click="deleteCase">删除用例</a-button>
        </template>
        <template #tags>
            <Tag color="blue">{{ ui_status }}</Tag>
        </template>
        <template #footer>
            <Tabs :defaultActiveKey="tabKey" animated @change="changeTab">
                <TabPane key="1">
                    <template #tab>
                        <Icon icon="entypo:info-with-circle" :size="tabIconSize" />
                        基础
                    </template>
                </TabPane>
                <TabPane key="2">
                    <template #tab>
                        <Icon icon="emojione-v1:window" :size="tabIconSize" />
                        界面
                    </template>
                </TabPane>
                <TabPane key="3">
                    <template #tab>
                        <Icon icon="ant-design:api-twotone" :size="tabIconSize" />
                        接口
                    </template>
                </TabPane>
                <TabPane key="4">
                    <template #tab>
                        <Icon icon="fluent:developer-board-lightning-20-regular" :size="tabIconSize" />
                        性能
                    </template>
                </TabPane>
            </Tabs>
        </template>
        <!-- basic -->
        <div class="p-4" v-show="tabKey === '1'">
            <Card hoverable>
                <template #title>
                    基本信息
                    <Tag color="blue">{{ ui_status }}</Tag>
                </template>
                <BasicForm @register="register" />
            </Card>
        </div>
        <!-- ui -->
        <div v-show="tabKey === '2'">
            <Card hoverable>
                <template #title>
                    通用信息
                    <Tag color="blue">{{ ui_status }}</Tag>
                </template>
                <template #extra>
                    <a-button color="warning" preIcon="ant-design:play-circle-filled" iconSize="16" shape="round">执行
                    </a-button>
                </template>
                <Row justify="start" align="middle" :gutter="[8, 16]">
                    <Col span="4">
                    <Space>
                        总步骤：{{ steps.length }}
                        <Divider type="vertical" />
                        有效步骤：{{ steps.length }}
                    </Space>
                    </Col>
                    <Col span="4">
                    用例变量：<a-button type="dashed" @click="caseVarible">{{ steps.length }}</a-button>
                    </Col>
                    <Col span="4">
                    <Tooltip arrowPointAtCenter>
                        <template #title>开启后每个步骤均进行截图</template>
                        <Icon icon="mdi:tooltip-text" />
                    </Tooltip>
                    性能模式
                    <Switch :checked="checked">
                        <template #checkedChildren>
                            <check-outlined />
                        </template>
                        <template #unCheckedChildren>
                            <close-outlined />
                        </template>
                    </Switch>
                    </Col>
                    <Col span="4">
                    <Tooltip arrowPointAtCenter>
                        <template #title>local执行只支持chrome</template>
                        <Icon icon="ant-design:warning-filled" />
                    </Tooltip>
                    执行浏览器：
                    <Select style="width: 100px" :value="browser" placeholder="请选择浏览器" @change="toggleElementType">
                        <SelectOption value="chrome">chrome</SelectOption>
                        <SelectOption value="firefox">firefox</SelectOption>
                        <SelectOption value="edge">edge</SelectOption>
                    </Select>
                    </Col>
                    <Col span="4">
                    运行模式：
                    <Select style="width: 100px" :value="exec_type" placeholder="请选择执行方式" @change="toggleElementType">
                        <SelectOption value="remote">远程执行</SelectOption>
                        <SelectOption value="local">本地执行</SelectOption>
                    </Select>
                    </Col>
                    <Col span="4">
                    用例全局等待时长：<InputNumber :value="global_timeout" :min="10" :max="300"></InputNumber> 秒
                    </Col>
                    <Col span="4">
                    用例状态：
                    <Select style="width: 100px" :value="ui_status" placeholder="请选择执行方式" @change="toggleElementType">
                        <SelectOption value="init">初始化</SelectOption>
                        <SelectOption value="changes">修改中</SelectOption>
                        <SelectOption value="completed">已完成</SelectOption>
                    </Select>
                    </Col>
                    <Col span="4">
                    <a-button type="primary" preIcon="ic:baseline-insert-page-break" iconSize="16">场景引用</a-button>
                    </Col>
                    <Col span="4">
                    <a-button color="success" preIcon="icon-park-outline:log" iconSize="16">执行记录</a-button>
                    </Col>
                    <Col span="4">
                    <a-button color="error" preIcon="ant-design:file-search-outlined" iconSize="16">变更记录</a-button>
                    </Col>
                </Row>
            </Card>
        </div>
        <CollapseContainer helpMessage="设置操作动作" :loading="loading" @click="loading = false" v-show="tabKey === '2'">
            <template #title>
                测试步骤
            </template>
            <Steps direction="vertical" :current="currentStep">
                <Step v-show="steps.length != 0" v-for="(item, index) in steps" :key="index">
                    <template #title>
                        {{ item }}
                        <Switch :checked="true" checked-children="启用" un-checked-children="禁用"></Switch>
                    </template>
                    <template #subTitle>
                        <Icon v-show="status === '查看'" icon="bi:arrow-bar-up" size="24" @mouseout="colorToGray"
                            @mouseover="colorToRed" :color="delIconColor" @click="delStep(index)">
                        </Icon>
                        <Icon v-show="status === '查看'" icon="bi:arrow-bar-down" size="24" @mouseout="colorToGray"
                            @mouseover="colorToRed" :color="delIconColor" @click="delStep(index)">
                        </Icon>
                        <Icon v-show="status === '查看'" icon="fluent:delete-28-filled" size="24" @mouseout="colorToGray"
                            @mouseover="colorToRed" :color="delIconColor" @click="delStep(index)">
                        </Icon>
                    </template>
                    <template #description>
                        <CollapseContainer helpMessage="设置操作动作" :loading="loading" @click="loading = false">
                            <template #title>
                                基础设置
                            </template>
                            <Row justify="start" align="middle" :gutter="[8, 16]">
                                <Col :span="2">
                                元素类型：
                                </Col>
                                <Col :span="4">
                                <Select style="width: 180px" allowClear placeholder="请选择类型" @change="toggleElementType">
                                    <SelectOption value="public">元素库</SelectOption>
                                    <SelectOption value="custom">自定义</SelectOption>
                                </Select>
                                </Col>
                                <Col v-show="elementType == '元素库'" :span="2">
                                {{ elementType }}：
                                </Col>
                                <Col v-show="elementType == '元素库'" :span="elementSpan">
                                <Cascader allowClear placeholder="请选择元素" changeOnSelect :options="options"
                                    :loadData="loadData"></Cascader>
                                </Col>
                                <Col v-show="elementType == '元素库'" :span="16 - elementSpan">
                                </Col>
                                <Col v-show="elementType == '自定义'" :span="2">
                                定位方式：
                                </Col>
                                <Col v-show="elementType == '自定义'" :span="4">
                                <Select style="width: 180px" allowClear placeholder="请选择方式" @change="toggleElementType">
                                    <SelectOption value="xpath">Xpath</SelectOption>
                                    <SelectOption value="id">Id</SelectOption>
                                </Select>
                                </Col>
                                <Col v-show="elementType == '自定义'" :span="2">
                                定位值：
                                </Col>
                                <Col v-show="elementType == '自定义'" :span="10">
                                <Input placeholder="请输入定位值" allowClear showCount></Input>
                                </Col>
                                <Col :span="2">
                                操作类型：
                                </Col>
                                <Col :span="4">
                                <Select style="width: 180px" allowClear placeholder="请选择操作"
                                    @change="toggleVisibleValue">
                                    <SelectOption value="assert">assert</SelectOption>
                                    <SelectOption value="get">get</SelectOption>
                                    <SelectOption value="click">click</SelectOption>
                                    <SelectOption value="sendKeys">sendKeys</SelectOption>
                                </Select>
                                </Col>
                                <Col v-show="isvisibleValue" :span="2">
                                操作值：
                                </Col>
                                <Col v-show="isvisibleValue" :span="10">
                                <Input placeholder="请输入操作值" allowClear showCount></Input>
                                </Col>
                            </Row>
                            <template #footer>
                                <Row justify="start" align="middle" :gutter="[8, 16]">
                                    <Col :span="2">
                                    快捷模板：
                                    </Col>
                                    <Col :span="2">
                                    <a-button type="primary" @click="">点击</a-button>
                                    </Col>
                                    <Col :span="2">
                                    <a-button type="primary" @click="">输入</a-button>
                                    </Col>
                                    <Col :span="2">
                                    <a-button type="primary" @click="">打开网址</a-button>
                                    </Col>
                                    <Col :span="2">
                                    <a-button type="primary" @click="">切换窗口</a-button>
                                    </Col>
                                </Row>
                            </template>
                        </CollapseContainer>
                        <CollapseContainer helpMessage="设置操作动作" :loading="loading" @click="loading = false">
                            <template #title>
                                高级设置：
                            </template>
                            <Tabs :defaultActiveKey="tabKey" animated>
                                <TabPance key="1">
                                    <template #tab>
                                        元素库
                                    </template>
                                </TabPance>
                                <TabPance key="2">
                                    <template #tab>
                                        前置操作
                                    </template>
                                </TabPance>
                                <TabPance key="3">
                                    <template #tab>
                                        后置操作
                                    </template>
                                </TabPance>
                                <TabPance key="4">
                                    <template #tab>
                                        错误处理
                                    </template>
                                </TabPance>
                                <TabPance key="5">
                                    <template #tab>
                                        其他设置
                                    </template>
                                </TabPance>
                            </Tabs>
                        </CollapseContainer>
                    </template>
                </Step>
                <Step v-show="status === '查看'" title="新增步骤" subTitle="配置步骤操作" description="添加下一步">
                    <template #icon>
                        <span>
                            <Icon icon="carbon:add-filled" :size="36" @click="addStep" />
                        </span>
                    </template>
                </Step>
            </Steps>
        </CollapseContainer>
    </PageWrapper>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import type { CascaderProps } from 'ant-design-vue';
import { InputNumber, Tag, Divider, Tooltip, Switch, Card, CardGrid, Input, Cascader, Row, Col, Select, SelectOption, Steps, Step, Tabs, TabPane } from 'ant-design-vue';
import { CheckOutlined, CloseOutlined } from '@ant-design/icons-vue';
import { CollapseContainer } from '/@/components/Container';
import { BasicForm, FormSchema, useForm } from '/@/components/Form/index';
import { Icon } from '/@/components/Icon';
import { PageWrapper } from '/@/components/Page';
const tabKey = ref("1");
const status = ref("编辑");
const collapseKey = ref("1");
const elementType = ref("元素库");
const tabIconSize = ref(20);
const currentStep = ref(0);
const checked = ref(false);
const isvisibleValue = ref(false);
const steps = ref([{ "1": "step1" }]);
const delIconColor = ref("gray");
const elementSpan = ref(6);
const loadTime = ref(1);
const loading = ref(true);
const changeTab = (activeKey: string) => {
    tabKey.value = activeKey;
}
function addStep() {
    steps.value.push({ "2": "demo" });
    currentStep.value = steps.value.length - 1;
}
function delStep(index: number) {
    steps.value.splice(index, 1);
}
const colorToGray = () => {
    delIconColor.value = "gray"
}
const colorToRed = () => {
    delIconColor.value = "red"
}
function toggleStatus() {
    if (status.value == "编辑") {
        status.value = "查看"
    } else {
        status.value = "编辑"
    }
}
function save() {

}
function deleteCase() {

}
function caseVariable() {
    console.log("variable is clicked");

}
const toggleVisibleValue = (value: string | undefined, option: Option | Array<Option>) => {
    switch (value) {
        case "assert":
        case "click":
        case undefined:
            isvisibleValue.value = false;
            break;
        case "get":
        case "sendKeys":
            isvisibleValue.value = true;
            break;
    }
}
const toggleElementType = (value: string | undefined, option: Option | Array<Option>) => {
    switch (value) {
        case "public":
        case undefined:
            elementType.value = "元素库"
            break;
        case "custom":
            elementType.value = "自定义"
            break;
    }
}
const options = ref<CascaderProps['options']>([
    {
        value: '分组1',
        label: '分组1',
        isLeaf: false,
    },
    {
        value: '分组2',
        label: '分组2',
        isLeaf: false,
    },
]);
const loadData: CascaderProps['loadData'] = selectedOptions => {
    const targetOption = selectedOptions[selectedOptions.length - 1];
    targetOption.loading = true;
}
const browser = ref('chrome');
const exec_type = ref('remote');
const ui_status = ref('init');
const global_timeout = ref(10);
const schemas: FormSchema[] = [
    {
        field: 'name',
        component: 'Input',
        label: '用例名称:',
        colProps: { span: 4 },
    },
    {
        field: 'model',
        component: 'ApiTreeSelect',
        label: '所属模块',
        colProps: { span: 4 },
    },
    {
        field: 'owner',
        component: 'ApiTreeSelect',
        label: '责任人',
        colProps: { span: 4 },
    },
    {
        field: 'level',
        component: 'ApiTreeSelect',
        label: '用例级别',
        colProps: { span: 4 },
    },
    {
        field: 'tags',
        component: 'ApiSelect',
        label: '标签',
        colProps: { span: 8 },
        componentProps: {
            maxTagCount: 'responsive',
        },
        // renderComponentContent: () => {
        //     return {
        //         maxTagPlaceholder: (omittedValues: any[]) => `${omittedValues.length}...`,
        //     }
        // }
    },
    {
        field: 'ui',
        component: 'Switch',
        label: '是否UI用例',
        colProps: { span: 4 },
    },
    {
        field: 'api',
        component: 'Switch',
        label: '是否API用例',
        colProps: { span: 4 },
    },
    {
        field: 'perf',
        component: 'Switch',
        label: '是否性能用例',
        colProps: { span: 4 },
    },
    {
        field: 'desc',
        component: 'InputTextArea',
        label: '用例描述',
        colProps: { span: 24 },
        componentProps: {
            showCount: true,
            maxlength: 500,
            rows: 4,
        }
    }
];
const [registerBase, { setProps, updateSchema, appendSchemaByField, removeSchemaByFiled }] =
    useForm({
        labelWidth: 100,
        schemas,
        actionColOptions: {
            span: 24,
        },
        showActionButtonGroup: false,
    });
</script>