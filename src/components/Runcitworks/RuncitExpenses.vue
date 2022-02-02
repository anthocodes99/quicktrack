<script setup lang="ts">
import { Monthdata, TransactionType } from '../../models/monthdata'
import RuncitTransactionTable from './RuncitTransactionTable.vue'

interface Props {
    currentMonthData: Monthdata
}

const props = defineProps<Props>()
</script>

<template>
    <h1>Expenses</h1>
    <RuncitTransactionTable
        :transactions="currentMonthData.expenses ?? []"
        :currentMonthId="currentMonthData.id"
        :type="TransactionType.Expense"
        :products="currentMonthData.products"
    />
</template>

<style scoped></style>
