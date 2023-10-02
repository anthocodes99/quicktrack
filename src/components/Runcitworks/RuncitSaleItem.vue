<script setup lang="ts">
interface Props {
    id: string
    accountName: String
    description: String
    formattedAmount: string
}
const props = defineProps<Props>()
</script>

<template>
    <li class="flex items-center justify-between my-2 py-1 border-b">
        <div>
            <h3 class="text-xl text-gray-200">
                {{ accountName ?? '----------' }}
            </h3>
            <span class="text-sm text-gray-500">{{ description }}</span>
        </div>
        <div>
            <h3 class="text-xl text-gray-200">{{ formattedAmount }}</h3>
        </div>
    </li>
</template>

<style scoped></style>
