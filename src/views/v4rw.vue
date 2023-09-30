<script setup lang="ts">
import RuncitAddMonthModal from '../components/Runcitworks/RuncitAddMonthModal.vue'

import { useMonthdataStore } from '../store/monthdata'

import { ref, onMounted, watch, computed } from 'vue'

import { useToast } from '../composables/toast'
import { useProgressBar } from '../composables/progressbar'

import { Monthdata } from '../models/monthdata'

import { useQuicktrackStore } from '../store/quicktrack'

import CompositeNav from '../components/CompositeNav.vue'
import { useRuncitworks } from '../composables/runcitworks'

// Composables
const toast = useToast()
const progressBar = useProgressBar()
const monthdataStore = useMonthdataStore()
const quicktrack = useQuicktrackStore()

// Template refs
const monthdatas = computed(() => monthdataStore.monthdatas)
const isNewMonthDialogOpen = ref(false)
// const isInitialized = computed(() => monthdataStore.isInitialized)
const isInitialized = ref(false)
const monthChosen = ref('')
const currentMonthdata = ref<Monthdata>()

// Template functions
function updateMonth(month: string) {
    monthChosen.value = month
}

// Watches
watch(monthChosen, async (newMonth) => {
    const idx = monthdatas.value
        .map((monthdata) => monthdata.month)
        .indexOf(newMonth)
    if (idx == -1) {
        toast.error(
            'Failed to retrieve selected month!',
            'Please contact administrator.'
        )
        return
    }
    // else
    if (!monthdatas.value[idx].sales) {
        isInitialized.value = false
        await monthdataStore.hydrateMonthdata(monthdatas.value[idx].id)
    }
    // finally
    currentMonthdata.value = monthdatas.value[idx]
    isInitialized.value = true
})

// actions
progressBar.initProgress(30)
onMounted(async () => {
    progressBar.addProgress(30)
    if (monthdatas.value.length === 0) {
        await monthdataStore.initMontdatas()
    }
    if (quicktrack.accounts.length === 0) {
        await quicktrack.initAccounts()
    }

    // In case of a new user(with no monthdatas)
    if (monthdatas.value.length !== 0)
        monthChosen.value = monthdatas.value[0].month
    // finally
    progressBar.addProgress(40)
    isInitialized.value = true
})

const balance = computed(() => {
    if (currentMonthdata.value === undefined) return []
    const runcitworks = useRuncitworks(currentMonthdata)
    interface TableProduct {
        product: string
        balance: number
    }
    const table: TableProduct[] = []
    currentMonthdata.value.products.forEach((product) => {
        table.push({
            product: product,
            balance: runcitworks.getCurrentBalanceByProduct(product),
        })
    })
    return table
})
</script>

<template>
    <CompositeNav>
        <template v-if="!isInitialized">
            <div
                class="w-full sm:max-w-md sm:mx-auto md:mx-0 pt-32 items-center"
            >
                <div class="flex justify-center" role="status">
                    <svg
                        aria-hidden="true"
                        class="w-16 h-16 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                        viewBox="0 0 100 101"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                            fill="currentColor"
                        />
                        <path
                            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                            fill="currentFill"
                        />
                    </svg>
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
        </template>
        <!-- v-else-if="monthdata.length = 0" -->
        <template v-else>
            <RuncitAddMonthModal
                :currentMonthData="currentMonthdata"
                :monthdatas="monthdatas"
                :isNewMonthDialogOpen="isNewMonthDialogOpen"
                @close="isNewMonthDialogOpen = false"
            />
            <main class="w-full sm:max-w-lg md:mx-0 pt-4 px-4">
                <!-- Monthdata Select Field -->
                <div class="flex justify-between">
                    <label class="text-2xl text-white" for="monthdata-selector">
                        Month
                    </label>
                    <div>
                        <button @click="isNewMonthDialogOpen = true">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="32"
                                height="32"
                                fill="none"
                            >
                                <g clip-path="url(#a)">
                                    <path
                                        fill="#E94F37"
                                        d="M0 8a8 8 0 0 1 8-8h16a8 8 0 0 1 8 8v16a8 8 0 0 1-8 8H8a8 8 0 0 1-8-8V8Z"
                                    />
                                    <path
                                        fill="#fff"
                                        d="M25.333 17.333h-8v8h-2.666v-8h-8v-2.666h8v-8h2.666v8h8v2.666Z"
                                    />
                                </g>
                            </svg>
                        </button>
                    </div>
                </div>
                <select
                    class="block mt-2 w-4/6 mx-auto py-2 text-center text-lg rounded-md"
                    v-model="monthChosen"
                    id="monthdata-selector"
                >
                    <option
                        v-for="monthdata in monthdatas"
                        :value="monthdata.month"
                        :key="monthdata.id"
                    >
                        {{ monthdata.month }}
                    </option>
                </select>
                <router-view
                    class="mt-4"
                    :currentMonthdata="currentMonthdata"
                ></router-view>
            </main>
        </template>
    </CompositeNav>
</template>

<style scoped></style>
