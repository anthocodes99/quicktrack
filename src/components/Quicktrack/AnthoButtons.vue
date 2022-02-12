<script setup lang="ts">
const emit = defineEmits<{
    (e: 'makeSale', name: string, unitPrice: number, quantity: number): void
}>()

const createSale = function (name, unitPrice, quantity) {
    emit('makeSale', name, unitPrice, quantity)
}
</script>

<template>
    <h3 class="text-center" style="color: #0000ff">Era Blue</h3>
    <div class="d-flex justify-content-evenly pb-2">
        <button
            class="btn-lg btn-primary"
            @click="createSale('Era Blue', 4, 1)"
        >
            RM 4
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('Era Blue', 4, 2)"
        >
            RM 8
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('Era Blue', 4, 3)"
        >
            RM 12
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('Era Blue', 3.7, 10)"
        >
            RM 37
        </button>
    </div>
    <h3 class="text-center" style="color: #009933">Era Black</h3>
    <div class="d-flex justify-content-evenly pb-2">
        <button
            class="btn-lg btn-primary"
            @click="createSale('Era Black', 4, 1)"
        >
            RM 4
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('Era Black', 4, 2)"
        >
            RM 8
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('Era Black', 4, 3)"
        >
            RM 12
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('Era Black', 3.7, 10)"
        >
            RM 37
        </button>
    </div>
    <h3 class="text-center" style="color: #0066ff">D&amp;J Ice Plus</h3>
    <div class="d-flex justify-content-evenly pb-2">
        <button
            class="btn-lg btn-primary"
            @click="createSale('D&J Ice Plus', 5, 1)"
        >
            RM 5
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('D&J Ice Plus', 5, 2)"
        >
            RM 10
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('D&J Ice Plus', 5, 3)"
        >
            RM 15
        </button>
        <button
            class="btn-lg btn-primary"
            @click="createSale('D&J Ice Plus', 4.5, 10)"
        >
            RM 45
        </button>
    </div>
</template>

<style></style>
