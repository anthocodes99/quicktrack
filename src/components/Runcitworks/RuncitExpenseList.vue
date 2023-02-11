<script setup lang="ts">
import RuncitExpenseItem from './RuncitExpenseItem.vue'

import { Transaction } from '../models/monthdata'

interface RuncitExpenseList {
    date: string
    transactions: Transaction[]
}

interface RuncitExpense {
    date: string
    id: string
    productName: string
    description: string
    formattedAmount: string
}

interface Props {
    expensesList: RuncitExpenseList[]
}
const props = defineProps<Props>()
</script>

<template>
    <ul class="flex-auto flex-col items-center">
        <li v-for="day in expensesList" :key="day.date">
            <h4 class="text-2xl text-center text-white">
                {{ day.date }}
            </h4>
            <template v-for="expense in day.transactions">
                <RuncitExpenseItem v-bind="expense" />
            </template>
        </li>
    </ul>
</template>

<style scoped></style>
