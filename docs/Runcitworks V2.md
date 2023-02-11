# Runcitworks Business Logic V2

Upgrading the business logic of Runcitworks.

## Problem

To get current balance, we'll have to do a few magic tomfoolery.

```ts
interface Props {
    currentMonthdata: Monthdata
}

const props = defineProps<Props>()

// we have to useRuncitworks to do the calculation
const runcitworks = useRuncitworks(currentMonthData)

// we then have to know the way how the business logic work to perform arithmetics
const currentBalance = computed(() => {
    // assemble an array of objects
    let table = <CurrentBalanceItem[]>[]
    // iterate through all objects and perform the calculation
    props.currentMonthData.products.forEach((product) => {
        const quantityBought = runcitworks.getTotalBoughtByProduct(product)
        const quantitySold = runcitworks.getTotalSoldByProduct(product)
        const quantityPrevBal = runcitworks.getPreviousBalanceByProduct(product)

    }
})
```

I still need to know the structure of the business logic in order to use the composable.

A better idea would just to do:

```ts
const balances = monthdata.getProductBalances()
// [{product: 'Cinnamoroll', balance: 12}, {product: 'Hello Kitty', balance: 8}]
const asset = monthdata.getAsset()
// 128.53
```

```ts
// tap into the store
const monthdataStore = useMonthdataStore()
const monthdata = monthdataStore.getCurrentMonthdata

//balance implies current, current balance is redundant
const balance = monthdata.getBalance('product')
// 12
const previousBalance = monthdata.getPreviousBalance('product')
// 4
const quantityBought = monthdata.getQuantityBought('product')
// 18
const quantitySold = monthdata.getQuantitySold('product')
// 10
```

The script could look like this:

```ts
const productBalanceList = []
products.forEach(function (product) {
    productBalanceList.push({ product: product, balance: getBalance(product) })
})
```
