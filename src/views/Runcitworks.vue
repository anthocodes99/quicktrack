<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'

import { useToast } from '../composables/toast'
import { useProgressBar } from '../composables/progressbar'
import { useMonthdataStore } from '../store/monthdata'

import { Monthdata } from '../models/monthdata'

import TheNavbar from '../components/TheNavbar.vue'
import RuncitAddMonthModal from '../components/Runcitworks/RuncitAddMonthModal.vue'
import RuncitPurchaseSales from '../components/Runcitworks/RuncitPurchaseSales.vue'
import RuncitExpenses from '../components/Runcitworks/RuncitExpenses.vue'
import RuncitPreviousBalances from '../components/Runcitworks/RuncitPreviousBalances.vue'
import RuncitCurrentBalance from '../components/Runcitworks/RuncitCurrentBalance.vue'
import RuncitCashFlow from '../components/Runcitworks/RuncitCashFlow.vue'
import RuncitSetup from '../components/Runcitworks/RuncitSetup.vue'
import { useQuicktrackStore } from '../store/quicktrack'

// Composables
const toast = useToast()
const progressBar = useProgressBar()
const monthdataStore = useMonthdataStore()
const quicktrack = useQuicktrackStore()

// Template refs
const monthdatas = computed(() => monthdataStore.monthdatas)
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
</script>

<template>
    <TheNavbar />
    <div class="overflow-auto">
        <div class="container-xxl col-lg-7 con-min-md">
            <RuncitAddMonthModal
                :monthdatas="monthdatas"
                :currentMonthData="currentMonthdata"
                @updateMonth="updateMonth"
            />
            <header class="container-xxl row">
                <div class="col">
                    <h1>Runcit Works</h1>
                </div>
                <div class="col">
                    <div class="row">
                        <div class="col-1 d-flex align-items-center">
                            <button
                                type="button"
                                class="btn btn-primary"
                                data-bs-toggle="modal"
                                data-bs-target="#addMonth"
                            >
                                <i class="fas fa-plus pointer"></i>
                            </button>
                        </div>
                        <div class="col-11">
                            <select
                                class="form-select mt-2"
                                v-model="monthChosen"
                                name="month"
                                id="month-select"
                            >
                                <option
                                    v-for="monthdata in monthdatas"
                                    :value="monthdata.month"
                                    :key="monthdata.id"
                                >
                                    {{ monthdata.month }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </header>
            <nav>
                <div class="nav nav-tabs" id="nav-tab" role="tablist">
                    <button
                        class="nav-link active text-light bg-dark"
                        id="nav-home-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#nav-home"
                        type="button"
                        role="tab"
                        aria-controls="nav-home"
                        aria-selected="true"
                    >
                        Purchases and Sales
                    </button>
                    <button
                        class="nav-link text-light bg-dark"
                        id="nav-expenses-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#nav-expenses"
                        type="button"
                        role="tab"
                        aria-controls="nav-expenses"
                        aria-selected="false"
                    >
                        Expenses
                    </button>
                    <button
                        class="nav-link text-light bg-dark"
                        id="nav-profile-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#nav-profile"
                        type="button"
                        role="tab"
                        aria-controls="nav-profile"
                        aria-selected="false"
                    >
                        Previous Balance
                    </button>
                    <button
                        class="nav-link text-light bg-dark"
                        id="nav-contact-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#nav-contact"
                        type="button"
                        role="tab"
                        aria-controls="nav-contact"
                        aria-selected="false"
                    >
                        Current Balance
                    </button>
                    <button
                        class="nav-link text-light bg-dark"
                        id="nav-cash-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#nav-cash"
                        type="button"
                        role="tab"
                        aria-controls="nav-cash"
                        aria-selected="false"
                    >
                        Cash Flow
                    </button>
                    <button
                        class="nav-link text-light bg-dark"
                        id="nav-setup-tab"
                        data-bs-toggle="tab"
                        data-bs-target="#nav-setup"
                        type="button"
                        role="tab"
                        aria-controls="nav-setup"
                        aria-selected="false"
                    >
                        Setup
                    </button>
                </div>
            </nav>
            <template v-if="!isInitialized">
                <div class="d-flex justify-content-center">
                    <div
                        class="spinner-border text-primary mt-5"
                        style="width: 3rem; height: 3rem"
                        role="status"
                    >
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </template>
            <template v-else-if="monthdatas.length == 0">
                <div class="pt-5">
                    <h1 class="text-center fs-3">
                        You haven't initialized a month yet !
                    </h1>
                    <p class="text-center lead">
                        Click on the plus(+) above to add a new month.
                    </p>
                </div>
            </template>
            <template v-else>
                <div class="tab-content" id="nav-tabContent">
                    <div
                        class="tab-pane fade show active"
                        id="nav-home"
                        role="tabpanel"
                        aria-labelledby="nav-home-tab"
                    >
                        <RuncitPurchaseSales
                            :curr_monthdata="currentMonthdata!"
                        />
                    </div>
                    <div
                        class="tab-pane fade"
                        id="nav-expenses"
                        role="tabpanel"
                        aria-labelledby="nav-expenses-tab"
                    >
                        <RuncitExpenses :currentMonthData="currentMonthdata!" />
                    </div>
                    <div
                        class="tab-pane fade"
                        id="nav-profile"
                        role="tabpanel"
                        aria-labelledby="nav-profile-tab"
                    >
                        <RuncitPreviousBalances
                            :currentMonthData="currentMonthdata!"
                        />
                    </div>
                    <div
                        class="tab-pane fade"
                        id="nav-contact"
                        role="tabpanel"
                        aria-labelledby="nav-contact-tab"
                    >
                        <RuncitCurrentBalance
                            :currentMonthData="currentMonthdata!"
                        />
                    </div>
                    <div
                        class="tab-pane fade"
                        id="nav-cash"
                        role="tabpanel"
                        aria-labelledby="nav-contact-tab"
                    >
                        <RuncitCashFlow :currentMonthData="currentMonthdata!" />
                    </div>
                    <div
                        class="tab-pane fade"
                        id="nav-setup"
                        role="tabpanel"
                        aria-labelledby="nav-contact-tab"
                    >
                        <RuncitSetup
                            :currentMonthData="currentMonthdata!"
                            :userProducts="monthdataStore.userProducts"
                        />
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped>
.con-min-md {
    min-width: 768px;
}
.pointer {
    cursor: pointer;
}
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

/* Firefox */
input[type='number'] {
    -moz-appearance: textfield;
}
</style>
