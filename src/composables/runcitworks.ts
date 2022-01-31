import { computed, ref, Ref } from 'vue'
import { Monthdata } from '../models/monthdata'

enum TransactionType {
    Purchase = 'purchases',
    Sale = 'sales',
    PreviousBalance = 'previous_balances',
    Expense = 'expenses',
}

const useRuncitworks = function (currentMonthData: Ref<Monthdata>) {
    const _filterByProduct = function (type: TransactionType, product: string) {
        // if (!currentMonthData.value) return
        return currentMonthData.value[type].filter(
            (tran) => tran.product == product
        )
    }

    const getTotalBoughtByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(
            TransactionType.Purchase,
            product
        )
        // returns undefined OR 0
        // if (!filteredTrans) return
        return filteredTrans
            .map((tran) => tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getTotalSoldByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(TransactionType.Sale, product)
        // returns undefined OR 0
        // if (!filteredTrans) return
        return filteredTrans
            .map((tran) => tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getPreviousBalanceByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(
            TransactionType.PreviousBalance,
            product
        )
        // returns undefined OR 0
        // if (!filteredTrans) return
        return filteredTrans
            .map((tran) => tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const calculateCurrentBalance = function (
        totalBought: number,
        totalSold: number,
        totalPrevBal: number
    ) {
        return totalBought + totalPrevBal - totalSold
    }

    const getTotalSaleByProduct = function (product) {
        const filteredTrans = _filterByProduct(TransactionType.Sale, product)
        return filteredTrans
            .map((tran) => parseFloat(tran.unit_price) * tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getTotalPurchaseByProduct = function (product) {
        const filteredTrans = _filterByProduct(
            TransactionType.Purchase,
            product
        )
        return filteredTrans
            .map((tran) => parseFloat(tran.unit_price) * tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getTotalPreviousBalanceByProduct = function (product) {
        const filteredTrans = _filterByProduct(
            TransactionType.PreviousBalance,
            product
        )
        // return undefined OR 0
        // if (!filteredTrans) return
        return filteredTrans
            .map((tran) => parseFloat(tran.unit_price) * tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getPurchaseUnitPrice = function (product: string) {
        const totalBought = getTotalBoughtByProduct(product)
        const totalPrevBal = getPreviousBalanceByProduct(product)
        const totalCostBought = getTotalPurchaseByProduct(product)
        const totalCostPrevBal = getTotalPreviousBalanceByProduct(product)
        return (
            (totalBought + totalPrevBal) / (totalCostBought + totalCostPrevBal)
        )
    }

    const getSaleUnitPrice = function (product: string) {
        const totalSold = getTotalSoldByProduct(product)
        const totalSale = getTotalSaleByProduct(product)

        return totalSale / totalSold
    }
    return {
        currentMonthData,
        getTotalBoughtByProduct,
        getTotalSoldByProduct,
        getPreviousBalanceByProduct,
        calculateCurrentBalance,
        getTotalPurchaseByProduct,
        getTotalSaleByProduct,
        getTotalPreviousBalanceByProduct,
        getPurchaseUnitPrice,
        getSaleUnitPrice,
    }
}

export { useRuncitworks }
