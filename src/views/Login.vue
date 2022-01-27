<script setup lang="ts">
import axios from 'axios'

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '../store'

const errorDetails = ref('')

const store = useStore()
const router = useRouter()

const login = async function (event) {
    const formData = Object.fromEntries(new FormData(event.target))
    const data = {
        username: formData.username,
        password: formData.password,
    }
    const options = {
        headers: {
            'X-CSRFToken': store.csrftoken,
        },
    }
    let res
    try {
        res = await axios.post('/accounts/login', data, options)
    } catch (err) {
        if (err.response.data['non_field_errors'] != null) {
            errorDetails.value = err.response.data['non_field_errors'][0]
        } else {
            errorDetails.value = 'Something went wrong.'
        }
    }
    // if succeeds
    store.$patch({
        username: res.data.username,
        isLoggedIn: true,
    })
    router.push({ name: 'QuicktrackMain' })
}
</script>

<template>
    <div class="container-lg col-lg-3 col-sm-5 mt-5">
        <h1>Quicktrack Login</h1>
        <span class="text-danger" v-if="errorDetails !== ''">
            {{ errorDetails }}
        </span>
        <form @submit.prevent="login">
            <div class="mb-3">
                <label for="loginUsername" class="form-label">Username</label>
                <input
                    class="form-control"
                    type="text"
                    name="username"
                    id="loginUsername"
                    required
                />
            </div>
            <div class="mb-3">
                <label for="loginPassword" class="form-label">Password</label>
                <input
                    class="form-control"
                    type="password"
                    name="password"
                    id="loginPassword"
                    required
                />
            </div>
            <div class="mb-3">
                <input
                    type="submit"
                    class="btn btn-primary"
                    id="loginSubmit"
                    value="Log In"
                />
            </div>
        </form>
    </div>
</template>

<style scoped></style>
