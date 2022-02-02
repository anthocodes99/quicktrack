<script setup lang="ts">
import { Monthdata, TransactionType } from '../../models/monthdata'
import RuncitTransactionTable from './RuncitTransactionTable.vue'

interface Props {
    currentMonthData: Monthdata
}

const props = defineProps<Props>()
</script>

<template>
    <h1>Previous Balances</h1>
    <RuncitTransactionTable
        :transactions="currentMonthData.previous_balances ?? []"
        :currentMonthId="currentMonthData.id"
        :type="TransactionType.PreviousBalance"
        :products="currentMonthData.products"
    />
</template>

<style scoped></style>
