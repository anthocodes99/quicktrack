<script setup lang="ts">
import { Account } from '../../models/quicktrack'
import router from '../../router'
interface Props {
    accounts: Account[]
}

const props = defineProps<Props>()

const routeChange = function (id: number) {
    router.push({ name: 'QuicktrackDetails', params: { id } })
}
</script>

<template>
    <div class="container col-lg-7 col-md-12 pt-5">
        <div class="accounts-list">
            <template v-for="account in accounts" :key="account.id">
                <div
                    class="account border border-1"
                    @click="routeChange(account.id)"
                    v-if="!account.hidden"
                >
                    <h2>{{ account.username }}</h2>
                    <h5 class="hutang">RM {{ account.hutang }}</h5>
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped>
.accounts-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 0.25rem;
}

.account {
    padding: 0.5rem;
    background-color: #021620;
    border-color: #033b57 !important;
    border-radius: 10%;
}

.account:hover {
    cursor: pointer;
}

.account > .username {
    color: #e94f37;
}
</style>
