<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <router-link :to="{ name: 'Home' }" class="navbar-brand"
                >Vite Lab</router-link
            >
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link
                            :to="{ name: 'QuicktrackMain' }"
                            class="nav-link"
                            >Quicktrack</router-link
                        >
                    </li>
                    <li class="nav-item">
                        <router-link
                            :to="{ name: 'Runcitworks' }"
                            class="nav-link"
                            >Runcitworks</router-link
                        >
                    </li>
                    <li class="nav-item">
                        <router-link
                            :to="{ name: 'ToastView' }"
                            class="nav-link"
                            >Toast</router-link
                        >
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
