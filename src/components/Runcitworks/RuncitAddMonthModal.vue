<script setup lang="ts">
import axios from 'axios'
import { Modal } from 'bootstrap'
import { toRefs } from 'vue'
import { useRuncitworks } from '../../composables/runcitworks'

import { useToast } from '../../composables/toast'
import { Monthdata, RawMonthdata } from '../../models/monthdata'
import { useStore } from '../../store'
import { useMonthdataStore } from '../../store/monthdata'
import { destructureAxios } from '../../utils/utils'

interface Props {
    monthdatas: Monthdata[]
    currentMonthData: Monthdata
}
const props = defineProps<Props>()
const { currentMonthData } = toRefs(props)

const emit = defineEmits<{ (e: 'updateMonth', month: string): void }>()

// init
const toast = useToast()
const store = useStore()
const monthdata = useMonthdataStore()
const runcitworks = useRuncitworks(currentMonthData)

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

const addMonth = async function (event) {
    // close the modal
    const monthModal = Modal.getInstance(document.getElementById('addMonth'))
    monthModal.hide()

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

    // obtains Product from the desired port month
    const products: string[] = []
    const data = {
        month: `${year}-${months.indexOf(month) + 1}-01`,
        starting_modal: formData.startingModal,
        profit_balance: formData.profitBalance,
        products,
    }

    const { previousbalancemonth } = formData
    // I decided that this is the better choice
    const targetMonthdata = monthdata.monthdatas.find(
        (monthdata) => monthdata.month == previousbalancemonth
    )

    if (previousbalancemonth !== '') {
        if (targetMonthdata === undefined)
            return toast.error('Error!', 'targetMonthdata is undefined.')

        data['products'] = targetMonthdata.products
    }

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
    if (previousbalancemonth !== '') {
        let productResponses: any[] = []
        for (const product of targetMonthdata!.products) {
            const productCurrentBalance =
                runcitworks.getCurrentBalanceByProduct(product)

            const productUnitPrice = runcitworks.getPurchaseUnitPrice(product)

            if (isNaN(productUnitPrice)) continue

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
    }
    monthdata.$patch({
        monthdatas: [updMonthdata, ...monthdata.monthdatas],
    })
    toast.success(
        'New month created.',
        `Created new month ${updMonthdata.month}`
    )
    emit('updateMonth', updMonthdata.month)
}
</script>

<template>
    <div class="modal" id="addMonth" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content bg-dark">
                <div class="modal-header">
                    <h5 class="modal-title text-warning">Create a new Month</h5>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <form action="" @submit.prevent="addMonth">
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-5">
                                <label
                                    class="form-label text-light"
                                    for="addMonthDate"
                                    >Select a Month</label
                                >
                                <select class="form-select" name="month" id="">
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
                            <div class="col-md-5">
                                <label class="form-label text-light" for="year"
                                    >Year</label
                                >
                                <select
                                    class="form-select"
                                    id="year"
                                    name="year"
                                >
                                    <option selected>2021</option>
                                    <option>2022</option>
                                    <option>2023</option>
                                    <option>2024</option>
                                    <option>2025</option>
                                    <option>2026</option>
                                </select>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-5">
                                <label
                                    class="form-label text-light"
                                    for="startingModal"
                                    >Starting Modal</label
                                >
                                <input
                                    class="form-control"
                                    type="number"
                                    name="startingModal"
                                    id="startingModal"
                                    value="0"
                                />
                            </div>
                            <div class="col-md-5">
                                <label
                                    class="form-label text-light"
                                    for="profitBalance"
                                    >Previous Profit Balance</label
                                >
                                <input
                                    class="form-control"
                                    type="number"
                                    name="profitBalance"
                                    id="profitBalance"
                                    step="0.0001"
                                    value="0"
                                />
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-5">
                                <label
                                    class="form-label text-light"
                                    for="previousbalancemonth"
                                    >Port from Previous Balance</label
                                >
                                <select
                                    class="form-select"
                                    name="previousbalancemonth"
                                >
                                    <option value="">None</option>
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
                    </div>
                    <div class="modal-footer">
                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                        >
                            Close
                        </button>
                        <button class="btn btn-primary" type="submit">
                            Save changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
