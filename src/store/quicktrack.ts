import axios from 'axios'

import { ref } from 'vue'

import { defineStore } from 'pinia'

import { Account, RawAccount } from '../models/quicktrack'

import { destructureAxios } from '../utils/utils'
import { useStore } from '.'
import { useToast } from '../composables/toast'

export const useQuicktrackStore = defineStore('quicktrack', () => {
    // initialization
    const store = useStore()
    const toast = useToast()

    // states
    const accounts = ref<Account[]>([])

    // utility functions
    const numerifyAccount = function (account: RawAccount) {
        return {
            ...account,
            hutang: parseFloat(account.hutang),
        }
    }

    // actions
    function addAccount(newAcc: RawAccount) {
        accounts.value.push(numerifyAccount(newAcc))
    }

    async function initAccounts() {
        console.log('initAccounts() called')
        const config = {
            headers: {
                'X-CSRFToken': store.csrftoken,
            },
        }
        const [res, error] = await destructureAxios(
            axios.get('/api/accounts', config)
        )
        if (res) {
            let updAccounts: Account[] = []
            for (const account of res.data) {
                updAccounts.push(numerifyAccount(account))
            }
            accounts.value = updAccounts
            return
        }
        // else
        toast.error('Failed to retrieve data.', error.response.data)
    }
    return {
        accounts,
        addAccount,
        initAccounts,
    }
})
