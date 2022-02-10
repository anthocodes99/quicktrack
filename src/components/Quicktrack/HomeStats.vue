<script setup lang="ts">
import { computed } from 'vue'
import { useQuicktrackStore } from '../../store/quicktrack'

const quicktrack = useQuicktrackStore()

const totalHutang = computed(() =>
    quicktrack.accounts
        .map((acc) => acc.hutang)
        .reduce((acc, curr) => acc + curr, 0)
)

const highestHutangAmount = computed(() => {
    if (quicktrack.accounts.length === 0) return
    return quicktrack.accounts
        .map((acc) => acc.hutang)
        .reduce((acc, curr) => Math.max(acc, curr), 0)
})

const highestHutangUser = computed(() => {
    if (quicktrack.accounts.length === 0) return

    return quicktrack.accounts.find(
        (acc) => acc.hutang === highestHutangAmount.value
    )?.username
})
</script>

<template>
    <div class="container-sm col-lg-5 col-md-7 col-sm-12 mt-5 border border-2">
        <h2>Stats</h2>
        <h5 data-test="total-hutang">Total Hutang: RM {{ totalHutang }}</h5>
        <h5 data-test="highest-hutang">
            Person with highest hutang :
            {{
                quicktrack.accounts.length === 0
                    ? 'N/A'
                    : highestHutangUser + ' with RM ' + highestHutangAmount
            }}
        </h5>
    </div>
</template>

<style scoped></style>
