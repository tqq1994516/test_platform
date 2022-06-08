import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const projectInfo: AppRouteModule = {
  path: '/testcase',
  name: 'Testcase',
  component: LAYOUT,
  redirect: '/testcase/testcases',
  meta: {
    orderNo: 30,
    icon: 'octicon:project-16',
    title: t('routes.testcase.testcase.testcase.title'),
  },

  children: [

    {
      path: 'testcases',
      name: 'testcases',
      component: () => import('/@/views/testcase/testcases/testcases.vue'),
      meta: {
        icon: 'ant-design:project-filled',
        title: t('routes.testcase.testcase.testcases.title'),
      },
    },
  ],
};

export default projectInfo;
