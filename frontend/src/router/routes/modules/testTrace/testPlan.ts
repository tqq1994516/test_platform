import type { AppRouteModule } from '/@/router/types';
import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const testTrace: AppRouteModule = {
  path: '/testTrace',
  name: 'TestTrace',
  component: LAYOUT,
  meta: {
    orderNo: 20,
    icon: 'ion:aperture-outline',
    title: t('routes.testTrace.testTrace.title'),
  },
  children: [
    {
      path: 'testPlan',
      name: 'TestPlan',
      components: () => import('/@/views/testTrace/testPlan/index.vue'),
      meta: {
        title: t('routes.testTrace.testPlan.title'),
      },
    },
  ],
};

export default testTrace;
