<script setup lang="ts">
interface CurrentBalance {
    product: string
    balance: number
}

interface Props {
    currentBalanceList: CurrentBalance[]
}

/*

*/

const props = defineProps<Props>()
</script>

<template>
    <!-- Product Current Balance -->
    <div>
        <h2 class="text-2xl">Current Balance</h2>
        <ul>
            <template v-for="item in currentBalanceList" :key="item.product">
                <li
                    class="flex items-center justify-between my-2 py-1 border-b"
                >
                    <div>
                        <span class="text-xl text-gray-200">{{
                            item.product
                        }}</span>
                    </div>
                    <div>
                        <span class="text-xl text-gray-200"
                            >{{ item.balance }} PCs</span
                        >
                    </div>
                </li>
            </template>
        </ul>
    </div>
    <div class="mt-8">
        <h2 class="text-2xl">Earning This Month</h2>
        <span class="text-2xl text-gray-200">RM 800</span>
    </div>
    <div class="mt-8">
        <h2 class="text-2xl">Cash In Hand</h2>
        <span class="text-2xl text-gray-200">RM 569</span>
    </div>
</template>

<style scoped></style>
