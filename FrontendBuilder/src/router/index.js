import { createRouter, createWebHistory } from 'vue-router';
import { authGuard } from '@auth0/auth0-vue';
import Landing from '../views/Landing.vue';

export const router = createRouter({
    history: createWebHistory(),
    routes: [
        // --- Public ---
        { path: '/', component: Landing, meta: { hideLayout: true }},
        { path: '/privacy', component: () => import('../views/PrivacyPolicy.vue'), meta: { hideLayout: true }},
        {
            path: '/preview-render',
            name: 'PreviewRender',
            component: () => import('../views/PreviewRender.vue'),
            meta: { hideLayout: true, requiresAuth: false }
        },
        {
            path: '/presentation',
            name: 'Presentation',
            component: () => import('../views/PresentationView.vue'),
            meta: { hideLayout: true }
        },

        // --- (Auth0) ---
        { path: '/waiting', component: () => import('../views/WaitingRoom.vue'), beforeEnter: authGuard },
        { path: '/dashboard', component: () => import('../views/Dashboard.vue'), beforeEnter: authGuard },
        { path: '/create', component: () => import('../views/CreateSite.vue'), beforeEnter: authGuard },
        { path: '/edit/:id', component: () => import('../views/EditSite.vue'), beforeEnter: authGuard },
        { path: '/domains', component: () => import('../views/DomainManager.vue'), beforeEnter: authGuard },
        { path: '/leads', component: () => import('../views/Leads.vue'), beforeEnter: authGuard },
        { path: '/settings', component: () => import('../views/Settings.vue'), beforeEnter: authGuard },
        { path: '/products', component: () => import('../views/ProductsManager.vue'), beforeEnter: authGuard },
        { path: '/seo', component: () => import('../views/SeoManager.vue'), beforeEnter: authGuard },
        { path: '/usage', component: () => import('../views/Usage.vue'), beforeEnter: authGuard }
    ]
});