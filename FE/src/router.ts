import { createRouter, createWebHistory } from 'vue-router';
import redirect from '@/views/redirect.vue'
import Login from '@/views/login/login.vue'
import Dashboard from "@/views/dashboard/dashboard.vue";

interface route {
    path: string,
    name: string,
    component: unknown
}

const routes: route[] = [
    {
        path: '/',
        name: 'redirect',
        component: redirect
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: Dashboard,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router