<script setup lang="ts">
import axios from 'axios'
import { Modal } from 'bootstrap'
import { toRefs, ref } from 'vue'
import { useRuncitworks } from '../../composables/runcitworks'

import { useToast } from '../../composables/toast'
import { Monthdata, RawMonthdata } from '../../models/monthdata'
import { useStore } from '../../store'
import { useMonthdataStore } from '../../store/monthdata'
import { destructureAxios } from '../../utils/utils'

interface Props {
    monthdatas: Monthdata[]
    isNewMonthDialogOpen: Boolean
    currentMonthData: Monthdata
}
const props = defineProps<Props>()
const { currentMonthData } = toRefs(props)

const emit = defineEmits<{
    (e: 'updateMonth', month: string): void
    (e: 'close'): void
}>()

// init
const toast = useToast()
const store = useStore()
const monthdata = useMonthdataStore()
const runcitworks = useRuncitworks(currentMonthData)

const portFromPreviousMonthCheckbox = ref(false)

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

const portFromPreviousMonth = async function () {}

const addMonth = async function (event) {
    // close the modal

    const formData = Object.fromEntries(new FormData(event.target))
    const { year, month } = formData
    const months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
    ]

    // check if we're on portFromPreviousMonth mode
    if (portFromPreviousMonthCheckbox.value == true) {
        const previousMonthdata = props.monthdatas.find(
            (monthdata) => monthdata.month === formData.portmonthselector
        )
        if (previousMonthdata === undefined) {
            return toast.error(
                'Error!',
                'Monthdata does not exist. Please refresh the page and try again.'
            )
        }
        // work with date
        const previousMonthDate = new Date(previousMonthdata.month)
        // data is setup as such
        // month : 1 month after selected month
        // starting modal, profit balance, products to follow previous month
        const data = {
            month: `${previousMonthDate.getFullYear()}-0${
                // MONTH STARTS FROM 0 :<
                previousMonthDate.getMonth() + 2
            }-01`,
            starting_modal: previousMonthdata.starting_modal,
            profit_balance: previousMonthdata.profit_balance,
            products: previousMonthdata.products,
        }
        // POST to CREATE a monthdata
        const [res, err] = await destructureAxios(
            axios.post('/api/v1/monthdatas', data, config)
        )

        if (err) {
            toast.error(
                'Failed to add new Month!',
                'Did not successfully add month.'
            )
            return
        }
        let updMonthdata = res.data
        let productResponses: any[] = []
        for (const product of previousMonthdata!.products) {
            const productCurrentBalance =
                runcitworks.getCurrentBalanceByProduct(product)

            const productUnitPrice = runcitworks.getPurchaseUnitPrice(product)

            if (isNaN(productUnitPrice)) {
                toast.warning('Warning!', `${product} is NaN! Skipping...`)
                continue
            }

            // post the backend
            const productData = {
                monthdata: res.data.id, // new month
                product,
                unit_price: productUnitPrice.toFixed(4),
                quantity: productCurrentBalance,
            }

            const [productRes, productErr] = await destructureAxios(
                axios.post(`/api/v1/previousbalances`, productData, config)
            )

            if (productRes) {
                productResponses.push(productRes)
                continue
            }
            //else
            toast.error(
                'An error occured.',
                'An error occured while applying previous balance.'
            )
        }
        updMonthdata = {
            previous_balances: productResponses.map((res) => res.data),
            ...res.data,
        }
        monthdata.$patch({
            monthdatas: [updMonthdata, ...monthdata.monthdatas],
        })
        toast.success(
            'New month created.',
            `Created new month ${updMonthdata.month}`
        )
        emit('updateMonth', updMonthdata.month)
    } else {
        // data is setup as a blank slate
        const products: string[] = []
        const data = {
            // again, indexof starts from 0, so month needs
            // a single nudge to work
            month: `${year}-${months.indexOf(month) + 1}-01`,
            starting_modal: formData.startingModal,
            profit_balance: formData.profitBalance,
            products,
        }
        // POST to CREATE a monthdata
        const [res, err] = await destructureAxios(
            axios.post('/api/v1/monthdatas', data, config)
        )

        if (err) {
            toast.error(
                'Failed to add new Month!',
                'Did not successfully add month.'
            )
            return
        }
        //else
        let updMonthdata = res.data
        monthdata.$patch({
            monthdatas: [updMonthdata, ...monthdata.monthdatas],
        })
        toast.success(
            'New month created.',
            `Created new month ${updMonthdata.month}`
        )
        emit('updateMonth', updMonthdata.month)
    }
    emit('close')
}
</script>

<template>
    <div
        class="relative z-10"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
        v-show="isNewMonthDialogOpen"
        @click.
    >
        <div
            class="fixed inset-0 bg-gray-800 bg-opacity-75 transition-opacity"
            @click="$emit('close')"
        ></div>

        <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
            <div
                class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
            >
                <form
                    class="relative transform overflow-hidden rounded-lg bg-dark-700 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg min-w-full sm:min-w-min"
                    @submit.prevent="addMonth"
                >
                    <div
                        class="bg-dark-600 px-4 pb-4 pt-5 sm:p-6 sm:pb-4 grid grid-cols-1 sm:grid-cols-2 gap-6"
                    >
                        <div class="flex flex-col gap-y-2 w-full">
                            <label for="month" class="text-white">Month</label>
                            <select
                                class="p-2 rounded-md"
                                name="month"
                                id="month"
                                :disabled="portFromPreviousMonthCheckbox"
                            >
                                <option selected>January</option>
                                <option>February</option>
                                <option>March</option>
                                <option>April</option>
                                <option>May</option>
                                <option>June</option>
                                <option>July</option>
                                <option>August</option>
                                <option>September</option>
                                <option>October</option>
                                <option>November</option>
                                <option>December</option>
                            </select>
                        </div>
                        <div class="flex flex-col gap-y-2">
                            <label class="text-white" for="year">Year</label>
                            <select
                                class="p-2 rounded-md"
                                id="year"
                                name="year"
                                :disabled="portFromPreviousMonthCheckbox"
                            >
                                <option selected>2021</option>
                                <option>2022</option>
                                <option>2023</option>
                                <option>2024</option>
                                <option>2025</option>
                                <option>2026</option>
                            </select>
                        </div>
                        <div class="flex flex-col gap-y-2">
                            <label class="text-white" for="startingModal"
                                >Starting Modal</label
                            >
                            <input
                                class="rounded-md p-2"
                                type="number"
                                name="startingModal"
                                id="startingModal"
                                value="0"
                                :disabled="portFromPreviousMonthCheckbox"
                            />
                        </div>
                        <div class="flex flex-col gap-y-2">
                            <label class="text-white" for="profitBalance"
                                >Previous Profit Balance</label
                            >
                            <input
                                class="rounded-md p-2"
                                type="number"
                                name="profitBalance"
                                id="profitBalance"
                                step="0.0001"
                                value="0"
                                :disabled="portFromPreviousMonthCheckbox"
                            />
                        </div>
                        <div class="flex flex-row gap-y-2 items-center">
                            <label
                                for="portfrompreviousmonth"
                                class="text-white"
                            >
                                Port from Previous Month
                            </label>
                            <div class="inline-flex items-center">
                                <label
                                    class="relative flex cursor-pointer items-center rounded-full p-3"
                                    for="checkbox"
                                    data-ripple-dark="true"
                                >
                                    <input
                                        type="checkbox"
                                        class="before:content[''] peer relative h-5 w-5 cursor-pointer appearance-none rounded-md border border-blue-gray-200 transition-all before:absolute before:top-2/4 before:left-2/4 before:block before:h-12 before:w-12 before:-translate-y-2/4 before:-translate-x-2/4 before:rounded-full before:bg-blue-gray-500 before:opacity-0 before:transition-opacity checked:border-pink-500 checked:bg-pink-500 checked:before:bg-pink-500 hover:before:opacity-10"
                                        name="portfrompreviousmonth"
                                        id="portfrompreviousmonth"
                                        v-model="portFromPreviousMonthCheckbox"
                                    />
                                    <div
                                        class="pointer-events-none absolute top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 text-white opacity-0 transition-opacity peer-checked:opacity-100"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            class="h-3.5 w-3.5"
                                            viewBox="0 0 20 20"
                                            fill="currentColor"
                                            stroke="currentColor"
                                            stroke-width="1"
                                        >
                                            <path
                                                fill-rule="evenodd"
                                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                clip-rule="evenodd"
                                            ></path>
                                        </svg>
                                    </div>
                                </label>
                            </div>
                        </div>
                        <div class="flex flex-col gap-y-2">
                            <label for="portmonthselector" class="text-white">
                                Month
                            </label>
                            <select
                                name="portmonthselector"
                                id="portmonthselector"
                                class="rounded-md p-2"
                                :disabled="!portFromPreviousMonthCheckbox"
                            >
                                <option selected>--------</option>
                                <option
                                    v-for="month in monthdatas"
                                    :key="month.id"
                                    :value="month.month"
                                >
                                    {{ month.month }}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div
                        class="bg-dark-600 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6"
                    >
                        <button
                            type="submit"
                            class="inline-flex w-full justify-center rounded-md bg-green-600 px-3 py-2 text-sm font-semibold text-gray-200 shadow-sm hover:bg-green-500 sm:ml-3 sm:w-auto"
                        >
                            Create New Month
                        </button>
                        <button
                            type="button"
                            class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-200 sm:mt-0 sm:w-auto"
                            @click="$emit('close')"
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
