<script setup lang="ts">
import { toRefs, computed } from 'vue'
import { useRuncitworks } from '../../composables/runcitworks'

import { Monthdata, Transaction } from '../../models/monthdata'

import { useQuicktrackStore } from '../../store/quicktrack'

interface CurrentBalance {
    product: string
    balance: number
}

interface Props {
    currentMonthdata: Monthdata
}

interface PerformanceTableItem {
    product: string
    unitProfit: number
    netProfit: number
}

const props = defineProps<Props>()
const quicktrack = useQuicktrackStore()

// FIXME: fix this vodoo
const { currentMonthdata: currentMonthData } = toRefs(props)
const runcitworks = useRuncitworks(currentMonthData)
// TODO: business logic
const currentBalanceList = computed<CurrentBalance[]>(() => {
    const balanceList: CurrentBalance[] = []
    for (const product of currentMonthData.value.products) {
        balanceList.push({
            product,
            balance: runcitworks.getCurrentBalanceByProduct(product),
        })
    }
    return balanceList
})

const recentSalesList = computed<Transaction[]>(() => {
    return currentMonthData.value.sales.filter((sale) => {
        // TODO: refactor this
        const saleDate = new Date(sale.date).getDate()
        const threeDaysAgo = new Date()
        threeDaysAgo.setDate(threeDaysAgo.getDay() - 3)
        return saleDate > threeDaysAgo.getDate()
    })
})

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

const cashOut = computed(() => currentMonthData.value.cashout)

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
    return quicktrack.accounts
        .map((acc) => acc.hutang)
        .reduce((acc, curr) => acc + curr, 0)
})

const pettyCash = computed(() => cashBalance.value - totalHutang.value)

const totalExpenses = computed(() => {
    return currentMonthData.value.expenses
        .map((expense) => parseFloat(expense.unit_price) * expense.quantity)
        .reduce((acc, curr) => acc + curr, 0)
})

const netProfit = computed(() => totalProfit.value - totalExpenses.value)
</script>

<template>
    <!-- Product Current Balance -->
    <div class="flex flex-col gap-4">
        <div class="border-2 p-2 border-white rounded-md">
            <h2 class="text-2xl">Current Balance</h2>
            <ul>
                <template
                    v-for="item in currentBalanceList"
                    :key="item.product"
                >
                    <li
                        class="flex items-center justify-between my-2 py-1 border-b border-gray-200"
                    >
                        <div>
                            <span class="text-xl text-gray-200">{{
                                item.product
                            }}</span>
                        </div>
                        <div>
                            <span class="text-xl text-gray-200"
                                >{{ item.balance }} pcs</span
                            >
                        </div>
                    </li>
                </template>
            </ul>
        </div>
        <div class="border-2 p-2 border-white rounded-md">
            <!-- TODO: router link to sales -->
            <div class="flex justify-between">
                <h2 class="text-2xl">Recent Sales</h2>
                <h3 class="text-gray-600 text-sm items-end">Past 3 Days</h3>
            </div>
            <!-- Recent Sales will default to past 3 days for now. -->
            <ul>
                <template v-for="item in recentSalesList" :key="item.product">
                    <li
                        class="flex items-center justify-between my-2 py-1 border-b border-gray-200"
                    >
                        <div class="flex flex-col">
                            <span class="text-xl text-gray-200">{{
                                item.account
                            }}</span>
                            <span class="text-md text-gray-500"
                                >{{ item.product }} x {{ item.quantity }} @ RM
                                {{
                                    // TODO: exorcise this demon
                                    parseInt(item.unit_price).toFixed(2)
                                }}
                                ea</span
                            >
                            <span>{{ item.date }}</span>
                        </div>
                        <div>
                            <span class="text-xl text-gray-200"
                                >RM
                                {{
                                    (
                                        item.quantity *
                                        parseInt(item.unit_price)
                                    ).toFixed(2)
                                }}</span
                            >
                        </div>
                    </li>
                </template>
            </ul>
        </div>
        <div class="grid grid-cols-2 gap-4">
            <div class="border-2 p-2 border-white rounded-md">
                <h2 class="text-2xl">Net Profit (MTD)</h2>
                <span class="text-xl text-gray-200">{{
                    `RM ${netProfit.toFixed(2)}`
                }}</span>
            </div>
            <div class="border-2 p-2 border-white rounded-md">
                <h2 class="text-2xl">Assets</h2>
                <span class="text-xl text-gray-200">{{
                    `RM ${assets.toFixed(2)}`
                }}</span>
            </div>
            <div class="border-2 p-2 border-white rounded-md">
                <h2 class="text-2xl">Petty Cash</h2>
                <span class="text-xl text-gray-200">{{
                    `RM ${pettyCash.toFixed(2)}`
                }}</span>
            </div>
            <div class="border-2 p-2 border-white rounded-md">
                <h2 class="text-2xl">Hutang</h2>
                <span class="text-xl text-gray-200">{{
                    `RM ${totalHutang.toFixed(2)}`
                }}</span>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
