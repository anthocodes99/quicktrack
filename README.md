# Quicktrack@next

Version 3 of Quicktrack.

## Reasoning

The reasoning is actually a story it on itself. I decided to remake Toast because the current one just sucks
(1 Toast only, uses Vuex???, doesn't have information encapsulation or hiding, tedious).
I also decided to rewrite it in TypeScript, which turned out REALLY great. I implemented it with Composition API, so it's neat, you only need to call a single function instead of sending context objects.

```ts
// before
const store = useStore()
const toast_context = {
    text: '',
    desc: '',
    color: 'text-primary',
}
store.dispatch('toast', toast_context)

// after
const toast = useToast()
toast.info('', '')
```

I decide to add TypeScript to my current project, but I couldn't because of various error between `eslint-plugin-vue`, `prettier`, `eslint`, etc. So I gave up and just went Vite since it doesn't bother with all these stuffs.

## New Technologies

### Vite

Now uses Vite instead of vue-cli. Faster boot time for sure. Also more lean, so doesn't come with lots of linting or code formatters.

### TypeScript

I'm a fan of TypeScript now. I was really frustrated with `runcitworks.js` because it was giving me 'X is null.' or 'reduce of empty array with no initial value' or whatever it is. TypeScript will say "X could be undefined.", which immediately fixes these error. TypeScript is a must on larger projects for sure.

### Composition API

All code from hereon will use Composition API. It's the superior method, everything is neatly organized and makes sense, no need comma for every single thing(looking at you, Options API), and also better code flow.

### Pinia

Pinia allows for `<script setup>` style, which means we're using this over Vuex for sure. It's also removes the need to use `mutations` which made little sense even back then. The removal of x.state.y is also very convenient.
