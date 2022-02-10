<script setup lang="ts">
import axios from 'axios'
import { useToast } from '../../composables/toast'
import { useStore } from '../../store'
import { useQuicktrackStore } from '../../store/quicktrack'
import { destructureAxios } from '../../utils/utils'

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
    <div class="container col-lg-5 col-md-7 col-sm-12 border border-2 mt-5 p-2">
        <h2>Add User</h2>
        <form class="row g-3" @submit.prevent="createUser">
            <div class="col-md-6">
                <label for="username" class="form-label">Username</label>
                <input
                    class="form-control"
                    type="text"
                    placeholder="Djlans"
                    name="username"
                />
            </div>
            <div class="col-md-4">
                <label for="hutang" class="form-label">Starting Hutang</label>
                <input
                    class="form-control"
                    id="hutang"
                    type="number"
                    placeholder="10"
                    name="hutang"
                />
            </div>
            <div class="d-flex align-items-end col-md-2">
                <button class="btn btn-outline-success" style="width: 100%">
                    Create
                </button>
            </div>
        </form>
    </div>
</template>

<style scoped></style>
-
