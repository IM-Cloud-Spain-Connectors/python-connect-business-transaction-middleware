# Python Connect Business Transaction Middleware

[![Test](https://github.com/othercodes/python-connect-business-transaction-middleware/actions/workflows/test.yml/badge.svg)](https://github.com/othercodes/python-connect-business-transaction-middleware/actions/workflows/test.yml)

Provides simple request-response style middleware for business transactions.

## Installation

The easiest way to install the Connect Business Transaction Middleware library is to get the latest version from PyPI:

```bash
# using poetry
poetry add rndi-connect-business-transaction-middleware
# using pip
pip install rndi-connect-business-transaction-middleware
```

## Usage

Creating and using a business transaction middleware is very easy, you just need to declare a middleware:

```python
from typing import Optional

from connect.eaas.core.responses import BackgroundResponse
from rndi.connect.business_transactions.contracts import FnBackgroundExecution


def middleware_sample(request: dict, nxt: Optional[FnBackgroundExecution] = None) -> BackgroundResponse:
    print('Sample Before')
    response = nxt(request)
    print('Sample After')
    return response
```

The signature of a middle must be the following:

```python
Middleware = Callable[[dict, Optional[FnBackgroundExecution]], TBackgroundResponse]
```

A middleware must accept a dictionary, commonly the Connect request dictionary, and an optional `FnBackgroundExecution`,
which is the next middleware or the actual transaction to be executed. The return type must be a valid
`BackgroundResponse`.

Once we have our middleware ready we can use the `make_middleware_callstack` to wrap the transaction with our
middlewares, as you can see as follows:

```python
from rndi.connect.business_transactions.adapters import prepare

# Prepare the selected transaction.
transaction = prepare(SomeTransaction())

# Instantiate the required middlewares.
middlewares = [
    middleware_sample
]

# Make the middleware callstack.
transaction = make_middleware_callstack(middlewares, transaction)

# Transaction Execution.
response = transaction(request)
```
