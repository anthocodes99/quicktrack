<script setup lang="ts">
import axios from 'axios'
import { useToast } from '../../composables/toast'
import { useStore } from '../../store'
import { useQuicktrackStore } from '../../store/quicktrack'
import { destructureAxios } from '../../utils/utils'

import BaseInput from '../../primitives/BaseInput.vue'
import BaseButton from '../../primitives/BaseButton.vue'

const store = useStore()
const quicktrack = useQuicktrackStore()
const toast = useToast()

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

const createUser = async function (event) {
    const formData = Object.fromEntries(new FormData(event.target))

    const { username, hutang } = formData

    const data = {
        username,
        hutang: hutang === '' ? 0 : hutang,
    }

    const [res, err] = await destructureAxios(
        axios.post('/api/accounts', data, config)
    )

    if (res) {
        quicktrack.addAccount(res.data)
        return toast.success('Account Created', 'Account created successfully.')
    }
    // else
    toast.error('Did not created Account!', 'Something went wrong.')
}
</script>

<template>
    <div class="px-2">
        <h2 class="text-2xl">Create Account</h2>
        <form class="pt-2 px-2" @submit.prevent="createUser">
            <div class="">
                <label for="username" class="text-gray-400">
                    Account Name
                </label>
                <BaseInput
                    type="text"
                    placeholder="Cinnamoroll"
                    name="username"
                />
            </div>
            <div class="mt-4">
                <label for="hutang" class="text-gray-400">
                    Initial Hutang
                </label>
                <BaseInput type="number" value="0" name="hutang" />
            </div>
            <BaseButton class="mt-8" type="submit"
                ><span class="font-semibold">Create Account</span></BaseButton
            >
        </form>
    </div>
</template>

<style scoped></style>
-
