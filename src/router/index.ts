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
            component: Runcitworks,
            meta: { req_auth: true },
        },
        {
            path: '/v4rw',
            name: 'v4rw',
            component: v4rw,
            meta: { req_auth: true },
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
