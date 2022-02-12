<script setup lang="ts">
import axios from 'axios'
import { computed, onBeforeMount, ref, toRefs } from 'vue'
import { useToast } from '../../composables/toast'
import { Monthdata } from '../../models/monthdata'
import { useStore } from '../../store'
import { useMonthdataStore } from '../../store/monthdata'
import { destructureAxios } from '../../utils/utils'

interface Props {
    currentMonthData: Monthdata
}

interface Product {
    name: string
}

const props = defineProps<Props>()
const { currentMonthData } = toRefs(props)

// init
const store = useStore()
const monthdata = useMonthdataStore()
const toast = useToast()

// local variables
const config = {
    headers: {
        'X-CSRFToken': store.csrftoken,
    },
}

// template refs
const userProducts = ref<Product[]>([])
const selectProduct = ref<Product | null>(null)

// computed properties
const products = computed(() => currentMonthData.value.products)

// template functions
const addProduct = async function (event) {
    // const formData = Object.fromEntries(new FormData(event.target))
    if (selectProduct.value === null) return
    const data = { name: selectProduct.value.name }
    const [res, err] = await destructureAxios(
        axios.post(
            `/api/v1/monthdatas/${currentMonthData.value.id}/products`,
            data,
            config
        )
    )
    if (res) {
        monthdata.addProduct(currentMonthData.value.id, data.name)
        toast.success(
            'Product added succesfully !',
            `You have added ${data.name} to month ${currentMonthData.value.month}`
        )
        return
    }
    // else
    toast.error(
        'An error occured!',
        `Did not succesfully add product ${data.name}.`
    )
}

const registerProduct = async function (event) {
    interface FormElement {
        product: string
    }
    const formData = <FormElement>Object.fromEntries(new FormData(event.target))
    const data = { name: formData.product }
    const [res, err] = await destructureAxios(
        axios.post(`/api/v1/products`, data, config)
    )
    if (res) {
        toast.success(
            'Product Registered.',
            `You have registered a product with name ${data.name}`
        )
        return
    }
    // else
    toast.error(
        'An error occured!',
        `Did not succesfully register the product ${data.name}.`
    )
}

// lifecycle hooks
onBeforeMount(async () => {
    const [res, err] = await destructureAxios(
        axios.get('/api/v1/products', config)
    )
    if (res) {
        userProducts.value = res.data
        return
    }
    // else
    toast.error(
        'Did not succesfully retrieve products!',
        'Please check your internet connection.'
    )
})
</script>

<template>
    <div class="d-flex justify-content-center">
        <div class="w-75 p-3">
            <h2>Products registered in this Month</h2>
            <ul class="list-group mb-3">
                <li
                    class="list-group-item lgi-dark"
                    v-for="(product, idx) in products"
                    :key="idx"
                >
                    {{ product }}
                </li>
            </ul>

            <h2>Add Product to Month</h2>
            <form @submit.prevent="addProduct">
                <div class="input-group mb-3 row g-3">
                    <div class="col">
                        <select
                            class="form-select"
                            name="product"
                            v-model="selectProduct"
                        >
                            <option
                                v-for="(item, idx) in userProducts"
                                :value="item"
                                :key="idx"
                            >
                                {{ item.name }}
                            </option>
                        </select>
                    </div>
                    <div class="col">
                        <input
                            class="btn btn-success"
                            type="submit"
                            value="Add Product"
                        />
                    </div>
                </div>
            </form>

            <h2>Register New Product</h2>
            <form @submit.prevent="registerProduct">
                <div class="row g-3">
                    <div class="col">
                        <input
                            class="form-control"
                            type="text"
                            name="product"
                        />
                    </div>
                    <div class="col">
                        <input
                            class="btn btn-primary"
                            type="submit"
                            value="Register Product"
                        />
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped></style>
