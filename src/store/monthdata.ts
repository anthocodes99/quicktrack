import axios from 'axios'

import { ref } from 'vue'

import { defineStore } from 'pinia'

import { destructureAxios } from '../utils/utils'
import { useStore } from '.'
import { useToast } from '../composables/toast'

// types
import {
    RawMonthdata,
    Monthdata,
    Transaction,
    TransactionType,
} from '../models/monthdata'

export const useMonthdataStore = defineStore('monthdata', () => {
    // initialzation
    const store = useStore()
    const toast = useToast()

    // local states
    const config = {
        headers: {
            'X-CSRFToken': store.csrftoken,
        },
    }

    // states
    const monthdatas = ref<Monthdata[]>([])
    const isInitialized = ref(false)

    // local functions
    function updateMonthdata(id: number, updMonthdata: Monthdata) {
        let monthdata = monthdatas.value.find((monthdata) => monthdata.id == id)
        if (!monthdata) return
        const idx = monthdatas.value.indexOf(monthdata)
        monthdatas.value[idx] = updMonthdata
    }

    function numerifyMonthdata(updMonthdata: RawMonthdata) {
        // backend serializes decimal into string type
        // I decided to process the data first so we don't
        // have to do it later
        return {
            id: updMonthdata.id,
            month: updMonthdata.month,
            products: updMonthdata.products,
            sales: updMonthdata.sales,
            expenses: updMonthdata.expenses,
            purchases: updMonthdata.purchases,
            previous_balances: updMonthdata.previous_balances,
            user: updMonthdata.user,
            starting_modal: parseFloat(updMonthdata.starting_modal),
            cashout: parseFloat(updMonthdata.cashout),
            profit_balance: parseFloat(updMonthdata.profit_balance),
        }
    }

    // actions
    function addTransaction(type: TransactionType, transaction: Transaction) {
        const month = monthdatas.value.find(
            (monthdata) => monthdata.id == transaction.monthdata
        )
        if (!month) return
        // FIXME: Fix this special case smelly code
        // API to serialize to previousbalances instead of previous_balances
        const chk =
            type == TransactionType.PreviousBalance ? 'previous_balances' : type
        month[chk].push(transaction)
    }

    function deleteTransaction(
        type: TransactionType,
        transaction: Transaction
    ) {
        const monthdata = monthdatas.value.find(
            (monthdata) => monthdata.id == transaction.monthdata
        )
        if (!monthdata) return
        // FIXME: Fix this special case smelly code
        // API to serialize to previousbalances instead of previous_balances
        const chk =
            type == TransactionType.PreviousBalance ? 'previous_balances' : type
        const idx = monthdata[chk].indexOf(transaction)
        if (idx == -1) return
        monthdata[chk].splice(idx, 1)
    }

    async function hydrateMonthdata(id: number) {
        // Since MonthDataList does not provide transactions,
        // we have to "hydrate" the Month by retrieving from db.
        const [res, err] = await destructureAxios(
            axios.get(`/api/v1/monthdatas/${id}`, config)
        )
        if (res) {
            updateMonthdata(id, numerifyMonthdata(res.data))
            return
        }
        // else
        toast.error(
            'Failed to retrieve data.',
            Object.values(err.response.data)
        )
    }

    async function initMontdatas() {
        const [res, error] = await destructureAxios(
            axios.get('/api/v1/monthdatas', config)
        )
        if (res) {
            monthdatas.value = res.data
            // In case of a new user.
            if (res.data[0] === undefined) return
            const [mdres, mderr] = await destructureAxios(
                axios.get(`/api/v1/monthdatas/${res.data[0].id}`, config)
            )
            if (mdres) {
                updateMonthdata(mdres.data.id, numerifyMonthdata(mdres.data))
                isInitialized.value = true
                return
            }
            //else
            toast.error('Failed to retrieve data', mderr.data)
            return
        }
        // else
        toast.error('Failed to retrieve data.', error.data)
    }

    function updateStartingModal(monthId, amount) {
        const updMonth = monthdatas.value.find((month) => month.id == monthId)
        if (!updMonth) return
        updMonth.starting_modal = amount
        // updateMonthdata(monthId, updMonth)
    }

    function updateCashout(monthId, amount) {
        const updMonth = monthdatas.value.find((month) => month.id == monthId)
        if (!updMonth) return
        updMonth.cashout = amount
        // updateMonthdata(monthId, updMonth)
    }

    return {
        monthdatas,
        isInitialized,
        addTransaction,
        deleteTransaction,
        initMontdatas,
        hydrateMonthdata,
        updateStartingModal,
        updateCashout,
    }
})
