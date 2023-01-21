<script setup lang="ts">
import NewNavbar from '../components/NewNavbar.vue'
import TheMobileTopNav from '../components/TheMobileTopNav.vue'
</script>

<template>
    <TheMobileTopNav />
    <div class="flex mx-auto md:max-w-xl lg:max-w-7xl gap-8 px-4">
        <NewNavbar class="hidden md:block" />
        <slot></slot>
    </div>
</template>

<style scoped></style>
