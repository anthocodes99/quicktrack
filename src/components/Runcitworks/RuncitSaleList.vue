<script setup lang="ts">
import RuncitSaleItem from './RuncitSaleItem.vue'

interface RuncitSaleList {
    date: string
    sales: RuncitSale[]
}

interface RuncitSale {
    id: string
    accountName: string
    description: string
    formattedAmount: string
}

interface Props {
    saleList: RuncitSaleList[]
}
const props = defineProps<Props>()
</script>

<template>
    <ul class="flex-auto flex-col items-center">
        <li v-for="day in saleList" :key="day.date">
            <h4 class="text-2xl text-center text-white">{{ day.date }}</h4>
            <template v-for="sale in day.sales">
                <RuncitSaleItem v-bind="sale" />
            </template>
        </li>
    </ul>
</template>

<style scoped></style>
