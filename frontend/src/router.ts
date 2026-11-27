import { createRouter, createWebHashHistory } from 'vue-router'
import { modeInfo } from './domain/modes'
import { MODES } from './types'
import HomeView from './views/HomeView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView, meta: { title: '怪物血量统计' } },
    ...MODES.map(mode => ({
      path: '/' + mode,
      name: mode,
      component: () => import('./views/ModeView.vue'),
      props: { mode },
      meta: { title: modeInfo[mode].name },
    })),
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, top: 100 }
    return { top: 0 }
  },
})

router.afterEach(to => {
  document.title = String(to.meta.title ?? '怪物血量统计') + ' · 星轨档案'
})

export default router
