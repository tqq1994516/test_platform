<template>
  <PageWrapper title="WebSocket 示例">
    <div class="flex">
      <div class="w-1/3 bg-white p-4">
        <div class="flex items-center">
          <span class="text-lg font-medium mr-4"> 连接状态: </span>
          <Tag :color="getTagColor">{{ status }}</Tag>
        </div>
        <hr class="my-4" />

        <div class="flex">
          <a-input v-model:value="server" disabled>
            <template #addonBefore> 服务地址 </template>
          </a-input>
          <a-button :type="getIsOpen ? 'danger' : 'primary'" @click="toggle">
            {{ getIsOpen ? '关闭连接' : '开启连接' }}
          </a-button>
        </div>
        <p class="text-lg font-medium mt-4">设置</p>
        <hr class="my-4" />

        <InputTextArea placeholder="需要发送到服务器的内容" :disabled="!getIsOpen" v-model:value="sendValue" allowClear />
        <a-button type="primary" block class="mt-4" :disabled="!getIsOpen" @click="handlerSend">
          发送
        </a-button>
        <a-button type="primary" block class="mt-4" @click="perviewLog">
          查看日志
        </a-button>
        <Drawer :title="fileName" width="800" :onClose="closeRead" :visible="visible">
          <iframe :src="fileUrl" width="100%"></iframe>
        </Drawer>
      </div>

      <div class="w-2/3 bg-white ml-4 p-4">
        <span class="text-lg font-medium mr-4"> 消息记录: </span>
        <hr class="my-4" />

        <div class="max-h-80 overflow-auto">
          <ul>
            <li v-for="item in getList" class="mt-2" :key="item.time">
              <div class="flex items-center">
                <span class="mr-2 text-primary font-medium">收到消息:</span>
                <span>{{ formatToDateTime(item.time) }}</span>
              </div>
              <div>
                {{ item.res }}
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </PageWrapper>
</template>
<script lang="ts">
import { defineComponent, reactive, watchEffect, computed, toRefs, ref } from 'vue';
import { Tag, Input, Drawer } from 'ant-design-vue';
import { PageWrapper } from '/@/components/Page';
import { useWebSocket } from '@vueuse/core';
import { formatToDateTime } from '/@/utils/dateUtil';
import { addTestcaseExecuteRecord, addTestcaseExecuteLog, loadTestcaseExecuteLog } from '/@/api/testcase/testcaseExecuteRecord/testcaseExecuteRecord'

export default defineComponent({
  components: {
    PageWrapper,
    [Input.name]: Input,
    InputTextArea: Input.TextArea,
    Tag,
    Drawer,
  },
  setup() {
    const path = "D:/project/Aidi_PDT-Auto/config/seleniumDrivers/chromedriver.exe"
    const steps = {
      1: {
        by: "",
        value: "",
        action: {
          type: "get",
          value: "https://www.baidu.com",
        },
      },
      2: {
        by: "id",
        value: "kw",
        action: {
          type: "sendKeys",
          value: "selenium",
        },
      },
      3: {
        by: "id",
        value: "kw",
        action: {
          type: "sendKeys",
          value: "111",
        },
      },
    }
    const loadedLog = ref(false);
    const fileUrl = ref("");
    const fileName = ref("");
    const visible = ref(false);
    const state = reactive({
      server: 'ws://localhost:10099/localTest',
      sendValue: '',
      recordList: [] as { id: number; time: number; res: string }[],
    });

    const { status, data, send, close, open } = useWebSocket(state.server, {
      immediate: false,
      autoReconnect: false,
      heartbeat: true,
      onDisconnected: async (ws: WebSocket, event: CloseEvent) => {
        for (const key in steps) {
          if (Object.prototype.hasOwnProperty.call(steps, key)) {
            if (key != "execute_time" && steps[key]['result']['result'] != "success") {
              steps["execute_result"] = "fail";
              break;
            } else if (key != "execute_time" && steps[key]['result']['result'] == "success") {
              steps["execute_result"] = "success";
            }
          }
        }
        steps["execute_type"] = 1
        const record_result = await addTestcaseExecuteRecord({
          execute_result: steps["execute_result"],
          execute_time: steps["execute_time"],
          execute_type: steps["execute_type"],
        })
        delete steps["execute_result"]
        delete steps["execute_time"]
        delete steps["execute_type"]
        const execute_cord = record_result['id']
        const log_result = await addTestcaseExecuteLog({
          execute_record: execute_cord,
          execute_log: steps,
        })
        const { id, log_path } = log_result;
        fileName.value = log_path
        const log_buffer = await loadTestcaseExecuteLog({ id: id })
        console.log(log_buffer);
        const blob = new Blob([log_buffer.data], {
          type: log_buffer.headers['content-type']
        })
        fileUrl.value = URL.createObjectURL(blob)
        loadedLog.value = true
      }
    });

    watchEffect(() => {
      if (data.value) {
        const res = JSON.parse(data.value);
        const time = new Date().getTime();
        state.recordList.push({
          res: res,
          id: Math.ceil(Math.random() * 1000),
          time: time,
        });
        for (const key in res) {
          if (Object.prototype.hasOwnProperty.call(res, key)) {
            steps[key]["result"] = { "time": time, "result": res[key] }
          }
        }
      }
    });

    const getIsOpen = computed(() => status.value === 'OPEN');
    const getTagColor = computed(() => (getIsOpen.value ? 'success' : 'red'));

    const getList = computed(() => {
      return [...state.recordList].reverse();
    });

    function handlerSend() {
      state.sendValue = JSON.stringify({
        "path": path,
        "steps": steps
      })
      send(state.sendValue);
      steps["execute_time"] = formatToDateTime(new Date().getTime());
      state.sendValue = '';
    }

    function toggle() {
      if (getIsOpen.value) {
        close();
      } else {
        open();
      }
    }

    const perviewLog = () => {
      visible.value = true;
    }

    const closeRead = () => {
      visible.value = false;
    }

    return {
      status,
      formatToDateTime,
      ...toRefs(state),
      loadedLog,
      fileUrl,
      fileName,
      perviewLog,
      handlerSend,
      getList,
      toggle,
      getIsOpen,
      getTagColor,
      closeRead,
      visible,
    };
  },
});
</script>
