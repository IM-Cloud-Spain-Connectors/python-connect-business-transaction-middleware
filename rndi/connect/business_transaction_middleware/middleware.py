#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import Callable, List, Optional

from connect.eaas.core.responses import BackgroundResponse
from rndi.connect.business_transactions.contracts import FnBackgroundExecution

Middleware = Callable[[dict, Optional[FnBackgroundExecution]], BackgroundResponse]


def make_middleware_callstack(
        middlewares: List[Middleware],
        transaction: Optional[FnBackgroundExecution] = None,
) -> FnBackgroundExecution:
    """
    Makes the middleware callstack.

    :param middlewares: List[Middleware] The list of middlewares to prepare.
    :param transaction: Optional[FnBackgroundExecution] The transaction to wrap with middlewares.
    :return: FnBackgroundExecution
    """

    def __make_middleware(current_: Middleware, next_: Optional[Middleware] = None) -> FnBackgroundExecution:
        def __middleware_callstack(request: dict):
            return current_(request, next_)

        return __middleware_callstack

    callstack = None
    for middleware in reversed(middlewares if transaction is None else middlewares + [transaction]):
        current = middleware
        if callstack is not None:
            current = __make_middleware(current, callstack)
        callstack = current

    return callstack
