<script setup lang="ts">
import NewNavbar from '../components/NewNavbar.vue'
import TheMobileTopNav from '../components/TheMobileTopNav.vue'
</script>

<template>
    <div>
        <TheMobileTopNav />
        <div class="flex gap-8">
            <NewNavbar
                class="hidden lg:[width:275px] md:[width:88px] sm:[width:68px] sm:flex sm:flex-col sm:flex-shrink-0 items-end [-moz-box-align:end] flex-grow [-moz-box-flex:1]"
            />
            <div
                class="flex lg:[width:700px] md:[width:680px] sm:[width:552px] [-moz-box-flex:1] flex-grow md:[flex-grow:2] items-start"
            >
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
