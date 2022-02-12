<script setup lang="ts">
interface Props {
    id: string
    color: string
    title: string
    desc: string
    btnColor: string
    btnText: string
}

const props = defineProps<Props>()
</script>

<template>
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark">
            <div class="modal-header">
                <h5 class="modal-title" :class="color" :id="id">
                    {{ title }}
                </h5>
                <button
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="modal"
                    aria-label="Close"
                ></button>
            </div>
            <div class="modal-body text-light">
                <slot></slot>
            </div>
            <div class="modal-footer">
                <button
                    type="button"
                    class="btn btn-secondary"
                    data-bs-dismiss="modal"
                >
                    Cancel
                </button>
                <button
                    @click="this.$emit('btnClick')"
                    type="button"
                    class="btn btn-danger"
                    :class="btnColor"
                    data-bs-dismiss="modal"
                >
                    {{ btnText }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
