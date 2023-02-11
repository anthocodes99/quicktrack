<script setup lang="ts">
import { ref, computed, onMounted, toRef } from 'vue'
import RuncitExpenseList from '../../components/Runcitworks/RuncitExpenseList.vue'
import { useMonthdataStore } from '../../store/monthdata'

import { Monthdata } from '../../models/monthdata'
import { useTransactionParser } from '../../composables/transactionParser'

interface Props {
    currentMonthdata: Monthdata
}

const runcitPurchase = {
    id: 'uuid-test',
    productName: 'Cinnamoroll',
    description: '12 pcs @ RM 4.00',
    formattedAmount: 'RM 48.00',
}

const props = defineProps<Props>()

const currentMonthdata = toRef(props, 'currentMonthdata')

const monthdataStore = useMonthdataStore()
const sortByDate = useTransactionParser()

const expensesList = computed(() => {
    const table: any = []
    currentMonthdata.value.expenses.forEach((expense) => {
        table.push({
            // the date attribute will be brought down
            // as a side effect of sortByDate.
            date: expense.date,
            id: expense.id,
            productName: expense.description,
            // description format
            // X pc(s) @ RM Y.YY
            description: `${expense.quantity} pc${
                expense.quantity > 0 ? 's' : ''
            } @ RM ${(+expense.unit_price).toFixed(2)}`,
            // RM Z.ZZ
            formattedAmount: `RM ${(+expense.unit_price).toFixed(2)}`,
        })
    })
    return sortByDate.sortTransactionsByDate(table)
})

onMounted(() => {
    console.log(expensesList.value)
})
</script>

<template>
    <div>
        <h2 class="text-4xl">Expenses</h2>
        <template v-if="expensesList.length == 0">
            <h3 class="text-2xl text-white text-center mt-12">No expenses~</h3>
        </template>
        <template v-else>
            <RuncitExpenseList :expensesList="expensesList" />
        </template>
    </div>
</template>

<style scoped></style>
