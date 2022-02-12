# Undefined

Exploration of the answers for potentially undefined variables.

## Problem

We have a function that could potentially return `undefined`

```ts
const _filterByProduct = function (type: TransactionType, product: string) {
    if (!currentMonthData.value) return
    return currentMonthData.value[type].filter(
        (tran) => tran.product == product
    )
}
```

This is to avoid `currentMonthData[type] is null`. However, logically speaking, `Purchases, Sales, Expenses and Previous Balance` will not be null if properly initialized.

Here's the root response of `MonthData Detail` view.

```json
{
    "id": 36,
    "month": "2021-12-01",
    "products": [],
    "sales": [],
    "expenses": [],
    "purchases": [],
    "previous_balances": [],
    "user": 1,
    "starting_modal": "0.0000",
    "cashout": "0.0000",
    "profit_balance": "0.0000"
}
```

That said, `runcitworks.ts` should not check whether or not `currentMonthData[type] is null` or not.

Since my first rendition of runcitworks, I have discovered that reduce also accepts an initial value as well. That means we won't have `reduce of empty array with no initial value.` as well.

```ts
x.reduce((acc, curr) => acc + curr, 0)
```
