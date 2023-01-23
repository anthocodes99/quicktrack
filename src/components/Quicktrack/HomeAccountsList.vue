<script setup lang="ts">
import { Account } from '../../models/quicktrack'
import router from '../../router'
interface Props {
    accounts: Account[]
}

const props = defineProps<Props>()

const routeChange = function (id: number) {
    router.push({ name: 'QuicktrackDetails', params: { id } })
}
</script>

<template>
    <h2 class="text-3xl pt-2 px-2">Accounts</h2>
    <ul>
        <template v-for="account in accounts" :key="account.id">
            <li
                class="flex justify-between border-b py-2 px-4 cursor-pointer"
                @click="routeChange(account.id)"
            >
                <span class="text-2xl">{{ account.username }}</span>
                <span class="text-xl text-gray-500">{{
                    account.hutang.toFixed(2)
                }}</span>
            </li>
        </template>
    </ul>
</template>

<style scoped></style>
