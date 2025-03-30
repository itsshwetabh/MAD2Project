import { createRouter, createWebHistory } from "vue-router";
import Landing from "./components/Landing/Landing.vue";
import AdminDashboard from "./components/Admin/AdminDashboard.vue";
import AdminHome from "./components/Admin/AdminHome.vue";
import AdminQuiz from "./components/Admin/AdminQuiz.vue";
import AdminSummary from "./components/Admin/AdminSummary.vue";
import UserDashboard from "./components/User/UserDashboard.vue";
import UserScore from "./components/User/UserScore.vue";
import UserSummary from "./components/User/UserSummary.vue";
import UserHome from "./components/User/UserHome.vue";
import Test from "./components/User/Test.vue";

const routes = [
    {
        name: 'Landing',
        path: '/',
        component: Landing
    },
    {
        name: 'AdminDashboard',
        path: '/AdminDashboard',
        component: AdminDashboard,
        meta: { requiresAuth: true },
        redirect: '/AdminDashboard/home',
        children: [  // 👈 Define AdminHome as a child route
            {
                name: 'AdminDashboardHome',
                path: 'home',  // 👈 Relative path (not starting with '/')
                component: AdminHome,
                meta: { requiresAuth: true }
            },
            {
                name: 'AdminQuiz',
                path: 'quiz',  // 👈 Relative path (not starting with '/')
                component: AdminQuiz,
                meta: { requiresAuth: true }
            },
            {
                name: 'AdminSummary',
                path: 'summary',  // 👈 Relative path (not starting with '/')
                component: AdminSummary,
                meta: { requiresAuth: true }
            },

        ]
    },
    {
        name: 'UserDashboard',
        path: '/UserDashboard',
        component: UserDashboard,
        meta: { requiresAuth: true },
        redirect: '/UserDashboard/home',
        children: [  // 👈 Define AdminHome as a child route
            {
                name: 'UserDashboardHome',
                path: 'home',  // 👈 Relative path (not starting with '/')
                component: UserHome,
                meta: { requiresAuth: true }
            },
            {
                name: 'UserSummary',
                path: 'summary',  // 👈 Relative path (not starting with '/')
                component: UserSummary,
                meta: { requiresAuth: true }
            },
            {
                name: 'UserScore',
                path: 'score',  // 👈 Relative path (not starting with '/')
                component: UserScore,
                meta: { requiresAuth: true }
            },
            {
                name: 'Test',
                path: 'test/:id',  // 👈 Relative path (not starting with '/')
                component: Test,
                meta: { requiresAuth: true },
                props:true
            }

        ]
    },


];

const router = createRouter({
    history: createWebHistory(),
    routes
});


router.beforeEach((to, from, next) => {
    const userData = JSON.parse(localStorage.getItem('userData')) || {}; 
    const isAuthenticated = !!userData.token; 

    console.log(isAuthenticated);

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/'); // Redirect to Login page if not logged in
    } else {
        next(); // Proceed to requested route
    }
});

export default router;
