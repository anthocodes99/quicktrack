<script setup lang="ts">
import RuncitSaleItem from './RuncitSaleItem.vue'

interface RuncitSaleList {
    date: string
    transactions: RuncitSale[]
}

interface RuncitSale {
    id: string
    accountName: string
    description: string
    formattedAmount: string
}

interface Props {
    salesList: RuncitSaleList[]
}
const props = defineProps<Props>()
</script>

<template>
    <ul class="flex-auto flex-col items-center">
        <li v-for="day in salesList" :key="day.date">
            <h4 class="text-2xl text-center text-white">{{ day.date }}</h4>
            <template v-for="sale in day.transactions">
                <RuncitSaleItem v-bind="sale" />
            </template>
        </li>
    </ul>
</template>

<style scoped></style>
