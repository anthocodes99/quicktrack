<script setup lang="ts">
import TheNavbar from '../components/TheNavbar.vue'
import { computed, onMounted, ref } from 'vue'
import { useQuicktrackStore } from '../store/quicktrack'
import { useProgressBar } from '../composables/progressbar'

const quicktrack = useQuicktrackStore()
const progressBar = useProgressBar()

const accounts = computed(() => quicktrack.accounts)
// const isInitialized = computed(() => quicktrack.isInitialized)
const isInitialized = ref(false)

// initialize progress bar
progressBar.initProgress(30)

onMounted(async () => {
    progressBar.addProgress(30)
    if (accounts.value.length == 0) {
        const res = await quicktrack.initAccounts()
    }
    // finally
    progressBar.addProgress(40)
    isInitialized.value = true
})
</script>

<template>
    <TheNavbar />
    <h1>Quicktrack</h1>
    <div v-if="!isInitialized">
        <h1>Loading...</h1>
    </div>
    <div v-else>
        <ul>
            <template v-for="account in accounts" :key="account.id">
                <li>{{ account.username }} | {{ account.hutang }}</li>
            </template>
        </ul>
    </div>
</template>

<style scoped></style>
