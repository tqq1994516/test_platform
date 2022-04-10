import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const projectInfo: AppRouteModule = {
  path: '/projectInfo',
  name: 'ProjectInfo',
  component: LAYOUT,
  redirect: '/projectInfo/project',
  meta: {
    orderNo: 30,
    icon: 'octicon:project-16',
    title: t('routes.projectInfo.projectInfo.projectInfo.title'),
  },

  children: [

    {
      path: 'project',
      name: 'Project',
      component: () => import('/@/views/projectInfo/project/project.vue'),
      meta: {
        icon: 'ant-design:project-filled',
        title: t('routes.projectInfo.projectInfo.project.title'),
      },
    },
    {
      path: 'env',
      name: 'Env',
      component: () => import('/@/views/projectInfo/env/env.vue'),
      meta: {
        icon: 'eos-icons:env',
        title: t('routes.projectInfo.projectInfo.env.title'),
      },
    },
    {
      path: 'version',
      name: 'Version',
      component: () => import('/@/views/projectInfo/version/version.vue'),
      meta: {
        icon: 'carbon:version',
        title: t('routes.projectInfo.projectInfo.version.title'),
      },
    },
  ],
};

export default projectInfo;
