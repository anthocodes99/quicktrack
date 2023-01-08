<script setup lang="ts">
import Logo from '../assets/logo.png'

import NewNavbar from '../components/NewNavbar.vue'

import RuncitSaleList from '../components/Runcitworks/RuncitSaleList.vue'
import RuncitPurchaseList from '../components/Runcitworks/RuncitPurchaseList.vue'

const runcitSale = {
    id: 'uuid-test',
    accountName: 'Ironmouse',
    description: 'Cinnamoroll x 1 @ RM 4.00',
    formattedAmount: 'RM 4.00',
}

const runcitSaleList = [
    { date: '12 Dec 2022', sales: [runcitSale, runcitSale, runcitSale] },
    { date: '11 Dec 2022', sales: [runcitSale, runcitSale, runcitSale] },
]

const runcitPurchase = {
    id: 'uuid-test',
    productName: 'Cinnamoroll',
    description: '12 pcs @ RM 4.00',
    formattedAmount: 'RM 48.00',
}

const runcitPurchaseList = [
    {
        date: '12 Dec 2022',
        purchases: [runcitPurchase, runcitPurchase, runcitPurchase],
    },
    {
        date: '11 Dec 2022',
        purchases: [runcitPurchase, runcitPurchase, runcitPurchase],
    },
]
</script>

<template>
    <nav class="block md:hidden mx-auto bg-[#212529] px-3 py-2">
        <div class="flex items-center justify-between">
            <span><img :src="Logo" width="32" height="32" alt="" /></span>

            <span class="text-[#3F88C5]">antho</span>
        </div>
    </nav>
    <div class="flex mx-auto md:max-w-xl lg:max-w-7xl gap-8">
        <NewNavbar class="hidden md:block" />
        <main class="flex-auto mt-4">
            <h3 class="text-3xl text-white">Sales</h3>
            <RuncitSaleList :saleList="runcitSaleList" />
            <h3 class="text-3xl text-white mt-12">Purchases</h3>
            <RuncitPurchaseList :purchaseList="runcitPurchaseList" />
        </main>
        <aside class="hidden lg:block border-2 mt-4 w-[18.5rem]">
            <p class="text-3xl text-white">stuff</p>
        </aside>
    </div>
</template>

<style scoped></style>
