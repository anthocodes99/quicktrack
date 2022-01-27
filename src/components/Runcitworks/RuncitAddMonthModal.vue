<script setup lang="ts">
import { monthdata } from '../../models/monthdata'
interface Props {
    monthdatas: monthdata[]
}
const props = defineProps<Props>()
</script>

<template>
    <div class="modal" id="addMonth" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content bg-dark">
                <div class="modal-header">
                    <h5 class="modal-title text-warning">Create a new Month</h5>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <form action="" @submit.prevent="$emit('addMonth', $event)">
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-5">
                                <label
                                    class="form-label text-light"
                                    for="addMonthDate"
                                    >Select a Month</label
                                >
                                <select class="form-select" name="month" id="">
                                    <option selected>January</option>
                                    <option>February</option>
                                    <option>March</option>
                                    <option>April</option>
                                    <option>May</option>
                                    <option>June</option>
                                    <option>July</option>
                                    <option>August</option>
                                    <option>September</option>
                                    <option>October</option>
                                    <option>November</option>
                                    <option>December</option>
                                </select>
                            </div>
                            <div class="col-md-5">
                                <label class="form-label text-light" for="year"
                                    >Year</label
                                >
                                <select
                                    class="form-select"
                                    id="year"
                                    name="year"
                                >
                                    <option selected>2021</option>
                                    <option>2022</option>
                                    <option>2023</option>
                                    <option>2024</option>
                                    <option>2025</option>
                                    <option>2026</option>
                                </select>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-5">
                                <label
                                    class="form-label text-light"
                                    for="startingModal"
                                    >Starting Modal</label
                                >
                                <input
                                    class="form-control"
                                    type="number"
                                    name="startingModal"
                                    id="startingModal"
                                    value="0"
                                />
                            </div>
                            <div class="col-md-5">
                                <label
                                    class="form-label text-light"
                                    for="profitBalance"
                                    >Previous Profit Balance</label
                                >
                                <input
                                    class="form-control"
                                    type="number"
                                    name="profitBalance"
                                    id="profitBalance"
                                    step="0.0001"
                                    value="0"
                                />
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-5">
                                <label
                                    class="form-label text-light"
                                    for="previousbalance"
                                    >Port from Previous Balance</label
                                >
                                <select
                                    class="form-select"
                                    name="previousbalance"
                                >
                                    <option value="">None</option>
                                    <option
                                        v-for="month in monthdatas"
                                        :key="month.id"
                                        :value="month.month"
                                    >
                                        {{ month.month }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                        >
                            Close
                        </button>
                        <button class="btn btn-primary" type="submit">
                            Save changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
