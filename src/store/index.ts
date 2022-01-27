import { defineStore } from 'pinia'

export const useStore = defineStore('index', {
    state: () => ({
        username: '',
        isLoggedIn: false,
        csrftoken: '',
    }),
    actions: {},
})
