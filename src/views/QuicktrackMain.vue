<script setup lang="ts">
import TheNavbar from '../components/TheNavbar.vue'
import { computed, onMounted, ref } from 'vue'
import { useQuicktrackStore } from '../store/quicktrack'
import { useProgressBar } from '../composables/progressbar'
import HomeUserList from '../components/Quicktrack/HomeUserList.vue'
import HomeAddUser from '../components/Quicktrack/HomeAddUser.vue'
import HomeStats from '../components/Quicktrack/HomeStats.vue'
import { useMonthdataStore } from '../store/monthdata'

const quicktrack = useQuicktrackStore()
const monthdata = useMonthdataStore()
const progressBar = useProgressBar()

const accounts = computed(() => quicktrack.accounts)
// const isInitialized = computed(() => quicktrack.isInitialized)
const isInitialized = ref(false)

// initialize progress bar
progressBar.initProgress(30)

onMounted(async () => {
    progressBar.addProgress(30)
    if (accounts.value.length === 0) {
        const res = await quicktrack.initAccounts()
    }
    if (monthdata.monthdatas.length === 0) {
        await monthdata.initMontdatas()
    }
    // finally
    progressBar.addProgress(40)
    isInitialized.value = true
})
</script>

<template>
    <TheNavbar />
    <div v-if="!isInitialized">
        <h1>Loading...</h1>
    </div>
    <div v-else>
        <HomeUserList :accounts="accounts" />
        <HomeAddUser />
        <HomeStats />
    </div>
</template>

<style scoped></style>
