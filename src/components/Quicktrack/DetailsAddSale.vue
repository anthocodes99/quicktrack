<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from '../../primitives/BaseButton.vue'

interface Props {
    products: string[]
}

const props = defineProps<Props>()
const selectedProduct = ref('')
</script>

<template>
    <form>
        <label class="text-gray-400 text-lg" for="product">Product </label>
        <fieldset>
            <legend class="sr-only">Product</legend>
            <div class="grid grid-cols-2 gap-4 pt-2">
                <template v-for="product in products" :key="product">
                    <label
                        class="group relative border rounded-md py-3 px-4 flex items-center justify-center text-sm font-medium uppercase hover:bg-[#1b1d1e] sm:flex-1 active:ring-2 active:ring-[#E94F37] bg-[#181a1b] shadow-sm text-[#d6d3cd] cursor-pointer checked:border-[#E94F37] checked:border-2"
                    >
                        <input
                            type="radio"
                            name="product"
                            class="sr-only"
                            :value="product"
                            aria-labelledby="size-choice-0-label"
                            v-model="selectedProduct"
                        />
                        <span id="size-choice-0-label">{{ product }}</span>
                        <span
                            class="border-2"
                            :class="[
                                selectedProduct === product
                                    ? 'border-[#E94F37]'
                                    : 'border-transparent',
                                'pointer-events-none absolute -inset-px rounded-md',
                            ]"
                            aria-hidden="true"
                        />
                    </label>
                </template>
            </div>
        </fieldset>
        <div class="pt-4">
            <label class="text-gray-400 text-lg" for="date">Date</label>
            <input
                class="block mt-2 p-2 rounded w-48"
                type="date"
                name="date"
                :value="new Date().toISOString().split('T')[0]"
                id=""
            />
        </div>
        <div class="pt-4">
            <label class="text-gray-400 text-lg" for="unitprice"
                >Unit Price</label
            >
            <input
                class="block mt-2 p-2 rounded w-48"
                type="number"
                name="unitprice"
                step="0.0001"
                value="0.0000"
                id=""
            />
        </div>
        <div class="pt-4">
            <label class="text-gray-400 text-lg" for="Quantity">Quantity</label>
            <input
                class="block mt-2 p-2 rounded w-48"
                type="number"
                name="quantity"
                step="1"
                value="1"
                id=""
            />
        </div>

        <BaseButton class="mt-8 font-semibold" type="submit"
            >Add Sale</BaseButton
        >
    </form>
</template>

<style scoped></style>
