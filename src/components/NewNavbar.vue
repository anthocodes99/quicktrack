<script setup lang="ts">
import Logo from '../assets/logo.png'
import Home from '../assets/home.svg'
import Runcitworks from '../assets/runcitworks.svg'
</script>

<template>
    <header>
        <nav
            class="flex xl:items-start md:items-end flex-col items-start gap-8 pt-4"
        >
            <div class="">
                <img :src="Logo" class="w-10 h-10" alt="" />
            </div>
            <router-link :to="{ name: 'QuicktrackMain' }"
                ><div class="flex items-center">
                    <img :src="Home" alt="" class="w-10 h-10" />
                    <span class="hidden xl:block text-2xl text-gray-200 pl-6"
                        >Quicktrack</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'Runcitworks' }" href=""
                ><div class="flex items-center">
                    <img :src="Runcitworks" class="w-10 h-10" alt="" />
                    <span class="hidden xl:block text-2xl text-gray-200 pl-6"
                        >Runcitworks</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'RuncitworksSalesPurchases' }" href=""
                ><div class="flex items-center">
                    <img :src="Runcitworks" class="w-10 h-10" alt="" />
                    <span class="hidden xl:block text-2xl text-gray-200 pl-6"
                        >Sales Purchases</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'RuncitworksExpenses' }" href=""
                ><div class="flex items-center">
                    <img :src="Runcitworks" class="w-10 h-10" alt="" />
                    <span class="hidden xl:block text-2xl text-gray-200 pl-6"
                        >Expenses</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'RuncitworksCurrentBalance' }" href=""
                ><div class="flex items-center">
                    <img :src="Runcitworks" class="w-10 h-10" alt="" />
                    <span class="hidden xl:block text-2xl text-gray-200 pl-6"
                        >Balance</span
                    >
                </div>
            </router-link>
            <router-link :to="{ name: 'RuncitworksCashFlow' }" href=""
                ><div class="flex items-center">
                    <img :src="Runcitworks" class="w-10 h-10" alt="" />
                    <span class="hidden xl:block text-2xl text-gray-200 pl-6"
                        >Cash Flow</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'RuncitworksSetup' }" href=""
                ><div class="flex items-center">
                    <img :src="Runcitworks" class="w-10 h-10" alt="" />
                    <span class="hidden xl:block text-2xl text-gray-200 pl-6"
                        >Setup</span
                    >
                </div>
            </router-link>
        </nav>
    </header>
</template>

<style scoped></style>
