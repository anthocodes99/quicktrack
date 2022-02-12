<script setup lang="ts">
interface Props {
    products: string[]
}

interface Context {
    date: string
    product: string
    unitPrice: number
    quantity: number
}

const props = defineProps<Props>()
const emit = defineEmits<{ (e: 'submitSale', context: Context): void }>()

const submitSale = function (event) {
    const formData = Object.fromEntries(new FormData(event.target))
    const context = {
        date: formData.date,
        product: formData.product,
        unitPrice: parseFloat(formData.unitPrice),
        quantity: parseInt(formData.quantity),
    }
    emit('submitSale', context)
}
</script>

<template>
    <div class="container-xxl border border-2 mt-2 py-1">
        <form action="" @submit.prevent="submitSale">
            <h2>Custom Input</h2>
            <div class="row g-3">
                <div class="col">
                    <label for="date">Date</label>
                    <input
                        class="form-control"
                        type="date"
                        name="date"
                        required
                    />
                </div>
                <div class="col">
                    <label for="product">Product</label>
                    <select class="form-select" name="product">
                        <option v-for="(product, idx) in products" :key="idx">
                            {{ product }}
                        </option>
                    </select>
                </div>
                <div class="col">
                    <label for="unitPrice">Unit Price</label>
                    <input
                        class="form-control"
                        type="number"
                        name="unitPrice"
                        step="0.0001"
                        placeholder="Unit Price"
                        required
                    />
                </div>
                <div class="col">
                    <label for="quantity">Quantity</label>
                    <input
                        class="form-control"
                        type="number"
                        name="quantity"
                        placeholder="Quantity"
                        required
                    />
                </div>
            </div>
            <div class="row p-2">
                <input
                    type="submit"
                    class="btn btn-success"
                    value="Make Sale"
                />
            </div>
        </form>
    </div>
</template>

<style scoped></style>
-
