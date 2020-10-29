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
        # initially, there is a restricted wait time - if we can't connect
        # raise an exception
        success = self.wait_for_raiden_api(num_retries=num_connection_retries)
        if not success:
            raise ConnectionError(f"Raiden API is not available at {self._base_url}.")
        self.address = self._get_raiden_address()

    def get_or_wait(self, url):
        response = None
        while response is None:
            try:
                response = requests.get(url)
                json = response.json()
                if type(json) is not list:
                    errors = json.get('errors')
                    if errors:
                        LOG.info(errors)
                        response = None
                        continue
            except requests.ConnectionError as e:
                LOG.info(f"Error while accessing the Raiden API: {e}")
                self.wait_for_raiden_api()
        return response


    def wait_for_raiden_api(self, num_retries=None):
        """
        Try to poll the /status endpoint of the Raiden API
        until it is 'ready'.
        If num_retries is None, it will try infinitely

        """
        counter = 0
        while True:
            try:
                response = requests.get(f"{self._base_url}/status")
                if response.status_code == 200:
                    if response.json()['status'] == 'ready':
                        return True
                elif response.status_code == 503:
                    LOG.info(f"Raiden Node is starting up, waiting for Raiden API to be available.")
                else:
                    response.raise_for_status()
            except requests.ConnectionError as e:
                LOG.info(f"Error while accessing the Raiden API: {e}")

            time.sleep(2)
            if num_retries is not None:
                if counter < num_retries:
                    counter += 1
                else:
                    break
        return False

    def _get_raiden_address(self):
        response = self.get_or_wait(f"{self._base_url}/address")
        return response.json()["our_address"]

    def get_payments(self):
        return list(self.iter_payments())

    def iter_payments(self):
        response = self.get_or_wait(f"{self._base_url}/payments/{self.token_address}")
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
