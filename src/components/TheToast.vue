<script setup lang="ts">
import ToastPopUp from '../primitives/ToastPopUp.vue'
import { useToast } from '../composables/toast'
import { computed } from 'vue'
import ToastButton from '../primitives/ToastButton.vue'

const toast = useToast()
const toasts = computed(() => toast.state.toasts.value)
const runCallback = function (e: () => void) {
    if (typeof e === 'function') return e()
    // else
    console.error('Toast callback is not a function!', e)
}
</script>

<template>
    <!-- TODO: Transition Animation (left in, or opacity in) -->
    <div class="fixed top-5 right-5 gap-2 flex flex-col">
        <template v-for="toast in toasts" :key="toast.id">
            <ToastPopUp
                :title="toast.title"
                :message="toast.message"
                :status="toast.status"
                :opacity="toast.opacity"
                @close="toast.close"
            >
                <template v-if="toast.buttons.length !== 0">
                    <div class="mt-2 pt-2 border-top">
                        <template v-for="button in toast.buttons">
                            <ToastButton
                                :btnText="button.btnText"
                                :btnStatus="button.btnStatus"
                                :btnCb="button.btnCb"
                                @btnClick="runCallback"
                            />
                        </template>
                    </div>
                </template>
            </ToastPopUp>
        </template>
    </div>
</template>

<style scoped></style>
