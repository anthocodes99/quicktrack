import { Ref } from 'vue'
import { Monthdata, Transaction } from '../models/monthdata'

enum MonthdataTransactionType {
    Purchase = 'purchases',
    Sale = 'sales',
    PreviousBalance = 'previous_balances',
    Expense = 'expenses',
}

const useRuncitworks = function (currentMonthData: Ref<Monthdata>) {
    const _filterByProduct = function (
        type: MonthdataTransactionType,
        product: string
    ) {
        // if (!currentMonthData.value) return
        return currentMonthData.value[type].filter(
            (tran) => tran.product == product
        )
    }

    const accumulateAllTransactions = function (transactions: Transaction[]) {
        return transactions
            .map((tran) => tran.quantity * parseFloat(tran.unit_price))
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getTotalBoughtByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(
            MonthdataTransactionType.Purchase,
            product
        )
        // returns undefined OR 0
        // if (!filteredTrans) return
        return filteredTrans
            .map((tran) => tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getTotalSoldByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(
            MonthdataTransactionType.Sale,
            product
        )
        // returns undefined OR 0
        // if (!filteredTrans) return
        return filteredTrans
            .map((tran) => tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getPreviousBalanceByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(
            MonthdataTransactionType.PreviousBalance,
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

    const getTotalSaleByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(
            MonthdataTransactionType.Sale,
            product
        )
        return filteredTrans
            .map((tran) => parseFloat(tran.unit_price) * tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getTotalPurchaseByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(
            MonthdataTransactionType.Purchase,
            product
        )
        return filteredTrans
            .map((tran) => parseFloat(tran.unit_price) * tran.quantity)
            .reduce((acc, curr) => acc + curr, 0)
    }

    const getTotalPreviousBalanceByProduct = function (product: string) {
        const filteredTrans = _filterByProduct(
            MonthdataTransactionType.PreviousBalance,
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

        const purchaseUnitPrice =
            (totalCostBought + totalCostPrevBal) / (totalBought + totalPrevBal)
        return isNaN(purchaseUnitPrice) ? 0 : purchaseUnitPrice
    }

    const getSaleUnitPrice = function (product: string) {
        const totalSold = getTotalSoldByProduct(product)
        const totalSale = getTotalSaleByProduct(product)

        const saleUnitPrice = totalSale / totalSold
        return isNaN(saleUnitPrice) ? 0 : saleUnitPrice
    }

    function calculateProductPerformance(product: string) {
        // unitprofit
        // (Amount Sold / Quantity Sold) -
        // (Amount Bought + Amount PrevBal) / (Quantity Bought + Quantity PrevBal)
        const purchaseUnitPrice = getPurchaseUnitPrice(product)

        const saleUnitPrice = getSaleUnitPrice(product)
        const unitProfit = saleUnitPrice - purchaseUnitPrice
        const netProfit = getTotalSoldByProduct(product) * unitProfit
        const item = {
            product,
            unitProfit,
            netProfit,
        }
        return item
    }

    const calculateAssets = function (
        totalPurchase: number,
        totalSale: number,
        totalProfit: number,
        totalPreviousBalance: number
    ) {
        // previous balance + purchases + profit - sales
        return totalPreviousBalance + totalPurchase + totalProfit - totalSale
    }

    return {
        currentMonthData,
        accumulateAllTransactions,
        getTotalBoughtByProduct,
        getTotalSoldByProduct,
        getPreviousBalanceByProduct,
        calculateCurrentBalance,
        getTotalPurchaseByProduct,
        getTotalSaleByProduct,
        getTotalPreviousBalanceByProduct,
        getPurchaseUnitPrice,
        getSaleUnitPrice,
        calculateProductPerformance,
        calculateAssets,
    }
}

export { useRuncitworks }
