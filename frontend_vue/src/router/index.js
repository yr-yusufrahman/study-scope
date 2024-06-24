import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import CoursesView from '@/views/CoursesView.vue'
import WorkspaceView from '@/views/WorkspaceView.vue'
import EditView from '@/views/EditView.vue'
import QuizView from '@/views/QuizView.vue'


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
      meta: { requiresAuth: true } // Stores data about the route
    },
    {
      path: '/workspace',
      name:'workspace',
      component: WorkspaceView,
      meta: { requiresAuth: true }
    },
    {
      path: '/edit',
      name:'edit',
      component: EditView,
      meta: { requiresAuth: true }
    },
    {
      path: '/quiz',
      name:'quiz',
      component: QuizView,
      meta: { requiresAuth: true }
    }
  ],

  scrollBehavior(to, from, savedPosition) {
    // always scroll to top
    return { top: 0 }
  },
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); // Check if token exists

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next({ name: 'login' }); // Redirect to login page
  } else {
    next(); // Proceed to route
  }
});


export default router
