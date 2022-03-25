import type { AppRouteModule } from '/@/router/types';
import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const projectManager: AppRouteModule = {
  path: '/projectManager',
  name: 'ProjectManager',
  component: LAYOUT,
  meta: {
    orderNo: 20,
    icon: 'ion:aperture-outline',
    title: t('routes.projectManager.projectManager.title'),
  },
  children: [
    {
      path: 'projectInfo',
      name: 'ProjectInfo',
      components: () => import('/@/views/testTrace/testPlan/index.vue'),
      meta: {
        title: t('routes.projectManager.projectInfo.title'),
      },
    },
  ],
};

export default projectManager;
