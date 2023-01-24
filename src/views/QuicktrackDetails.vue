<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import CompositeNav from '../components/CompositeNav.vue'

import TheNavbar from '../components/TheNavbar.vue'
import AnthoButtons from '../components/Quicktrack/AnthoButtons.vue'
import DetailsSubmitPayment from '../components/Quicktrack/DetailsSubmitPayment.vue'

import { useStore } from '../store'
import { useQuicktrackStore } from '../store/quicktrack'
import { useProgressBar } from '../composables/progressbar'
import { useToast } from '../composables/toast'
import { useMonthdataStore } from '../store/monthdata'

import { destructureAxios } from '../utils/utils'

import { Account } from '../models/quicktrack'
import DetailsAddSale from '../components/Quicktrack/DetailsAddSale.vue'
import DetailsCustomSale from '../components/Quicktrack/DetailsCustomSale.vue'
import DetailsAddHutang from '../components/Quicktrack/DetailsAddHutang.vue'
import DetailRecentSales from '../components/Quicktrack/DetailRecentSales.vue'

const store = useStore()
const quicktrack = useQuicktrackStore()
const monthdata = useMonthdataStore()
const progressBar = useProgressBar()
const toast = useToast()
const route = useRoute()

// local properties

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

// template refs
const isInitialized = ref(false)
const isError = ref(false)
const monthdataId = ref<number | undefined>()

// computed properties
const username = computed(() => store.username)

const accounts = computed(() => quicktrack.accounts)
const account = ref<Account>()

const monthdatas = computed(() => monthdata.monthdatas)

const currentMonthdataProducts = computed(
    () =>
        monthdata.monthdatas.find(
            (monthdata) => monthdata.id == monthdataId.value
        )?.products ?? []
)

// initialize progress bar
progressBar.initProgress(30)

onMounted(async () => {
    progressBar.addProgress(30)
    // FIXME: What if I had no accounts?
    if (accounts.value.length === 0) {
        await quicktrack.initAccounts()
    }
    if (monthdata.monthdatas.length === 0) {
        await monthdata.initMontdatas()
    }
    const currAccount = quicktrack.accounts.find(
        (acc) => acc.id === parseInt(route.params.id)
    )
    if (typeof currAccount === 'undefined') {
        toast.error(
            'An error occured.',
            'Did not successfully retrieve Account!'
        )
        isError.value = true
        return
    }
    // else
    account.value = currAccount
    if (monthdata.monthdatas.length !== 0) {
        monthdataId.value = monthdata.monthdatas[0].id
    }
    progressBar.addProgress(40)
    isInitialized.value = true
})

const createSale = async function (event) {
    const formData = Object.fromEntries(new FormData(event.target))
    const { date, product, unitprice: unitPrice, quantity } = formData
    const data = {
        monthdata: monthdataId.value,
        date: date,
        product: product,
        unit_price: unitPrice,
        quantity: quantity,
    }
    const [res, err] = await destructureAxios(
        axios.post(`/api/accounts/${account.value!.id}/sales`, data, config)
    )
    if (res) {
        // update hutang
        account.value!.hutang += unitPrice * quantity
        // update the sale for the monthdata
        const updMonthdata = monthdata.monthdatas.find(
            (monthdata) => monthdata.id === res.data.monthdata
        )
        // if monthdata exists and is initialized(sales exists)
        if (updMonthdata && updMonthdata['sales']) {
            updMonthdata['sales'].push(res.data)
        }
        // update the current account's sales as well
        account.value!.recent_sales.push(res.data)
        return toast.success('Sale Added', 'Sale added succesfully!')
    }
    // else
    toast.error(
        'Failed to add Sale!',
        `Something went wrong. ${Object.values(err.response.data)}`
    )
}

const submitPayment = async function (event) {
    const formData = Object.fromEntries(new FormData(event.target))
    const { paymentAmount } = formData

    if (paymentAmount > account.value!.hutang) {
        return toast.error('Error!', 'You may not pay more than the hutang!')
    }

    //FIXME: make it accurate. This is off by about 0.01
    account.value!.hutang = parseFloat(
        (account.value!.hutang - paymentAmount).toFixed(2)
    )

    const data = {
        hutang: account.value!.hutang,
    }

    const [res, err] = await destructureAxios(
        axios.patch(`/api/accounts/${account.value!.id}`, data, config)
    )
    if (res) {
        toast.success('Payment Success', 'Succesfully made payment.')
        return
    }
    // else
    toast.error(
        'Payment Failed',
        `Something went wrong. ${Object.values(err.response.data)}`
    )
}
</script>

<template>
    <CompositeNav>
        <div class="w-full sm:max-w-md sm:mx-auto md:mx-0">
            <template v-if="!isInitialized">
                <div class="mt-32 flex justify-center" role="status">
                    <svg
                        aria-hidden="true"
                        class="w-16 h-16 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                        viewBox="0 0 100 101"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                            fill="currentColor"
                        />
                        <path
                            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                            fill="currentFill"
                        />
                    </svg>
                    <span class="sr-only">Loading...</span>
                </div>
            </template>
            <template v-else-if="isError">
                <!-- TODO: Error Page -->
                <h1>An error occured.</h1>
                <p>It seems like we hic'd.</p>
            </template>
            <template v-else>
                <div class="p-4">
                    <!-- Account Name & Hutang -->
                    <h1 class="text-4xl">{{ account!.username }}</h1>
                    <h2 class="text-2xl pt-2">
                        RM {{ account!.hutang.toFixed(2) }}
                    </h2>

                    <!-- Add Sale Form -->
                    <DetailsAddSale
                        class="pt-8"
                        :products="currentMonthdataProducts"
                        @submit.prevent="createSale"
                    />

                    <!-- Runcitworks Monthdata Selector -->
                    <div class="container">
                        <label class="form-label fs-4" for="monthdata-selector"
                            >Monthdata</label
                        >
                        <div v-if="monthdatas.length === 0">
                            <p class="lead">
                                You haven't initialize Runcitworks yet.
                                <router-link :to="{ name: 'Runcitworks' }">
                                    Head there?
                                </router-link>
                            </p>
                        </div>
                        <select
                            v-else
                            v-model="monthdataId"
                            class="form-select"
                            id="monthdata-selector"
                        >
                            <option
                                selected
                                v-for="monthdata in monthdatas"
                                :key="monthdata.id"
                                :value="monthdata.id"
                            >
                                {{ monthdata.month }}
                            </option>
                        </select>

                        <!-- <DetailsAddHutang />
                        <DetailsSubmitPayment @submitPayment="submitPayment" /> -->
                        <DetailRecentSales :account="account!" />
                    </div>
                </div>
            </template>
        </div>
    </CompositeNav>
</template>

<style scoped></style>
