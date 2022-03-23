<script setup lang="ts">
import axios from 'axios'
import { computed } from 'vue'
import { useToast } from '../composables/toast'
import { useStore } from '../store'
import { destructureAxios } from '../utils/utils'

const store = useStore()
const toast = useToast()

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

// computed properties

const username = computed(() => store.username)

// template functions

const logout = async function () {
    const [res, err] = await destructureAxios(
        axios.post('/accounts/logout', {}, config)
    )
    if (res) {
        return window.location.replace('/login')
    }
    // else
    toast.error('Error!', "Couldn't log out.")
}
</script>

<template>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <div class="flex justify-content-start">
                <router-link
                    :to="{ name: 'QuicktrackMain' }"
                    class="navbar-brand text-orange"
                    >Quicktrack</router-link
                >
                <router-link
                    :to="{ name: 'Runcitworks' }"
                    class="navbar-brand text-orange"
                    >Runcitworks</router-link
                >
            </div>
            <span class="navbar-text">
                {{ username }}
                <a href="#" class="navbar-text" @click.prevent="logout()"
                    >Log out</a
                >
            </span>
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    background-color: var(--bs-gray-dark);
}

.navbar-brand {
    color: #e94f37 !important;
}

.nav-link {
    color: var(--bs-light) !important;
}

.navbar-text {
    color: #3f88c5 !important;
}
</style>
