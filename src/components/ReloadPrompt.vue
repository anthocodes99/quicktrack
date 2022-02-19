<script setup lang="ts">
import { useRegisterSW } from 'virtual:pwa-register/vue'
import { watch, watchEffect } from 'vue'
import { useToast } from '../composables/toast'

const toast = useToast()

const { offlineReady, needRefresh, updateServiceWorker } = useRegisterSW()

const close = async () => {
    offlineReady.value = false
    needRefresh.value = false
}

console.log({ offlineReady }, { needRefresh })

watch(offlineReady, (curr, prev) => {
    if (curr) toast.info('App Ready', 'App is ready to work offline')
})

watch(needRefresh, (curr, prev) => {
    if (curr) {
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
})
</script>

<template>
    <div></div>
</template>

<style></style>
