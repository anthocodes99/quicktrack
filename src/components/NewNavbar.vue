<script setup lang="ts">
import Logo from '../assets/logo.png'
</script>

<template>
    <header>
        <nav
            class="flex lg:items-start sm:items-end flex-col items-start gap-8 pt-4"
        >
            <!-- 
                NOTE: The workflow for adding SVG to tailwindcss projects should be
                      done using inline SVG.
                      (https://stackoverflow.com/questions/64197107/how-to-modify-svg-icon-colors-with-tailwind)
            -->

            <!-- 
                Icons are courtesy from Google Fonts
                https://fonts.google.com/icons?icon.platform=web
            -->

            <div class="">
                <img :src="Logo" class="w-8 h-8" alt="" />
            </div>

            <router-link :to="{ name: 'QuicktrackMain' }"
                ><div class="flex items-center">
                    <svg
                        class="fill-current text-[#E94F37] w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -960 960 960"
                    >
                        <path
                            d="M160-120v-480l320-240 320 240v480H560v-280H400v280H160Z"
                        />
                    </svg>
                    <span class="hidden lg:block text-xl text-gray-200 pl-6"
                        >Quicktrack</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'rw-dashboard' }" href=""
                ><div class="flex items-center">
                    <svg
                        class="fill-current text-[#E94F37] w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -960 960 960"
                    >
                        <path
                            d="M510-570v-270h330v270H510ZM120-450v-390h330v390H120Zm390 330v-390h330v390H510Zm-390 0v-270h330v270H120Z"
                        />
                    </svg>
                    <span class="hidden lg:block text-xl text-gray-200 pl-6"
                        >Dashboard</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'rw-sales' }" href="">
                <div class="flex items-center">
                    <svg
                        class="fill-current text-[#E94F37] w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -960 960 960"
                    >
                        <path
                            d="M433-160H140q-24 0-42-18t-18-42v-520q0-24 18-42t42-18h680q24 0 42 18t18 42v239h-32L598-251 471-378 343-250l90 90Zm165 80L428-250l43-43 127 127 240-240 42 44L598-80ZM140-640v139h680v-139H140Z"
                        />
                    </svg>
                    <span class="hidden lg:block text-xl text-gray-200 pl-6"
                        >Sales</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'rw-purchases' }" href=""
                ><div class="flex items-center">
                    <svg
                        class="fill-current text-[#E94F37] w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -960 960 960"
                    >
                        <path
                            d="M220-80q-24 0-42-18t-18-42v-680q0-24 18-42t42-18h361l219 219v521q0 24-18 42t-42 18H220Zm230-121h60v-40h60q13 0 21.5-8.5T600-271v-130q0-13-8.5-21.5T570-431H420v-70h180v-60h-90v-40h-60v40h-60q-13 0-21.5 8.5T360-531v130q0 13 8.5 21.5T390-371h150v70H360v60h90v40Zm106-460h159L556-820v159Z"
                        />
                    </svg>
                    <span class="hidden lg:block text-xl text-gray-200 pl-6"
                        >Purchases</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'rw-expenses' }" href=""
                ><div class="flex items-center">
                    <svg
                        class="fill-current text-[#E94F37] w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -960 960 960"
                    >
                        <path
                            d="M222-80q-43.75 0-74.375-30.625T117-185v-125h127v-570l59.8 60 59.8-60 59.8 60 59.8-60 59.8 60 60-60 60 60 60-60 60 60 60-60v695q0 43.75-30.625 74.375T738-80H222Zm514.5-60q19.5 0 31.5-12.5t12-32.5v-611H307v536h390v75q0 20 10 32.5t29.5 12.5ZM360-642v-60h240v60H360Zm0 134v-60h240v60H360Zm333-134q-12 0-21-9t-9-21q0-12 9-21t21-9q12 0 21 9t9 21q0 12-9 21t-21 9Zm0 129q-12 0-21-9t-9-21q0-12 9-21t21-9q12 0 21 9t9 21q0 12-9 21t-21 9Z"
                        />
                    </svg>
                    <span class="hidden lg:block text-xl text-gray-200 pl-6"
                        >Expenses</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'rw-balance' }" href=""
                ><div class="flex items-center">
                    <svg
                        class="fill-current text-[#E94F37] w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -960 960 960"
                    >
                        <path
                            d="M180-120q-24 0-42-18t-18-42v-660h60v660h660v60H180Zm75-135v-334h119v334H255Zm198 0v-540h119v540H453Zm194 0v-170h119v170H647Z"
                        />
                    </svg>
                    <span class="hidden lg:block text-xl text-gray-200 pl-6"
                        >Balance</span
                    >
                </div>
            </router-link>
            <router-link :to="{ name: 'rw-cashflow' }" href=""
                ><div class="flex items-center">
                    <svg
                        class="fill-current text-[#E94F37] w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -960 960 960"
                    >
                        <path
                            d="M510-510v-309q123 8 210.5 97.5T819-510H510Zm-60 369q-131-11-220.5-109T140-480q0-132 89.5-230T450-819v678Zm60 0v-309h309q-11 122-98.5 211.5T510-141Z"
                        />
                    </svg>
                    <span class="hidden lg:block text-xl text-gray-200 pl-6"
                        >Cash Flow</span
                    >
                </div>
            </router-link>

            <router-link :to="{ name: 'rw-settings' }" href=""
                ><div class="flex items-center">
                    <svg
                        class="fill-current text-[#E94F37] w-8 h-8"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -960 960 960"
                    >
                        <path
                            d="m388-80-20-126q-19-7-40-19t-37-25l-118 54-93-164 108-79q-2-9-2.5-20.5T185-480q0-9 .5-20.5T188-521L80-600l93-164 118 54q16-13 37-25t40-18l20-127h184l20 126q19 7 40.5 18.5T669-710l118-54 93 164-108 77q2 10 2.5 21.5t.5 21.5q0 10-.5 21t-2.5 21l108 78-93 164-118-54q-16 13-36.5 25.5T592-206L572-80H388Zm92-270q54 0 92-38t38-92q0-54-38-92t-92-38q-54 0-92 38t-38 92q0 54 38 92t92 38Z"
                        />
                    </svg>
                    <span class="hidden lg:block text-xl text-gray-200 pl-6"
                        >Settings</span
                    >
                </div>
            </router-link>
        </nav>
    </header>
</template>

<style scoped></style>
