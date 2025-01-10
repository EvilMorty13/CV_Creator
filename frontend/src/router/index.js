import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ProfileView from '@/views/ProfileView.vue';
import { useTokenStore } from '@/stores/tokenStore';



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }, 
    },
  ],
});

// Navigation guard to check authentication before allowing access to protected routes
router.beforeEach((to, from, next) => {
  const tokenStore = useTokenStore();

  if (to.meta.requiresAuth && !tokenStore.isAuthenticated()) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;
