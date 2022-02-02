<script setup lang="ts">
import { Monthdata, TransactionType } from '../../models/monthdata'
import RuncitTransactionTable from './RuncitTransactionTable.vue'

interface Props {
    curr_monthdata: Monthdata
}

const props = defineProps<Props>()
</script>

<template>
    <h1 class="mt-2">Purchases</h1>
    <RuncitTransactionTable
        :transactions="curr_monthdata.purchases ?? []"
        :currentMonthId="curr_monthdata.id"
        :type="TransactionType.Purchase"
        :products="curr_monthdata.products"
    />
    <h1 class="">Sales</h1>
    <RuncitTransactionTable
        :transactions="curr_monthdata.sales ?? []"
        :currentMonthId="curr_monthdata.id"
        :type="TransactionType.Sale"
        :products="curr_monthdata.products"
    />
</template>

<style scoped></style>
