<script setup lang="ts">
import NewNavbar from '../components/NewNavbar.vue'
import TheMobileTopNav from '../components/TheMobileTopNav.vue'
</script>

<template>
    <div>
        <TheMobileTopNav />
        <div class="flex mx-auto md:max-w-xl lg:max-w-7xl gap-8">
            <NewNavbar class="hidden md:block" />
            <slot></slot>
        </div>
    </div>
</template>

<style scoped></style>
