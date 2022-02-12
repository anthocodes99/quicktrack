# Accounts and Sales

What's the best appoarch for dealing with Sales and Data Saver?

## Problem

Accounts have a list of past Sales, which is all the Sales that is linked to the selected Account. I used to obtain the Sales from accumulating all Sales from Monthdata and filtering it, but because I now lazy loads Monthdata(fetching only the first Monthdata, leaving the rest for Load on Visit), I couldn't reliably use it anymore. I would be missing a lot of Sales and it would hurt.

## Solutions

### Solution A

Append SaleSerializer for Accounts. Each account will list Sales for the past 40 days.

Pros:

-   Lazy Loading for Monthdata is preserved.
-   Loading between Home and UserDetails is fast.
-   Does not require lengthy code to work with.

Cons:

-   Longer initialization time.
-   Doesn't preserve DRY for Monthdata Sales.

### Solution B

MonthdataList to include Sales.

This will allow me to locally look up all Sales without fecthing it from the API.

Pros:

-   DRY is preserved.
-   Load time between UserDetails is fast.

Cons:

-   Fetches way too much Sales(I only need 40 days, not all the months).
-   Highest data consumption.
-   Require a lengthy amount of code to make it work.
-   Huge delay for initialization time.

### Soluton C

Fetch upon visit.

Sales will be fetched once the user is visited.

Pros:

-   Fastest initialization time(+0).
-   Least data consumption

Cons:

-   Unstable load times between Home and UserDetails.
