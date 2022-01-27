<script setup lang="ts">
import TheNavbar from '../components/TheNavbar.vue'
import { useProgressBar } from '../composables/progressbar'

const progress = useProgressBar()
</script>

<template>
    <TheNavbar />
    <div>
        <h1>Vite Lab</h1>

        <div class="d-flex gap-3">
            <button class="btn btn-primary" @click="progress.initProgress(30)">
                Initialize Progress
            </button>
            <button class="btn btn-primary" @click="progress.addProgress(30)">
                Add 30 Progress
            </button>
        </div>
    </div>
</template>

<style scoped></style>
