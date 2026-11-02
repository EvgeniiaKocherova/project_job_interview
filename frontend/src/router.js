import { createRouter, createWebHistory } from 'vue-router'
import Login from './view/Login.vue'
import Profile from './view/Profile.vue'
import ForgotPassword from './view/ForgotPassword.vue'
import ResetPassword from './view/ResetPassword.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/forgot-password', component: ForgotPassword },
  { path: '/reset-password', component: ResetPassword }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router