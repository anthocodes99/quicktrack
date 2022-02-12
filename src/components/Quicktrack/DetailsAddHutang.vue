<script setup lang="ts">
import { useStore } from '../../store'
import { useQuicktrackStore } from '../../store/quicktrack'

import { useToast } from '../../composables/toast'
import { destructureAxios } from '../../utils/utils'
import axios from 'axios'
import { Account } from '../../models/quicktrack'

interface Props {
    account: Account
}

const props = defineProps<Props>()

// initialization
const store = useStore()
const quicktrack = useQuicktrackStore()
const toast = useToast()

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

const addHutang = async function (event) {
    const formData = Object.fromEntries(new FormData(event.target))
    const { amount } = formData

    const data = {
        hutang: props.account.hutang + amount,
    }
    const [res, err] = await destructureAxios(
        axios.patch(`/api/accounts/${props.account.id}`, data, config)
    )

    if (res) {
        toast.success('Hutang Added!', 'Hutang added successfully.')
    }
}
</script>

<template>
    <div class="container-xxl container-xxl col-xl-7 border border-2 mt-2">
        <form class="form" @submit.prevent="addHutang">
            <h2>Add Hutang</h2>
            <label for="amount" class="form-label">Amount</label>
            <div class="row g-3">
                <div class="col-8">
                    <input
                        class="form-control"
                        type="number"
                        name="amount"
                        id="amount"
                    />
                </div>
                <div class="col-4">
                    <input
                        class="btn btn-success"
                        type="submit"
                        value="Submit"
                    />
                </div>
            </div>
        </form>
    </div>
</template>

<style scoped></style>
