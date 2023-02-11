# Runcitworks Routes

Doc on the design and planning for handling routing for `Runcitworks`

# Potential Solutions

## ID based path resolution

> `/runcitworks/:id`

> `/runcitworks/:id/sales`

> `/runcitworks/:id/expenses`

This is interesting, because `Quicktrack`'s design has been always this way. I don't think it ever came up to my mind when I was designing routing for `Runcitworks`.

This is good because all the nested components do not need to depend on a single `const monthdata = ref()` to find out which monthdata are we on.

However, this appoarch has some problems to it.

**Problem 1 - You need Runcitworks List View**

To have details views `/runcitworks/:id`, you need a list view `/runcitworks/`. This can be mitigated with `Vue Router`'s nested routes. It will always be displaying detail views, and only when you change the `<select>` element, then it will programmatically navigate to it's respective view.

**Problem 2 - `/runcitworks` endpoint needs to be resolved**

Navbar links to `/runcitworks`, not `/runcitworks/id`. What do you do?

## Ref based path resolution

> `/runcitworks`

> `/runcitworks/sales`

> `/runcitworks/expenses`

This is basically following my original design. There would be a single `ref()` that all subsequent renders are based on. When this change, the view's `isInitialized` ref will be assigned to `false` until the required data are acquired. But with nested routes, this present some problems:

**Problem 1 - How do you send props down?**

TODO: figure this one out lmao.

## Nested Name Views Resolution

You can create complex layouts using named views with nested views.

```
/runcitworks/dashboard

Runcitworks
+------+--------------------+
| Nav  | Dashbaord          |
|      |                    |
+------|--------------------|

         |
         V

/runcitworks/sales

Runcitworks
+------+--------------------+
| Nav  | Sales              |
|      |                    |
+------|--------------------|
```

Props can be passed via `props:true` properties in routes.

`<router-views>` can have data attached to them `:monthdata="monthdata"`.

I could also use hooks `useMonthdata()` to make everything more global, but that increases coupling a lot. The router views shouldn't have to know what model of Monthdata we are working with.
