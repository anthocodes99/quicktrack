import axios from 'axios'

import { ref, toDisplayString } from 'vue'

import { defineStore } from 'pinia'

import { destructureAxios } from '../utils/utils'
import { useStore } from '.'
import { useToast } from '../composables/toast'

// types
import { Monthdata, Transaction, TransactionType } from '../models/monthdata'
import { propsToAttrMap } from '@vue/shared'

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

    // actions
    function addTransaction(type: TransactionType, transaction: Transaction) {
        const month = monthdatas.value.find(
            (monthdata) => monthdata.id == transaction.monthdata
        )
        if (!month) return
        month[type].push(transaction)
    }

    function deleteTransaction(
        type: TransactionType,
        transaction: Transaction
    ) {
        const monthdata = monthdatas.value.find(
            (monthdata) => monthdata.id == transaction.monthdata
        )
        if (!monthdata) return
        const idx = monthdata[type].indexOf(transaction)
        if (idx == -1) return
        monthdata[type].splice(idx, 1)
    }

    async function hydrateMonthdata(id: number) {
        // Since MonthDataList does not provide transactions,
        // we have to "hydrate" the Month by retrieving from db.
        const [res, err] = await destructureAxios(
            axios.get(`/api/v1/monthdatas/${id}`, config)
        )
        if (res) {
            updateMonthdata(id, res.data)
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
            const [mdres, mderr] = await destructureAxios(
                axios.get(`/api/v1/monthdatas/${res.data[0].id}`, config)
            )
            if (mdres) {
                updateMonthdata(mdres.data.id, mdres.data)
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

    return {
        monthdatas,
        isInitialized,
        addTransaction,
        deleteTransaction,
        initMontdatas,
        hydrateMonthdata,
    }
})
