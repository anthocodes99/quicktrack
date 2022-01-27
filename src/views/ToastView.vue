<script setup lang="ts">
import { onMounted } from 'vue'
import { useToast } from '../composables/toast'
import TheNavbar from '../components/TheNavbar.vue'

const toast = useToast()

onMounted(() => {
    toast.info('Welcome', 'Click the buttons to send a toast.')
    toast.success('New Update is Avaliable', 'Click refresh to update.')
})

const clearToasts = function () {
    toast.clearToasts()
}

const makeToast = function () {
    toast.success('Button is presed!', 'You have created a toast!')
}

const makeToastError = function () {
    toast.error('Oh no!', 'You angered the Toast gods.')
}
</script>

<template>
    <TheNavbar />
    <div class="container-lg toast-main">
        <h1>Toast.vue</h1>
        <h4>Fancy stackable Bootstrap Vue Toast</h4>
        <p class="mb-0">
            Written in TypeScript, intended for use with Composition API only.
        </p>
        <small class="">Requires TypeScript, Bootstrap and Vue 3</small>
        <div class="hstack gap-3 mt-3">
            <button class="btn btn-primary" @click="makeToast">
                Send a Toast !
            </button>
            <button class="btn btn-danger" @click="makeToastError">
                Another fancy Toast.
            </button>
            <button class="btn btn-primary" @click="clearToasts">
                Clear All Toasts
            </button>
        </div>
    </div>
</template>

<style scoped></style>
