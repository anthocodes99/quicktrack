import { ref } from 'vue'

const progress = ref(0)
const isLoading = ref(false)

function initProgress(amount: number = 30) {
    isLoading.value = true
    progress.value = amount
}

function addProgress(amount: number) {
    progress.value += amount
    if (progress.value >= 100) {
        setTimeout(() => (isLoading.value = false), 250)
    }
}

export function useProgressBar() {
    const state = {
        progress,
        isLoading,
    }

    return {
        state,
        initProgress,
        addProgress,
    }
}
