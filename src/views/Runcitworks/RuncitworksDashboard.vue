<script setup lang="ts">
interface CurrentBalance {
    product: string
    balance: number
}

interface Props {
    currentBalanceList: CurrentBalance[]
}

/*

*/

const props = defineProps<Props>()
// TODO: business logic
const currentBalanceList = [
    { product: 'cinnamoroll', balance: 5 },
    { product: 'cinnamoroll', balance: 5 },
    { product: 'cinnamoroll', balance: 5 },
]

const recentSalesList = [
    {
        id: 1,
        product: 'cinnamoroll',
        account: 'ironmouse',
        quantity: 4,
        unit_price: 12.0,
    },
    {
        id: 2,
        product: 'cinnamoroll',
        account: 'ironmouse',
        quantity: 2,
        unit_price: 12.0,
    },
    {
        id: 2,
        product: 'cinnamoroll',
        account: 'ironmouse',
        quantity: 1,
        unit_price: 12.0,
    },
]
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
            <h2 class="text-2xl">Recent Sales</h2>
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
                                {{ item.unit_price.toFixed(2) }} ea</span
                            >
                        </div>
                        <div>
                            <span class="text-xl text-gray-200"
                                >RM
                                {{
                                    (item.quantity * item.unit_price).toFixed(2)
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
                <span class="text-xl text-gray-200">RM 56.64</span>
            </div>
            <div class="border-2 p-2 border-white rounded-md">
                <h2 class="text-2xl">Assets</h2>
                <span class="text-xl text-gray-200">RM 81.20</span>
            </div>
            <div class="border-2 p-2 border-white rounded-md">
                <h2 class="text-2xl">Petty Cash</h2>
                <span class="text-xl text-gray-200">RM 134.00</span>
            </div>
            <div class="border-2 p-2 border-white rounded-md">
                <h2 class="text-2xl">Hutang</h2>
                <span class="text-xl text-gray-200">RM 349.00</span>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
