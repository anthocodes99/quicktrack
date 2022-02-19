<script setup lang="ts">
import { Account } from '../../models/quicktrack'

interface Props {
    account: Account
}

const props = defineProps<Props>()
</script>

<template>
    <h2>Recent Sales</h2>
    <ul>
        <li v-for="sale in account.recent_sales" :key="sale.id">
            {{ sale.date }} : {{ sale.product }} | RM
            {{ parseFloat(sale.unit_price) * sale.quantity }}
            <em>
                <span class="text-muted px-2"
                    >({{ sale.quantity }} pcs @ RM
                    {{ parseFloat(sale.unit_price).toFixed(2) }})</span
                ></em
            >
        </li>
    </ul>
</template>

<style scoped></style>
