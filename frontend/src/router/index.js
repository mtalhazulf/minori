import { route } from 'quasar/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory
} from 'vue-router'
import routes from './routes'
/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function ({ store }) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
    ? createWebHistory
    : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(
      process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE
    )
  })

  Router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!sessionStorage.getItem('subscriber')) {
        next('/subscriber')
      } else if (
        store.getters.getLoginStatus ||
        sessionStorage.getItem('user')
      ) {
        const user_type = JSON.parse(sessionStorage.getItem('user')).usertype
        if (
          !to.matched.some(record => record.meta.permissions) ||
          (to.matched.some(record => record.meta.permissions) &&
            to.meta.permissions.includes(user_type))
        ) {
          next()
          return
        } else {
          next('')
        }
      } else {
        next('/login')
      }
    } else {
      next()
    }
  })

  return Router
})
