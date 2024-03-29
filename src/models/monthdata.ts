export interface RawMonthdata {
    id: number
    month: string
    products: string[]
    user: number
    starting_modal: string
    cashout: string
    profit_balance: string

    purchases: Transaction[]
    sales: Transaction[]
    expenses: Transaction[]
    previous_balances: Transaction[]
}

export interface Monthdata {
    id: number
    month: string
    products: string[]
    user: number
    starting_modal: number
    cashout: number
    profit_balance: number

    purchases: Transaction[]
    sales: Transaction[]
    expenses: Transaction[]
    previous_balances: Transaction[]
}

export interface Transaction {
    id: string
    monthdata: number
    date: string
    unit_price: string
    quantity: number

    product?: string
    account?: string
    description?: string
    created_at?: string
}

// prev_bal == purchase
// export interface Purchase extends Transaction {
//     product: string
// }

// export interface Sale extends Transaction {
//     product: string
//     account: string
// }

// export interface Expense extends Transaction {
//     description: string
//     created_at: string
// }

export enum TransactionType {
    Purchase = 'purchases',
    Sale = 'sales',
    Expense = 'expenses',
    PreviousBalance = 'previousbalances',
}

export interface Product {
    name: string
}
