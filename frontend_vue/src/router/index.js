import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import CoursesView from '@/views/CoursesView.vue'
import WorkspaceView from '@/views/WorkspaceView.vue'
import EditView from '@/views/EditView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      //component: () => import('../views/LoginView.vue')
    },
    {
      path: '/courses',
      name:'courses',
      component: CoursesView,
    },
    {
      path: '/workspace',
      name:'workspace',
      component: WorkspaceView,
    },
    {
      path: '/edit',
      name:'edit',
      component: EditView,
    }
  ]
})

export default router
