const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/notebook', component: () => import('pages/Notebook.vue') },
      {
        path: '/tasks',
        component: () => import('pages/Tasks.vue'),
        meta: { permissions: ['superadmin', 'admin', 'user'] }
      },
      { path: '/logbook', component: () => import('pages/Logbook.vue') },
      { path: '/medication', component: () => import('pages/Medication.vue') },
      {
        path: '/minor_info_sheet?id=:id&isFirstPriceEdit=:isFirstPriceEdit',
        name: 'minor_info_sheet',
        component: () => import('pages/MinorInfoSheet.vue'),
        props: true
      },
      {
        path: '/adult_info_sheet?id=:id&isFirstPriceEdit=:isFirstPriceEdit',
        name: 'adult_info_sheet',
        component: () => import('pages/AdultInfoSheet.vue'),
        props: true
      },
      {
        path: '/minor_register',
        component: () => import('pages/MinorAttendanceRegister.vue')
      },
      {
        path: '/minors',
        component: () => import('pages/Minors.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/minors_archive',
        component: () => import('pages/MinorsArchive.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/minors_tariffs',
        component: () => import('pages/MinorsTariffs.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/adults',
        component: () => import('pages/Adults.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/adult_register',
        component: () => import('pages/AdultAttendanceRegister.vue')
      },
      {
        path: '/adults_archive',
        component: () => import('pages/AdultsArchive.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/adults_tariffs',
        component: () => import('pages/AdultsTariffs.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/operator_register',
        component: () => import('pages/OperatorAttendanceRegister.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/operators',
        component: () => import('pages/Operators.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/operator_archive',
        component: () => import('pages/OperatorArchive.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/rooms',
        component: () => import('pages/Rooms.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/scheduler',
        component: () => import('pages/Scheduler.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/shifts',
        component: () => import('pages/Shifts.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/operator-shifts',
        component: () => import('pages/OperatorShifts.vue'),
        meta: { permissions: ['user'] }
      },
      { path: '/calendar', component: () => import('pages/Calendar.vue') },
      {
        path: '/settings',
        component: () => import('pages/Settings.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/reports',
        component: () => import('pages/Reports.vue'),
        meta: { permissions: ['superadmin', 'admin'] }
      },
      {
        path: '/phone_call_log',
        component: () => import('pages/PhoneCallLog.vue')
      },
      {
        path: '/change_password',
        component: () => import('pages/ChangePassword.vue')
      },
      {
        path: 'catalogo',
        name: 'catalogo',
        component: () => import('pages/Catalogo.vue')
      },
      {
        path: '/incentivi',
        component: () => import('pages/UserIncentives.vue')
      }
    ],
    meta: {
      requiresAuth: true
    }
  },
  { path: '/subscriber', component: () => import('src/pages/Subscriber.vue') },
  { path: '/login', component: () => import('src/pages/Login.vue') },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
