<script setup lang="ts">
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

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

const createSale = async function (product, unitPrice, quantity, date = null) {
    if (monthdata.monthdatas.length === 0)
        return toast.error(
            'Did not create Sale!',
            'You have yet to initialize Runcitworks!'
        )
    let dateData: string | null = date
    if (date == null) {
        const date = new Date()
        const [month, day, year] = [
            // for the love of god getMonth() starts from 0
            date.getMonth() + 1,
            date.getDate(),
            date.getFullYear(),
        ]
        dateData = `${year}-${month}-${day}`
    }
    const data = {
        monthdata: monthdataId.value,
        date: dateData,
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
    <TheNavbar />
    <div class="container-sm col-md-9 col-lg-7 border border-3">
        <template v-if="!isInitialized">
            <h1>Loading...</h1>
        </template>
        <template v-else-if="isError">
            <h1>An error occured.</h1>
            <p>It seems like we hic'd.</p>
        </template>
        <template v-else>
            <h1 class="text-center">{{ account!.username }}</h1>
            <h2 class="text-center">Hutang : RM {{ account!.hutang }}</h2>
            <template v-if="store.username == 'antho'">
                <AnthoButtons @makeSale="createSale" />
            </template>
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
                <DetailsCustomSale
                    :products="currentMonthdataProducts"
                    @submitSale="
                        createSale(
                            $event.product,
                            $event.unitPrice,
                            $event.quantity,
                            $event.date
                        )
                    "
                />
                <DetailsAddHutang />
                <DetailsSubmitPayment @submitPayment="submitPayment" />
                <DetailRecentSales :account="account!" />
            </div>
        </template>
    </div>
</template>

<style scoped></style>
