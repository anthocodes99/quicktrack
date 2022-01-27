<script setup lang="ts">
import { computed } from '@vue/runtime-core'
import { useProgressBar } from '../composables/progressbar'

const progressBar = useProgressBar()

const progress = computed(() => progressBar.state.progress.value)
const isLoading = computed(() => progressBar.state.isLoading.value)
</script>

<template>
    <div
        class="progress bg-gray-dark"
        :class="{ 'is-loading': isLoading }"
        style="background-color: var(--bs-gray-dark); height: 2px"
    >
        <div
            class="progress-bar"
            role="progressbar"
            :style="{ width: `${progress}%` }"
            aria-valuenow="25"
            aria-valuemin="0"
            aria-valuemax="100"
        ></div>
    </div>
</template>

<style scoped>
.progress {
    /* background-color: transparent !important; */
    opacity: 0 !important;
    transition: opacity 0.4s linear 0.4s !important;
    z-index: 99999;
}
.progress-bar {
    transition: width 0.4s ease;
}
.is-loading {
    opacity: 1 !important;
    transition: none !important;
}
</style>
