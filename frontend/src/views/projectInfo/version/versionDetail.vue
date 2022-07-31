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
import VersionAdd from './versionAdd.vue';
import VersionView from './versioniew.vue';
import VersionEdit from './versionEdit.vue';

const route = useRoute();
const showComponent = shallowRef<Nullable<ComponentOptions>>(null);
switch (route.params.action) {
    case PageActionEnum.ADD:
        showComponent.value = VersionAdd;
        break;
    case PageActionEnum.EDIT:
        showComponent.value = VersionEdit;
        break;
    case PageActionEnum.VIEW:
        showComponent.value = VersionView;
        break;
}
</script>