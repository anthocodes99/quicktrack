<script setup lang="ts">
import Logo from '../assets/logo.png'
</script>

<template>
    <nav class="block md:hidden mx-auto bg-[#212529] px-3 py-2">
        <div class="flex items-center justify-between">
            <span><img :src="Logo" width="32" height="32" alt="" /></span>

            <span class="text-[#3F88C5]">antho</span>
        </div>
    </nav>
</template>

<style scoped></style>
