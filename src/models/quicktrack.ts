export interface Account {
    id: number
    username: string
    hutang: number
    owner: number
    hidden: boolean
}

export interface RawAccount {
    id: number
    username: string
    hutang: string
    owner: number
    hidden: boolean
}
