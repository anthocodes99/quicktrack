import { Transaction } from './monthdata'

export interface Account {
    id: number
    username: string
    hutang: number
    owner: number
    hidden: boolean
    recent_sales: Transaction[]
}

export interface RawAccount {
    id: number
    username: string
    hutang: string
    owner: number
    hidden: boolean
    recent_sales: Transaction[]
}
