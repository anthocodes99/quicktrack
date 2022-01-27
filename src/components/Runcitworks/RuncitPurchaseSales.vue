<script setup lang="ts">
import { Monthdata, TransactionType } from '../../models/monthdata'
import RuncitTransactionTable from './RuncitTransactionTable.vue'

interface Props {
    curr_monthdata: Monthdata
}

const props = defineProps<Props>()
</script>

<template>
    <h3 class="text-orange mt-2">Purchases</h3>
    <RuncitTransactionTable
        :transactions="curr_monthdata.purchases ?? []"
        :currentMonthId="curr_monthdata.id"
        :type="TransactionType.Purchases"
        :products="curr_monthdata.products"
    />
    <h3 class="text-orange">Sales</h3>
    <RuncitTransactionTable
        :transactions="curr_monthdata.sales ?? []"
        :currentMonthId="curr_monthdata.id"
        :type="TransactionType.Sales"
        :products="curr_monthdata.products"
    />
</template>

<style scoped></style>
