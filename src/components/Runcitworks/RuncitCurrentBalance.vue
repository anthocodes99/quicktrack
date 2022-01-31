<script setup lang="ts">
import { computed, reactive, ref, toRefs, watch } from 'vue'
import { useRuncitworks } from '../../composables/runcitworks'
import { useToast } from '../../composables/toast'
import { Monthdata } from '../../models/monthdata'

interface Props {
    currentMonthData: Monthdata
}

interface CurrentBalanceItem {
    product: string
    quantityBought: number
    quantitySold: number
    quantityPrevBal: number
    currentBalance: number
    productValue: number
}

interface PerformanceTableItem {
    product: string
    unitProfit: number
    netProfit: number
}

const props = defineProps<Props>()
const { currentMonthData } = toRefs(props)

const toast = useToast()
const runcitworks = useRuncitworks(currentMonthData)

// template refs

const isError = ref(false)

// local functions

// FIXME: TypeScript intellisense does not interpret this properly
function _isUndefined<Type>(variable: Type): Boolean {
    return typeof variable === 'undefined'
}

const currentBalanceTable = computed(() => {
    let table = <CurrentBalanceItem[]>[]
    props.currentMonthData.products.forEach((product) => {
        const quantityBought = runcitworks.getTotalBoughtByProduct(product)
        const quantitySold = runcitworks.getTotalSoldByProduct(product)
        const quantityPrevBal = runcitworks.getPreviousBalanceByProduct(product)

        if (
            typeof quantityBought === 'undefined' ||
            typeof quantitySold === 'undefined' ||
            typeof quantityPrevBal === 'undefined'
        ) {
            isError.value = true
            const data = {
                quantityBought,
                quantitySold,
                quantityPrevBal,
            }
            toast.error(
                'Error',
                `You dun goofed boi, currentBalance aint workin. ${Object.values(
                    data
                )}`
            )
            return
        }
        const currentBalance = runcitworks.calculateCurrentBalance(
            quantityBought,
            quantitySold,
            quantityPrevBal
        )

        const productValue =
            runcitworks.getPurchaseUnitPrice(product) * currentBalance

        const item = {
            product,
            quantityBought,
            quantitySold,
            quantityPrevBal,
            currentBalance,
            productValue,
        }
        table.push(item)
    })
    return table
})

const performanceTable = computed(() => {
    let table = <PerformanceTableItem[]>[]
    props.currentMonthData.products.forEach((product) => {
        // unitprofit
        // (Amount Sold / Quantity Sold) -
        // (Amount Bought + Amount PrevBal) / (Quantity Bought + Quantity PrevBal)
        const purchaseUnitPrice = runcitworks.getPurchaseUnitPrice(product)

        const saleUnitPrice = runcitworks.getSaleUnitPrice(product)
        const unitProfit = saleUnitPrice - purchaseUnitPrice
        const netProfit =
            runcitworks.getTotalSoldByProduct(product) * unitProfit
        const item = {
            product,
            unitProfit,
            netProfit,
        }
        table.push(item)
    })
    return table
})
</script>

<template>
    <template v-if="isError">
        <div>
            <h1>An Error Occured</h1>
            <h3>
                Did not successfully calculate data. Please contract
                administrator.
            </h3>
        </div>
    </template>
    <template v-else>
        <h2 class="text-orange">Current Balance</h2>
        <table id="runcit-balance" class="table text-light">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Product</th>
                    <th scope="col">Quantity Bought</th>
                    <th scope="col">Quantity Sold</th>
                    <th scope="col">Previous Balance</th>
                    <th scope="col">Current Balance</th>
                    <th scope="col">Value</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, idx) in currentBalanceTable" :key="idx">
                    <th scope="row">{{ idx + 1 }}</th>
                    <td>{{ item.product }}</td>
                    <td>{{ item.quantityBought }} pcs</td>
                    <td>{{ item.quantitySold }} pcs</td>
                    <td>{{ item.quantityPrevBal }} pcs</td>
                    <td>{{ item.currentBalance }} pcs</td>
                    <td>
                        <template v-if="isNaN(item.productValue)">
                            N/A
                        </template>
                        <template v-else>
                            RM {{ item.productValue.toFixed(4) }}
                        </template>
                    </td>
                </tr>
            </tbody>
        </table>
        <h2>Performance</h2>
        <table class="table text-light">
            <thead>
                <tr>
                    <th scope="col">Product</th>
                    <th scope="col">Unit Profit</th>
                    <th scope="col">Net Profit</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(product, idx) in performanceTable" :key="idx">
                    <th scope="row">{{ product.product }}</th>
                    <td>
                        <template v-if="isNaN(product.unitProfit)">
                            N/A
                        </template>
                        <template v-else>
                            RM {{ product.unitProfit.toFixed(2) }}/pcs
                        </template>
                    </td>
                    <td>
                        <template v-if="isNaN(product.netProfit)">
                            N/A
                        </template>
                        <template v-else>
                            RM {{ product.netProfit.toFixed(2) }}
                        </template>
                    </td>
                </tr>
            </tbody>
        </table>
    </template>
</template>

<style scoped></style>
