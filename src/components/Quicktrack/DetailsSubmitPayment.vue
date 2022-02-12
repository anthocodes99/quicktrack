<script setup lang="ts">
const emits = defineEmits<{ (e: 'submitPayment', event): void }>()
</script>

<template>
    <div class="container-xxl col-xl-7 border border-2 mt-2 py-2">
        <form @submit.prevent="$emit('submitPayment', $event)" class="row g-3">
            <h2>Payment</h2>
            <label for="submitPayment" class="form-label my-0">Payment</label>
            <div class="col-8 mt-0">
                <input
                    type="number"
                    class="form-control bg-gray"
                    id="submitPayment"
                    name="paymentAmount"
                    required
                />
            </div>
            <div class="col-4 mt-0">
                <input
                    type="submit"
                    class="btn btn-success text-wrap"
                    style="width: 100%"
                    value="Make Payment"
                />
            </div>
        </form>
    </div>
</template>

<style></style>
