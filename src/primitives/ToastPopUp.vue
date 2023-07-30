<script lang="ts" setup>
import FlowbiteCheck from '../primitives/FlowbiteCheck.vue'
import FlowbiteInfo from '../primitives/FlowbiteInfo.vue'
import FlowbiteWarning from '../primitives/FlowbiteWarning.vue'
import FlowbiteError from '../primitives/FlowbiteError.vue'

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
    <!-- TODO: css/ui to match color scheme and design scheme -->
    <div
        id="toast-default"
        class="flex items-center w-full max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800 transition ease-in-out duration-100"
        :style="{ opacity: `${opacity}%` }"
        role="alert"
    >
        <template v-if="status == Status.Success">
            <FlowbiteCheck />
        </template>
        <template v-else-if="status == Status.Warning">
            <FlowbiteWarning />
        </template>
        <template v-else-if="status == Status.Danger">
            <FlowbiteError />
        </template>
        <template v-else>
            <FlowbiteInfo />
        </template>
        <div class="ml-3 text-sm font-normal">{{ message }}</div>
        <!-- CONSIDER: move file to primitive, or use own X button. -->
        <button
            type="button"
            class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700"
            data-dismiss-target="#toast-default"
            aria-label="Close"
            @click="$emit('close')"
        >
            <span class="sr-only">Close</span>
            <svg
                class="w-3 h-3"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 14 14"
            >
                <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                />
            </svg>
        </button>
    </div>
</template>
