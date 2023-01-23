import { createApp } from 'vue'
import router from './router/index'

import App from './App.vue'

import '@fortawesome/fontawesome-free/css/all.css'
// import 'bootstrap'
// import 'bootstrap/dist/css/bootstrap.min.css'
import { createPinia } from 'pinia'
import './style.css'
const pinia = createPinia()

createApp(App).use(pinia).use(router).mount('#app')
