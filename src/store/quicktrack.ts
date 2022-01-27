import axios from 'axios'

import { ref } from 'vue'

import { defineStore } from 'pinia'

import { destructureAxios } from '../utils/utils'
import { useStore } from '.'
import { useToast } from '../composables/toast'

export const useQuicktrackStore = defineStore('quicktrack', () => {
    // initialization
    const store = useStore()
    const toast = useToast()

    // states
    const accounts = ref([])

    // actions
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
            accounts.value = res.data
            return
        }
        // else
        toast.error('Failed to retrieve data.', error.response.data)
    }
    return {
        accounts,
        initAccounts,
    }
})
