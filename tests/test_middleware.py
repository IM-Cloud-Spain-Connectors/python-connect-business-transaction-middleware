from random import randint

from rndi.connect.business_transaction_middleware.middleware import make_middleware_callstack


def tests_transaction_preparer_should_build_a_transaction_callstack_successfully(make_transaction, make_middleware):
    state = {'executions': 0}  # mutable object (dict) to track the state.

    middlewares = make_middleware(randint(1, 10), state)
    transaction = make_middleware_callstack(middlewares, make_transaction())

    response = transaction({
        'id': 'PR-0001-0002-0003-0004',
        'status': 'pending',
        'params': [
            {'id': 'PARAM_CUSTOMER_ID', 'value': 'eda1b4f1-a3a8-4a87-bd3f-ad71f6c2e93e'},
        ],
    })

    assert response.status == 'success'
    assert state.get('executions', 0) == len(middlewares)
