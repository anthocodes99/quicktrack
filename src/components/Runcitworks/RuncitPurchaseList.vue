<script setup lang="ts">
import RuncitPurchaseItem from './RuncitPurchaseItem.vue'

interface RuncitPurchaseList {
    date: string
    purchases: RuncitPurchase[]
}

interface RuncitPurchase {
    id: string
    productName: string
    description: string
    formattedAmount: string
}

interface Props {
    purchaseList: RuncitPurchaseList[]
}
const props = defineProps<Props>()
</script>

<template>
    <ul class="flex-auto flex-col items-center">
        <li v-for="day in purchaseList" :key="day.date">
            <h4 class="text-2xl text-center text-white">{{ day.date }}</h4>
            <template v-for="purchase in day.purchases">
                <RuncitPurchaseItem v-bind="purchase" />
            </template>
        </li>
    </ul>
</template>

<style scoped></style>
