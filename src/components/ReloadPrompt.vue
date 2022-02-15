<script setup lang="ts">
import { useRegisterSW } from 'virtual:pwa-register/vue'
import { useToast } from '../composables/toast'

const toast = useToast()

const { offlineReady, needRefresh, updateServiceWorker } = useRegisterSW()

const close = async () => {
    offlineReady.value = false
    needRefresh.value = false
}

console.log({ offlineReady }, { needRefresh })

if (offlineReady.value) {
    toast.info('App Ready', 'App is ready to work offline')
}
if (needRefresh.value) {
    const buttons = [
        {
            btnText: 'Update',
            btnStatus: 'btn-primary',
            btnCb: updateServiceWorker,
        },
    ]
    toast.info(
        'New Update Available',
        'Click on Reload button to Update.',
        buttons,
        20000
    )
}
</script>

<template></template>

<style></style>
