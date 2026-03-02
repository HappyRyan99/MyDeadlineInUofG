import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import CoursesView from '../views/CoursesView.vue'
import GroupsView from '../views/GroupsView.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/dashboard/',
            name: 'dashboard',
            component: DashboardView
        },
        {
            path: '/courses/',
            name: 'courses',
            component: CoursesView
        },
        {
            path: '/groups/',
            name: 'groups',
            component: GroupsView
        }
    ]
})

export default router
