<template>
    <div>
        <Suspense>
            <component :is="showComponent"></component>
        </Suspense>
    </div>
</template>
<script lang="ts" setup>
import { shallowRef, ComponentOptions } from 'vue';
import { useRoute } from 'vue-router';
import { PageActionEnum } from '/@/enums/pageActionEnum';
import ProjectAdd from './projectAdd.vue';
import ProjectView from './projectView.vue';
import ProjectEdit from './projectEdit.vue';

const route = useRoute();
const showComponent = shallowRef<Nullable<ComponentOptions>>(null);
switch (route.params.action) {
    case PageActionEnum.ADD:
        showComponent.value = ProjectAdd;
        break;
    case PageActionEnum.EDIT:
        showComponent.value = ProjectEdit;
        break;
    case PageActionEnum.VIEW:
        showComponent.value = ProjectView;
        break;
}
</script>