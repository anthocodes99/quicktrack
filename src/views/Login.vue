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
    //TODO: Use destructureAxios
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
    //FIXME: login to provide new CSRFToken.
    store.$patch({
        username: res.data.username,
        isLoggedIn: true,
    })
    router.push({ name: 'QuicktrackMain' })
}
</script>

<template>
    <div
        class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8"
    >
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <img
                class="mx-auto h-10 w-auto"
                src="/src/assets/logo.png"
                alt="Your Company"
            />
            <h2
                class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-orange-600"
            >
                Sign in to your account
            </h2>
        </div>

        <div class="sm:mx-auto sm:w-full sm:max-w-sm mt-8">
            <h3 class="text-center text-red-600 text-bold text-lg">
                {{ errorDetails }}
            </h3>
        </div>

        <div class="mt-2 sm:mx-auto sm:w-full sm:max-w-sm">
            <form class="space-y-6" @submit.prevent="login">
                <div>
                    <label
                        for="email"
                        class="block text-sm font-medium leading-6 text-gray-200"
                        >Username</label
                    >
                    <div class="mt-2">
                        <input
                            id="username"
                            name="username"
                            type="username"
                            autocomplete="username"
                            required
                            class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-800 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-[#3f88c5] sm:text-sm sm:leading-6"
                        />
                    </div>
                </div>

                <div>
                    <div class="flex items-center justify-between">
                        <label
                            for="password"
                            class="block text-sm font-medium leading-6 text-gray-200"
                            >Password</label
                        >
                        <div class="text-sm">
                            <a
                                href="#"
                                class="font-semibold text-[#3f88c5] hover:text-[#4a9ee3]"
                                >Forgot password?</a
                            >
                        </div>
                    </div>
                    <div class="mt-2">
                        <input
                            id="password"
                            name="password"
                            type="password"
                            autocomplete="current-password"
                            required
                            class="block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-[#3f88c5] sm:text-sm sm:leading-6"
                        />
                    </div>
                </div>

                <div>
                    <button
                        type="submit"
                        class="flex w-full justify-center rounded-md bg-[#3f88c5] px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-[#4a9ee3] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#3f88c5]"
                    >
                        Sign in
                    </button>
                </div>
            </form>

            <p class="mt-10 text-center text-sm text-gray-500">
                Not a member?
                {{ ' ' }}
                <a
                    href="#"
                    class="font-semibold leading-6 text-[#3f88c5] hover:text-[#4a9ee3]"
                    >Contact administrator</a
                >
            </p>
        </div>
    </div>
</template>

<style scoped></style>
