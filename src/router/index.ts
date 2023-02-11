import axios from 'axios'

import { createRouter, createWebHistory } from 'vue-router'
import { useStore } from '../store/index'
import { useToast } from '../composables/toast'

import Home from '../views/Home.vue'
import QuicktrackMain from '../views/QuicktrackMain.vue'
import QuicktrackDetails from '../views/QuicktrackDetails.vue'
import Runcitworks from '../views/Runcitworks.vue'
import v4rw from '../views/v4rw.vue'
import ToastView from '../views/ToastView.vue'
import Login from '../views/Login.vue'

import RuncitworksSales from '../views/Runcitworks/RuncitworksSales.vue'
import RuncitworksPurchases from '../views/Runcitworks/RuncitworksPurchases.vue'
import RuncitworksExpenses from '../views/Runcitworks/RuncitworksExpenses.vue'
import RuncitworksCurrentBalance from '../views/Runcitworks/RuncitworksCurrentBalance.vue'
import RuncitworksCashFlow from '../views/Runcitworks/RuncitworksCashFlow.vue'
import RuncitworksSetup from '../views/Runcitworks/RuncitworksSetup.vue'
import RuncitworksDashboard from '../views/Runcitworks/RuncitworksDashboard.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'QuicktrackMain',
            component: QuicktrackMain,
            meta: { req_auth: true },
        },
        {
            path: '/accounts/:id',
            name: 'QuicktrackDetails',
            component: QuicktrackDetails,
            meta: { req_auth: true },
        },
        {
            path: '/runcitworks',
            name: 'Runcitworks',
            component: v4rw,
            meta: { req_auth: true },
            children: [
                // nested routes
                // https://router.vuejs.org/guide/essentials/nested-routes.html
                {
                    path: '',
                    name: 'rw-dashboard',
                    component: RuncitworksDashboard,
                },
                {
                    path: 'sales',
                    name: 'rw-sales',
                    component: RuncitworksSales,
                },
                {
                    path: 'purchases',
                    name: 'rw-purchases',
                    component: RuncitworksPurchases,
                },
                {
                    path: 'expenses',
                    name: 'rw-expenses',
                    component: RuncitworksExpenses,
                },
                {
                    path: 'balance',
                    name: 'rw-balance',
                    component: RuncitworksCurrentBalance,
                },
                {
                    path: 'cashflow',
                    name: 'rw-cashflow',
                    component: RuncitworksCashFlow,
                },
                {
                    path: 'settings',
                    name: 'rw-settings',
                    component: RuncitworksSetup,
                },
            ],
        },
        { path: '/login', name: 'Login', component: Login },
    ],
})

router.beforeEach(async (to) => {
    const store = useStore()
    const toast = useToast()
    if (to.meta.req_auth && store.$state.isLoggedIn == false) {
        const res = await axios.get('/accounts/me')
        if (res.data.username == '') {
            toast.error('Invalid Credentials', 'You are not Logged In.')
            store.csrftoken = res.data.csrftoken
            return { name: 'Login' }
        }
        store.$patch({
            username: res.data.username,
            csrftoken: res.data.csrftoken,
            isLoggedIn: true,
        })
    }
})

export default router
