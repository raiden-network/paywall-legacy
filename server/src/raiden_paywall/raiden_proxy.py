import datetime
import time
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import Optional, Tuple, Union

import requests
import structlog
from raiden.api.v1.encoding import PaymentSchema

LOG = structlog.get_logger()


class RaidenNode:
    def __init__(self, endpoint, token_address, num_connection_retries=20):
        self._base_url = endpoint + "/api/v1"
        self.token_address = token_address
        self.wait_for_raiden_api(num_retries=num_connection_retries)
        self.address = self._get_raiden_address()



    def wait_for_raiden_api(self, num_retries=20):
        counter = 0
        # TODO make this exponential backoff
        # TODO make ait time config parameter
        while counter < num_retries:
            response = requests.get(f"{self._base_url}/info")
            if response.status_code == 200:
                break
            elif response.status_code == 503:
                LOG.info(f"Raiden Node is starting up, waiting for Raiden API to be available.\
                         Remaining retries: {num_retries - counter + 1}")
                time.sleep(2)
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
