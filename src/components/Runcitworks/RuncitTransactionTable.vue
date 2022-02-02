<script setup lang="ts">
import { Transaction, TransactionType } from '../../models/monthdata'

import { useStore } from '../../store'
import { useToast } from '../../composables/toast'
import { useMonthdataStore } from '../../store/monthdata'
import { destructureAxios } from '../../utils/utils'
import axios from 'axios'

interface Props {
    transactions: Transaction[]
    currentMonthId: number
    type: TransactionType
    products: string[]
}

const props = defineProps<Props>()

const store = useStore()
const toast = useToast()
const monthdataStore = useMonthdataStore()

const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

const submitTransaction = async function (event) {
    const formData = Object.fromEntries(new FormData(event.target))
    let data = {}
    if (props.type == TransactionType.Expense) {
        data = {
            monthdata: props.currentMonthId,
            date: formData.date,
            description: formData.description,
            unit_price: formData.unitprice,
            quantity: formData.quantity,
        }
    } else {
        // sale / purchase / previousbalance
        data = {
            monthdata: props.currentMonthId,
            date: formData.date,
            product: formData.product,
            unit_price: formData.unitprice,
            quantity: formData.quantity,
        }
    }
    const [res, err] = await destructureAxios(
        axios.post(`/api/v1/${props.type}`, data, config)
    )
    if (res) {
        monthdataStore.addTransaction(props.type, res.data)
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

const deleteTransaction = async function (transaction) {
    const [res, err] = await destructureAxios(
        axios.delete(`/api/v1/${props.type}/${transaction.id}`, config)
    )
    if (res) {
        monthdataStore.deleteTransaction(props.type, transaction)
        toast.success(
            'Transaction deleted.',
            'Transaction deleted successfully.'
        )
        return
    }
    // else
    toast.error(
        'Failed to delete transaction.',
        `Did not successfully delete transaction. ${Object.values(
            err.response.data
        )}`
    )
}
</script>

<template>
    <form @submit.prevent="submitTransaction">
        <table class="table">
            <thead>
                <tr>
                    <th class="">#</th>
                    <th class="col-1">Date</th>
                    <!-- Product if Purchase/Sales, 'Description' if Expenses -->
                    <th class="col-4">
                        {{ type != 'expenses' ? 'Product' : 'Description' }}
                    </th>
                    <th class="col-2">Unit Price</th>
                    <th class="col-2">Quantity</th>
                    <th class="col-2">Amount</th>
                    <!-- Same here, doesnt' show account if not Purchases/Sales -->
                    <th colspan="2" class="col-2" v-if="type != 'expenses'">
                        Account
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="(transaction, idx) in transactions"
                    :key="transaction.id"
                >
                    <th scope="row">
                        {{ idx + 1 }}
                    </th>
                    <td>{{ transaction.date }}</td>
                    <td>
                        {{
                            type != 'expenses'
                                ? transaction.product
                                : transaction.description
                        }}
                    </td>
                    <td>
                        RM {{ parseFloat(transaction.unit_price).toFixed(2) }}
                    </td>
                    <td>{{ transaction.quantity }} packs</td>
                    <td>
                        RM
                        {{
                            (
                                parseFloat(transaction.unit_price) *
                                transaction.quantity
                            ).toFixed(2)
                        }}
                    </td>
                    <!-- Same deal, doesn't list it -->
                    <td v-if="type != 'expenses'">
                        {{ transaction.account || '---------' }}
                    </td>
                    <td>
                        <i
                            @click="deleteTransaction(transaction)"
                            class="fas fa-backspace"
                            style="color: #fff"
                        ></i>
                    </td>
                </tr>
                <tr>
                    <th></th>
                    <td>
                        <input
                            class="form-control"
                            type="date"
                            name="date"
                            id="transaction-date"
                            required
                            v-if="type != 'previousbalances'"
                        />
                    </td>

                    <!-- select field if Purchases/Sales, otherwise just a text field-->
                    <td v-if="type != 'expenses'">
                        <select
                            class="form-select"
                            name="product"
                            id="transaction-product"
                        >
                            <option disabled value="">--Choose--</option>
                            <option
                                v-for="(product, idx) in products"
                                :key="idx"
                                :value="product"
                            >
                                {{ product }}
                            </option>
                        </select>
                    </td>
                    <td v-else>
                        <input
                            class="form-control"
                            name="description"
                            id="transaction-description"
                            type="text"
                        />
                    </td>

                    <td>
                        <input
                            class="form-control"
                            type="number"
                            name="unitprice"
                            id="transaction-unit-price"
                            step="0.01"
                            required
                        />
                    </td>
                    <td>
                        <input
                            class="form-control"
                            type="number"
                            name="quantity"
                            id="transaction-quantity"
                            required
                        />
                    </td>
                    <!-- Basically removing this field if it's expenses -->
                    <td v-if="type != 'expenses'"></td>
                    <td colspan="2">
                        <button class="btn btn-success" type="submit">
                            Submit
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </form>
</template>

<style scoped>
.fas:hover {
    cursor: pointer;
}
</style>
