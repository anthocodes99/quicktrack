<script setup lang="ts">
import { Transaction } from '../../models/monthdata'
import { Account } from '../../models/quicktrack'

interface Props {
    account: Account
}

interface sortedSales {
    String: Transaction[]
}

const props = defineProps<Props>()

const sortSales = function (recent_sales: Transaction[]) {
    const sortedByDate = recent_sales.sort((a, b) => {
        // the + before new are to clear ts error.
        // https://stackoverflow.com/a/68876658/15029609
        return +new Date(b.date) - +new Date(a.date)
    })
    const sortedSales = sortedByDate.reduce((acc, curr) => {
        if (!acc[curr.date]) {
            acc[curr.date] = []
        }
        acc[curr.date].push(curr)
        return acc
    }, {})

    return sortedSales
}

const sortedSales = sortSales(props.account.recent_sales)
</script>

<template>
    <h2 class="text-2xl pt-8">Recent Sales</h2>
    <ul class="flex-auto flex-col items-center">
        <li v-for="[day, sales] of Object.entries(sortedSales)" :key="day">
            <h4 class="text-lg text-center text-white">{{ day }}</h4>
            <template v-for="sale in sales">
                <!-- <RuncitSaleItem v-bind="sale" /> -->
                <li
                    class="flex items-center justify-between my-2 py-1 border-b"
                >
                    <div>
                        <h3 class="text-md text-gray-200">
                            {{ sale.product }}
                        </h3>
                        <span class="text-sm text-gray-500"
                            >{{ sale.quantity }} pcs @ RM
                            <!-- + in front of unit_price will convert it into number -->
                            <!-- unit_price is a string -->
                            {{ (+sale.unit_price).toFixed(2) }} ea</span
                        >
                    </div>
                    <div>
                        <h3 class="text-md text-gray-200">
                            RM
                            {{ (+sale.unit_price * sale.quantity).toFixed(2) }}
                        </h3>
                    </div>
                </li>
            </template>
        </li>
        image.png
    </ul>
</template>

<style scoped></style>
