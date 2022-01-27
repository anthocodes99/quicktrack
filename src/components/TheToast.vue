<script setup lang="ts">
import ToastPopUp from '../primitives/ToastPopUp.vue'
import { useToast } from '../composables/toast'
import { computed } from 'vue'

const toast = useToast()
const toasts = computed(() => toast.state.toasts.value)
</script>

<template>
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
        <template v-for="toast in toasts" :key="toast.id">
            <ToastPopUp
                :title="toast.title"
                :message="toast.message"
                :status="toast.status"
                :opacity="toast.opacity"
                @close="toast.close"
            >
                <div class="mt-2 pt-2 border-top">
                    <button type="button" class="btn btn-primary btn-sm">
                        Take action
                    </button>
                    <button
                        type="button"
                        class="btn btn-secondary btn-sm"
                        data-bs-dismiss="toast"
                    >
                        Close
                    </button>
                </div>
            </ToastPopUp>
        </template>
    </div>
</template>

<style scoped></style>
