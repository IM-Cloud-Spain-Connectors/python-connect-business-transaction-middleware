from typing import Optional, List

import pytest
from connect.eaas.core.responses import BackgroundResponse
from rndi.connect.business_transactions.adapters import prepare
from rndi.connect.business_transactions.contracts import BackgroundTransaction, FnBackgroundExecution

from rndi.connect.business_transaction_middleware.middleware import Middleware


@pytest.fixture
def make_transaction():
    class ApproveRequest(BackgroundTransaction):
        def name(self) -> str:
            return 'Approve Request'

        def should_execute(self, request: dict) -> bool:
            return request.get('status', 'pending') != 'approved'

        def execute(self, _: dict) -> BackgroundResponse:
            print('Transaction Execution')
            return BackgroundResponse.done()

        def compensate(self, _: dict, e: Exception) -> BackgroundResponse:
            return BackgroundResponse.fail()

    def __():
        return prepare(ApproveRequest())

    return __


@pytest.fixture
def make_middleware():
    def __(amount: int, state: dict) -> List[Middleware]:
        middlewares = []

        class DummyMiddleware:
            def __init__(self, index_: int, state_: dict):
                self.__index = index_
                self.__state = state_

            def __call__(self, request: dict, nxt: Optional[FnBackgroundExecution] = None) -> BackgroundResponse:
                self.__state.update({'executions': self.__state.get('executions', 0) + 1})
                print(f'00{self.__index} Before')
                response = nxt(request)
                print(f'00{self.__index} After')
                assert isinstance(response, BackgroundResponse)
                return response

        for index in range(amount):
            middlewares.append(DummyMiddleware(index + 1, state))

        return middlewares

    return __
