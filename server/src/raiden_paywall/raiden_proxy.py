import asyncio
import datetime
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import Optional, Tuple, Union

import aiohttp
import requests
import structlog
from raiden.api.v1.encoding import PaymentSchema

LOG = structlog.get_logger()


class RaidenNode:
    def __init__(self, endpoint, token_address):
        self._base_url = endpoint + "/api/v1"
        self.token_address = token_address
        self.wait_for_raiden_api()
        self.address = self._get_raiden_address()



    def wait_for_raiden_api(self):
        return asyncio.wait(self._wait_for_raiden_api, num_retries=20)


    async def _wait_for_raiden_api(self, num_retries=20):
        counter = 0
        # TODO make retries and wait time parameters
        # make this exponential backoff
        while counter < num_retries:
            response = requests.get(f"{self._base_url}/info")
            if response.status_code == 200:
                break
            elif response.status_code == 503:
                LOG.info(f"Raiden Node is starting up, waiting for Raiden API to be available.\
                         Remaining retries: {num_retries - counter + 1}")
                await asyncio.sleep(2)
                counter += 1
                continue
            else:
                response.raise_for_status()


    def _get_raiden_address(self):
        response = requests.get(f"{self._base_url}/address")
        return response.json()["our_address"]

    def get_payments(self):
        return list(self.iter_payments())

    def iter_payments(self):
        response = requests.get(f"{self._base_url}/payments/{self.token_address}")
        # TODO error handling etc for payment in response.json():
        for payment in response.json():
            if payment["event"] == "EventPaymentReceivedSuccess":
                yield payment

    @classmethod
    def from_config(cls, config):
        if not (endpoint := config.get("RD_API_ENDPOINT")):
            raise KeyError("Config required")
        if not (token_address := config.get("RD_TOKEN_ADDRESS")):
            raise KeyError("Config required")
        return cls(endpoint, token_address)
