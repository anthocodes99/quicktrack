# Information Hiding / Encapsulation

https://www.youtube.com/watch?v=29NMlHHLUsI

## Information Hiding

As the name suggests, information is hidden behind function calls. One does not need to know the specific state of the variable, all they need is just the function that is responsible for getting the result.

```py
class Payment:
    def __init__():
        self.payment_status = 'checkout'

    def is_checkout():
        return self.payment_status == 'checkout'
    
    def is_paid():
        return self.payment_status == 'paid'
```

In this case, all you need is `is_checkout()`. If there's a new implementation in the future, you will just call the new function that is responsible for the new feature. This makes it so that code are harder to break.

We're using that pattern here as well.
```ts
toast.info()
toast.warning()
```

We just removed 1 unneccesary argument. We do not need to know the status either, that's handled by toast itself. Neat, isn't it?

## Encapsulation

This one allows the user to modify status without directly touching the variable.

To borrow from the previous example :
```py
class Payment:
    self._payment_status = 'checkout'

    def checkout(){
        # charges the user
        self._payment_status = 'paid'
    }
```

This is used to either restrict access or to provide abstraction. Very neat also.

However, we do not need this at the moment.
