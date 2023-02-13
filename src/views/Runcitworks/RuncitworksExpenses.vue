<script setup lang="ts">
import { ref, computed, onMounted, toRef } from 'vue'
import RuncitExpenseList from '../../components/Runcitworks/RuncitExpenseList.vue'
import { useMonthdataStore } from '../../store/monthdata'

import { Monthdata } from '../../models/monthdata'
import { useTransactionParser } from '../../composables/transactionParser'
import BaseInput from '../../primitives/BaseInput.vue'
import BaseButton from '../../primitives/BaseButton.vue'

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

const revealAddForm = ref(false)

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
        <div class="flex justify-between">
            <h2 class="text-4xl pb-4">Expenses</h2>
            <div class="flex gap-2">
                <BaseButton
                    class="w-12 h-12"
                    @click="revealAddForm = !revealAddForm"
                    >add</BaseButton
                >
                <BaseButton class="w-12 h-12">del</BaseButton>
            </div>
        </div>
        <form
            class="bg-dark-700 p-4 rounded-lg border border-dark-400"
            v-if="revealAddForm"
            @submit.prevent=""
        >
            <div class="">
                <label class="text-gray-400 text-lg" for="date">Date</label>
                <BaseInput type="date" id="date" class="h-10 w-48" />
            </div>
            <div class="mt-4">
                <label class="text-gray-400 text-lg" for="description"
                    >Description</label
                >
                <BaseInput type="text" id="description" class="h-10 w-48" />
            </div>
            <div class="mt-4">
                <label class="text-gray-400 text-lg" for="unit_price"
                    >Unit Price</label
                >
                <BaseInput type="number" id="unit_price" class="h-10 w-48" />
            </div>
            <div class="mt-4">
                <label class="text-gray-400 text-lg" for="quantity"
                    >Quantity</label
                >
                <BaseInput
                    type="number"
                    step="1"
                    id="quantity"
                    class="h-10 w-48"
                />
            </div>
            <div class="mt-4">
                <BaseButton>Create Expense</BaseButton>
            </div>
        </form>
        <template v-if="expensesList.length == 0">
            <h3 class="text-2xl text-white text-center mt-12">No expenses~</h3>
        </template>
        <template v-else>
            <RuncitExpenseList class="mt-8" :expensesList="expensesList" />
        </template>
    </div>
</template>

<style scoped></style>
