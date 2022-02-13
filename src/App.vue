<script setup lang="ts">
import Toast from './components/TheToast.vue'
import TheProgressBar from './components/TheProgressBar.vue'
import ReloadPrompt from './components/ReloadPrompt.vue';
</script>

<template>
    <TheProgressBar />
    <router-view></router-view>
    <Toast />
    <ReloadPrompt />
</template>

<style>
html {
    background-color: #131516;
}
h1,
h2 {
    color: #e94f37;
}
h3,
h4,
h5,
p,
.form-label {
    color: #3f88c5;
}
li,
th,
td,
small {
    color: rgb(236, 230, 221);
}
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    background-color: #131516;
}

.text-orange {
    color: #e94f37 !important;
}
</style>
