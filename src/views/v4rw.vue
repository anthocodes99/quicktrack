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
    <div class="mx-auto max-w-lg md:max-w-xl lg:max-w-7xl">
        <NewNavbar
            class="hidden md:block fixed top-0 pt-4 px-4 xl:w-[15rem] md:w-[11rem]"
        />
        <main class="pl-[rem] mt-4">
            <div class="max-w-3xl mx-auto">
                <h3 class="text-3xl text-white">Sales</h3>
                <RuncitSaleList :saleList="runcitSaleList" />
                <h3 class="text-3xl text-white mt-12">Purchases</h3>
                <RuncitPurchaseList :purchaseList="runcitPurchaseList" />
            </div>
        </main>
        <aside
            class="hidden 2xl:block fixed top-0 right-[max(0px,calc(50%-45rem))] w-[18rem] pt-4"
        >
            <p class="text-4xl text-white">aside</p>
        </aside>
    </div>
</template>

<style scoped></style>
