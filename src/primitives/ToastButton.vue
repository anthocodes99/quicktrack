<script setup lang="ts">
import { ToastButtonColor } from '../composables/toast'
interface Props {
    btnText: string
    btnStatus: ToastButtonColor
    btnCb: () => void
}

const props = defineProps<Props>()
</script>

<template>
    <button
        type="button"
        class="btn btn-sm"
        :class="btnStatus"
        @click="$emit('btnClick', btnCb)"
    >
        {{ btnText }}
    </button>
</template>

<style scoped></style>
