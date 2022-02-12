# Pinia vs Vuex

## Vuex `mutation` is no more

Pinia does not use `mutation` anymore. Instead, you either directly modify the state or call an action which modifies it.

## $patch with Pinia

You can patch multiple states with `$patch()`

```ts
quicktrack.$patch(
    {
        count: 12
        xyz: 12
    }
)
```

## setup() with Pinia

You can write Pinia stores with `setup()` style. I like this a lot, really makes Vue 3 what it is.

```ts
export const useQuicktrackStore = defineStore('quicktrack', () => {
    const count = ref(0)
    const doubleCount = () => count.value*2
    return {
        count
        doubleCount
    }
})
```
