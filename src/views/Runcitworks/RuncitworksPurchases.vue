<script setup lang="ts">
import RuncitPurchaseList from '../../components/Runcitworks/RuncitPurchaseList.vue'

import { ref, computed, onMounted, toRef } from 'vue'
import { useMonthdataStore } from '../../store/monthdata'

import { Monthdata } from '../../models/monthdata'
import { useTransactionParser } from '../../composables/transactionParser'
import BaseInput from '../../primitives/BaseInput.vue'
import BaseButton from '../../primitives/BaseButton.vue'
import { destructureAxios } from '../../utils/utils'
import axios from 'axios'
import { useStore } from '../../store'
import { useToast } from '../../composables/toast'

import { TransactionType } from '../../models/monthdata'

interface Props {
    currentMonthdata: Monthdata
}

const props = defineProps<Props>()

const revealAddForm = ref(false)

const currentMonthdata = toRef(props, 'currentMonthdata')

const store = useStore()
const toast = useToast()
const monthdataStore = useMonthdataStore()
const sortByDate = useTransactionParser()

const todayString = () => {
    // this is an abomination
    // following codes literally generates
    // 2023-09-02
    //         ^ only put 0 IF single digit.
    // why? is there no other way?
    const today = new Date()
    const todayString = `${today.getFullYear()}-0${today.getMonth()}-${
        today.getDate() % 10 == today.getDate() ? '0' : ''
    }${today.getDate()}`
    console.log(todayString)
    return todayString
}

const purchaseList = computed(() => {
    const table: any = []
    currentMonthdata.value.purchases.forEach((sale) => {
        table.push({
            // the date attribute will be brought down
            // as a side effect of sortByDate.
            date: sale.date,
            id: sale.id,
            productName: sale.product,
            // description format
            // ITEM x X @ RM Y.YY ea
            description: `${sale.product} x ${
                sale.quantity
            } @ RM ${(+sale.unit_price).toFixed(2)} ea`,
            // RM Z.ZZ
            formattedAmount: `RM ${(+sale.unit_price * +sale.quantity).toFixed(
                2
            )}`,
        })
    })
    return sortByDate.sortTransactionsByDate(table)
})

const createPurchase = async function (event) {
    const config = {
        headers: {
            'X-CSRFToken': store.csrftoken,
        },
    }
    const formData = Object.fromEntries(new FormData(event.target))
    const data = {
        monthdata: currentMonthdata.value.id,
        date: formData.date,
        product: formData.product,
        unit_price: formData.unit_price,
        quantity: formData.quantity,
    }

    const [res, err] = await destructureAxios(
        axios.post(`/api/v1/purchases`, data, config)
    )
    if (res) {
        monthdataStore.addTransaction(TransactionType.Purchase, res.data)
        toast.success('Transaction added!', 'Transaction added successfully.')
        return
    }
    // else
    toast.error(
        'Error!',
        `An error occured while adding transaction.\n ${Object.values(
            err.response.data
        )}`
    )
}
</script>

<template>
    <div>
        <div class="flex justify-between">
            <h2 class="text-4xl pb-4">Purchases</h2>
            <div class="flex gap-2">
                <BaseButton
                    class="w-12 h-12"
                    @click="revealAddForm = !revealAddForm"
                    >add</BaseButton
                >
                <BaseButton class="w-12 h-12">del</BaseButton>
            </div>
        </div>
        <form
            class="bg-dark-700 p-4 rounded-lg border border-dark-400"
            v-if="revealAddForm"
            @submit.prevent="createPurchase"
        >
            <div class="">
                <label class="text-gray-400 text-lg" for="date">Date</label>
                <BaseInput
                    type="date"
                    name="date"
                    id="date"
                    :value="todayString()"
                    class="h-10 w-48"
                />
            </div>
            <div class="mt-4">
                <label class="text-gray-400 text-lg" for="product"
                    >Product</label
                >
                <select
                    class="block px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none h-10 w-48"
                    name="product"
                    id="transaction-product"
                >
                    <option disabled value="">--Choose--</option>
                    <option
                        v-for="(product, idx) in currentMonthdata.products"
                        :key="idx"
                        :value="product"
                    >
                        {{ product }}
                    </option>
                </select>
            </div>
            <div class="mt-4">
                <label class="text-gray-400 text-lg" for="unit_price"
                    >Unit Price</label
                >
                <BaseInput
                    type="number"
                    name="unit_price"
                    id="unit_price"
                    step="0.0001"
                    class="h-10 w-48"
                />
            </div>
            <div class="mt-4">
                <label class="text-gray-400 text-lg" for="quantity"
                    >Quantity</label
                >
                <BaseInput
                    type="number"
                    step="1"
                    name="quantity"
                    id="quantity"
                    class="h-10 w-48"
                />
            </div>
            <div class="mt-4">
                <BaseButton type="submit">Create Purchase</BaseButton>
            </div>
        </form>
        <template v-if="purchaseList.length == 0">
            <h3 class="text-2xl text-white text-center mt-12">No Purchases~</h3>
        </template>
        <template v-else>
            <RuncitPurchaseList class="mt-8" :purchaseList="purchaseList" />
        </template>
    </div>
</template>

<style scoped></style>
