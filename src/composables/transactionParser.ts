import { Transaction } from '../models/monthdata'

function convertkvObjectToArray(kvObject: {}) {
    // turn key-value array pairs into
    // array with date in it.
    // {"2023-02-10":{}}
    //     becomes
    // [{date:"2023-02-10, transactions:[]"},{},{}]
    const resultTable: {}[] = []
    for (const [key, value] of Object.entries(kvObject)) {
        // key = "2023-02-10"
        // value = [...transactions]
        resultTable.push({ date: key, transactions: value })
    }
    return resultTable
}

export function useTransactionParser() {
    // TODO: Refactor code
    function sortByDate(transactions) {
        const sortedByDate = transactions.sort((a, b) => {
            // the + before new are to clear ts error.
            // https://stackoverflow.com/a/68876658/15029609
            return +new Date(b.date) - +new Date(a.date)
        })
        const sortedTransactions = sortedByDate.reduce((acc, curr) => {
            if (!acc[curr.date]) {
                acc[curr.date] = []
            }
            acc[curr.date].push(curr)
            return acc
        }, {})

        return sortedTransactions
    }

    // FIXME: sortTransactionByDate isn't actually using Transaction
    //        model. New name / refactor code. Still works.
    function sortTransactionsByDate(transactions: Transaction[]) {
        const sortedByDate = transactions.sort((a, b) => {
            // the + before `new Date()` are to clear ts error.
            // https://stackoverflow.com/a/68876658/15029609
            return +new Date(b.date) - +new Date(a.date)
        })

        const sortedTransactions = sortedByDate.reduce((acc, curr) => {
            if (!acc[curr.date]) {
                acc[curr.date] = []
            }
            acc[curr.date].push(curr)
            return acc
        }, {})

        return convertkvObjectToArray(sortedTransactions)
    }

    return {
        sortByDate,
        sortTransactionsByDate,
    }
}
