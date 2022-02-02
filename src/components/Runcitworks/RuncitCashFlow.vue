<script setup lang="ts">
import { computed, ref, toRefs } from 'vue'

import { Monthdata } from '../../models/monthdata'

import { useRuncitworks } from '../../composables/runcitworks'
import { useToast } from '../../composables/toast'
import { destructureAxios } from '../../utils/utils'
import axios from 'axios'
import { useStore } from '../../store'
import { useMonthdataStore } from '../../store/monthdata'

interface Props {
    currentMonthData: Monthdata
}

interface PerformanceTableItem {
    product: string
    unitProfit: number
    netProfit: number
}

const props = defineProps<Props>()
const { currentMonthData } = toRefs(props)

// Initialization
const store = useStore()
const monthdata = useMonthdataStore()
const toast = useToast()
const runcitworks = useRuncitworks(currentMonthData)

// local variables

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

// Computed Properties

const startingModal = computed(() => currentMonthData.value.starting_modal)

const totalProfit = computed(() => {
    let performanceTable: PerformanceTableItem[] = []
    currentMonthData.value.products.forEach((product) =>
        performanceTable.push(runcitworks.calculateProductPerformance(product))
    )
    return performanceTable
        .map((el) => el.netProfit)
        .reduce((acc, curr) => acc + curr, 0)
})

const assets = computed(() => {
    const totalPurchase = runcitworks.accumulateAllTransactions(
        currentMonthData.value.purchases
    )
    const totalSale = runcitworks.accumulateAllTransactions(
        currentMonthData.value.sales
    )
    const totalPreviousBalance = runcitworks.accumulateAllTransactions(
        currentMonthData.value.previous_balances
    )

    return runcitworks.calculateAssets(
        totalPurchase,
        totalSale,
        totalProfit.value,
        totalPreviousBalance
    )
})

const prevProfitBalance = computed(() => currentMonthData.value.profit_balance)

const cashBalance = computed(() => {
    return (
        currentMonthData.value.starting_modal -
        assets.value +
        netProfit.value -
        cashOut.value +
        prevProfitBalance.value
    )
})

const totalHutang = computed(() => {
    return 0
})

const cashInHand = computed(() => cashBalance.value - totalHutang.value)

const grossProfit = computed(() => totalProfit.value)

const totalExpenses = computed(() => {
    return currentMonthData.value.expenses
        .map((expense) => parseFloat(expense.unit_price) * expense.quantity)
        .reduce((acc, curr) => acc + curr, 0)
})
const netProfit = computed(() => grossProfit.value - totalExpenses.value)

const cashOut = computed(() => currentMonthData.value.cashout)

const profitBalance = computed(
    () => netProfit.value + prevProfitBalance.value - cashOut.value
)

// template refs

const isError = ref(false)

const isEditingModal = ref(false)
const startingModalInput = ref<HTMLInputElement | null>(null)
const updModal = ref(startingModal.value)

const isEditingCashOut = ref(false)
const cashOutInput = ref<HTMLInputElement | null>(null)
const updCashOut = ref(cashOut.value)

// template functions

const dbClickModal = function () {
    isEditingModal.value = !isEditingModal.value
    setTimeout(() => {
        if (!startingModalInput.value) return
        startingModalInput.value.focus()
        startingModalInput.value.select()
    }, 10)
}

const dbclickCashOut = function () {
    isEditingCashOut.value = !isEditingCashOut.value
    setTimeout(() => {
        if (!cashOutInput.value) return
        cashOutInput.value.focus()
        cashOutInput.value.select()
    }, 10)
}

const updateStartingModal = async function () {
    isEditingModal.value = !isEditingModal.value
    const id = currentMonthData.value.id
    const data = {
        starting_modal: updModal.value,
    }
    const [res, err] = await destructureAxios(
        axios.patch(`/api/v1/monthdatas/${id}`, data, config)
    )
    if (res) {
        monthdata.updateStartingModal(id, updModal.value)
        toast.success(
            'Starting Modal Updated!',
            'Starting modal updated successfully.'
        )
        return
    }
    // else
    toast.error(
        'Starting Modal Update Failed',
        `Something went wrong, ${err.data.response}`
    )
}

const updateCashOut = async function () {
    isEditingCashOut.value = !isEditingCashOut.value
    const id = currentMonthData.value.id
    const data = {
        cashout: updCashOut.value,
    }
    const [res, err] = await destructureAxios(
        axios.patch(`/api/v1/monthdatas/${id}`, data, config)
    )
    if (res) {
        monthdata.updateCashout(id, updCashOut.value)
        toast.success(
            'Starting Modal Updated!',
            'Starting modal updated successfully.'
        )
        return
    }
    // else
    toast.error(
        'Starting Modal Update Failed',
        `Something went wrong, ${err.data.response}`
    )
}
</script>

<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm">
                <table id="cash-balance" class="table text-light">
                    <thead>
                        <th colspan="2" scope="row">
                            <h1 class="text-orange">Cash Balance</h1>
                        </th>
                    </thead>
                    <tbody>
                        <tr>
                            <th scope="row">Starting Modal</th>
                            <template v-if="!isEditingModal">
                                <td @dblclick="dbClickModal">
                                    RM {{ startingModal }}
                                    <i
                                        @click="dbClickModal"
                                        class="fas fa-pencil-alt"
                                    ></i>
                                </td>
                            </template>
                            <template v-else>
                                <td>
                                    <span>RM </span>
                                    <input
                                        ref="startingModalInput"
                                        class="dbclick-text"
                                        type="text"
                                        v-model="updModal"
                                        @keyup.enter="updateStartingModal"
                                        @keyup.esc="
                                            isEditingModal = !isEditingModal
                                        "
                                    />
                                </td>
                            </template>
                        </tr>
                        <tr>
                            <th scope="row">Assets</th>
                            <td>
                                <span>RM {{ assets.toFixed(2) }}</span>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">Quicktrack</th>
                            <td>
                                <span>RM {{ totalHutang }}</span>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">Cash in Hand</th>
                            <td>
                                <span>RM {{ cashInHand.toFixed(2) }}</span>
                            </td>
                        </tr>
                        <tr>
                            <th scope="row">Cash Balance</th>
                            <td>
                                <span>RM {{ cashBalance.toFixed(2) }}</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="col-sm">
                <table class="table text-light">
                    <thead>
                        <th colspan="2" scope="col">
                            <h1 class="text-orange">Profit Sheet</h1>
                        </th>
                    </thead>
                    <tbody>
                        <tr>
                            <th scope="row">Gross Profit</th>
                            <td>RM {{ grossProfit.toFixed(2) }}</td>
                        </tr>
                        <tr>
                            <th scope="row">Net Profit</th>
                            <td>RM {{ netProfit.toFixed(2) }}</td>
                        </tr>
                        <tr>
                            <th scope="row">Previous Balance</th>
                            <td>RM {{ prevProfitBalance.toFixed(4) }}</td>
                        </tr>
                        <tr>
                            <th scope="row">Cash Out</th>
                            <template v-if="!isEditingCashOut">
                                <td @dblclick="dbclickCashOut">
                                    RM {{ cashOut }}
                                    <i
                                        @click="dbclickCashOut"
                                        class="fas fa-pencil-alt"
                                    ></i>
                                </td>
                            </template>
                            <template v-else>
                                <td>
                                    <span>RM </span>
                                    <input
                                        ref="cashOutInput"
                                        class="dbclick-text"
                                        type="text"
                                        v-model="updCashOut"
                                        @keyup.enter="updateCashOut"
                                        @keyup.esc="
                                            isEditingCashOut = !isEditingCashOut
                                        "
                                    />
                                </td>
                            </template>
                        </tr>

                        <tr>
                            <th scope="row">Profit Balance</th>
                            <td>RM {{ profitBalance.toFixed(4) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<style scoped>
.fas:hover {
    cursor: pointer;
}
</style>
