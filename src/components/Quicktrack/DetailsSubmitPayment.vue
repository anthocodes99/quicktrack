<script setup lang="ts">
import BaseButton from '../../primitives/BaseButton.vue'

const emits = defineEmits<{ (e: 'submitPayment', event): void }>()
</script>

<template>
    <div class="bg-[#1d1f21] p-4 rounded-lg border border-[#4b5457]">
        <form @submit.prevent="$emit('submitPayment', $event)" class="">
            <h2 class="text-2xl mb-2">Payment</h2>
            <label for="submitPayment" class="text-gray-400 text-lg"
                >Amount</label
            >
            <input
                type="number"
                class="block mt-2 p-2 rounded w-48"
                id="submitPayment"
                name="paymentAmount"
                value="0"
                step="0.0001"
                required
            />
            <BaseButton class="mt-8 font-semibold" type="submit"
                >Pay</BaseButton
            >
        </form>
    </div>
</template>

<style></style>
