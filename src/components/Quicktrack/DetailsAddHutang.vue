<script setup lang="ts">
import { useStore } from '../../store'
import { useQuicktrackStore } from '../../store/quicktrack'

import { useToast } from '../../composables/toast'
import { destructureAxios } from '../../utils/utils'
import axios from 'axios'
import { Account } from '../../models/quicktrack'
import { useRoute } from 'vue-router'

// interface Props {
//     account: Account
// }

// const props = defineProps<Props>()

// initialization
const route = useRoute()
const store = useStore()
const quicktrack = useQuicktrackStore()
const toast = useToast()

const account = quicktrack.accounts.find(
    (account) => account.id === parseInt(route.params.id)
)

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

const addHutang = async function (event) {
    const formData = Object.fromEntries(new FormData(event.target))
    const { amount } = formData

    const data = {
        hutang: account!.hutang + parseInt(amount),
    }
    const [res, err] = await destructureAxios(
        axios.patch(`/api/accounts/${account!.id}`, data, config)
    )

    if (res) {
        account!.hutang += parseFloat(amount)
        return toast.success('Hutang Added!', 'Hutang added successfully.')
    }
    // else
    toast.error('Error!', 'Did not succesffully add Hutang.')
}
</script>

<template>
    <div
        class="container-xxl container-xxl col-xl-7 border border-sm border-2 mt-2"
    >
        <form class="form py-2" @submit.prevent="addHutang">
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
