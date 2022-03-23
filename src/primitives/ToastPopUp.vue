<script lang="ts" setup>
import { Status } from '../composables/toast'
interface Props {
    title: string
    message: string
    status: Status
    opacity: number
}
const props = defineProps<Props>()
</script>

<template>
    <div
        class="toast fade show bg-dark text-light"
        :style="{ opacity: `${opacity}%` }"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
    >
        <div class="toast-header">
            <strong class="me-auto" :class="status">{{ title }}</strong>
            <button
                type="button"
                class="btn-close"
                aria-label="Close"
                @click="$emit('close')"
            ></button>
        </div>
        <div class="toast-body">
            {{ message }}
            <slot></slot>
        </div>
    </div>
</template>
