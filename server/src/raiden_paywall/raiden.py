import asyncio
import datetime
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import Optional, Tuple, Union

import aiohttp
import structlog
from raiden.api.v1.encoding import PaymentSchema

LOG = structlog.get_logger()


def seconds_until(time):
    return (time - datetime.datetime.now()).total_seconds()


class PaymentStatus(Enum):
    SUCCESS = 1
    FAILED = 2
    TIMED_OUT = 3
    ERROR = 4


class RaidenPaymentProxy:
    _payment_schema_v1 = PaymentSchema()

    def __init__(self, host, port, token_address, poll_interval=0.5):
        self._base_url = f"{host}:{port}"
        self._payment_awaits = {}
        self._poll_interval = poll_interval
        self._poll_task = None
        self._session = aiohttp.ClientSession()
        self.token_address = token_address
        super().__init__()

    @property
    def _event_is_waiting(self):
        return bool(len(self._payment_awaits))

    @property
    def is_polling(self):
        if self._poll_task:
            return not self._poll_task.cancelled()
        return False

    async def _get(self, resource):
        async with self._session.get(f"{self._base_url}{resource}") as response:
            return await response.json()

    async def _poll_payments(self):
        response = await self._get(f"/payments/{self.token_address}")
        if response.status == 200:
            # return the payments
            return response.data
        # TODO handle errors
        else:
            return []

    async def _run(self):
        try:
            while True:
                payments = await self._poll_payments()
                for payment in payments:
                    payment_await_event = self._payment_awaits.get(
                        payment["identifier"]
                    )
                    if payment_await_event:
                        payment_await_event.set(payment)
                await asyncio.sleep(self._poll_interval)
        except asyncio.CancelledError:
            LOG.debug("Polling was cancelled")

    async def _stop(self):
        # TODO should be called when the class is teared down
        # (or when the run loop quits?)
        await self._session.close()
        # TODO await poll task here?

    @contextmanager
    def _create_payment_event(self, identifier):
        if self._payment_awaits.get(identifier):
            raise KeyError("Identifier already exists")

        event = asyncio.Event()
        self._payment_awaits[identifier] = event
        if not self.is_polling:
            # FIXME task need to be awaited somewhere, so that errors can raise etc
            self._poll_task = asyncio.create_task(self._run())
        yield event
        del self._payment_awaits[identifier]
        if not self._event_is_waiting:
            self._poll_task.cancel()

    # TODO types
    async def await_payment(
        self, identifier, expiration_time: datetime.datetime
    ) -> Tuple[PaymentStatus, Union["Payment", "TODO"]]:
        if self._payment_awaits.get(identifier):
            LOG.debug("Payment already awaited", identifier=identifier)
            return PaymentStatus.ERROR, None

        with self._create_payment_event(identifier) as event:
            try:
                await asyncio.wait_for(
                    event.wait(), timeout=seconds_until(expiration_time)
                )
                result = event.get()
                return PaymentStatus.SUCCESS, result
            except asyncio.TimeoutError:
                return PaymentStatus.TIMED_OUT, None
            except asyncio.CancelledError:
                raise NotImplementedError("Cancelling events is not implemented yet")
                return PaymentStatus.ERROR, None
