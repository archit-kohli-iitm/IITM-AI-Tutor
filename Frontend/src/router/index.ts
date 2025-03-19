import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Signup from '../views/Signup.vue';
import login from '@/views/login.vue';
import home from '@/views/home.vue';
import Course from '@/views/Course.vue';
const routes = [
  {
    path: '/',
    name: 'HOME',
    component: HomeView,
  },
  {
    path: '/course',
    name: 'Course',
    component: Course,
  },

  {
    path:'/signup',
    name:'SignUp',
    component:Signup,
  },
  {
    path:'/login',
    name:'Login',
    component:login,
  },
  {
    path:'/home',
    name:'Home',
    component:home,
  },
];









const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
