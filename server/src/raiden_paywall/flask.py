from functools import wraps
from flask import g, request, redirect, url_for, make_response, current_app
from flask_cors import CORS
from dataclasses import dataclass 
import json 
import logging
import random

import requests
import datetime


from flask.logging import default_handler

root = logging.getLogger()
root.addHandler(default_handler)

log = logging.getLogger('werkzeug')
log.info('test logging')

@dataclass
class PaymentInformation:
    amount: float
    identifier: int
    token: 'Address'
    receiver: 'Address'
    timeout: 'UTC'
    token_decimal: int = 10

    def to_json(self):
        dic = {
            'amount': str(self.amount),
            'identifier': str(self.identifier),
            'token': str(self.token),
            'receiver': str(self.receiver),
            'timeout': str(self.timeout),
        }
        return json.dumps(dic)

    def to_payment_url(self, light_client_base):
        # TODO convert absolute amount to decimal amount
        # FIXME remove hardcoded amount
        return f'{light_client_base}/#/transfer/{self.token}/{self.receiver}/{self.identifier}?amount={self.amount}'

class PaymentService:
    """
    Simple class, just querying the raiden api naively with no caching
    and keeping the state of ID reusage etc in memory.
    Prototype used for DEVELOPMENT ONLY!
    """
    DEFAULT_TIMEOUT = datetime.timedelta(minutes=10)

    def __init__(self, raiden_address, token_address):
        self._payments_awaited = {}
        self._address = raiden_address + '/api/v1'
        self.token_address = token_address
        self._redeemed_payments = set()
        # TODO get receiver address from raiden node
        self.raiden_address = self._get_raiden_address()

    @property
    def payments_awaited(self):
        return self._payments_awaited

    def _get_raiden_address(self):
        response = requests.get(f"{self._address}/address")
        # TODO error handling
        return response.json()['our_address']

    @property
    def timeout(self):
        return self.DEFAULT_TIMEOUT


    def _calculate_timeout(self):
        return datetime.datetime.now() + self.timeout

    def payment_exists(self, identifier, amount):
        response = requests.get(f"{self._address}/payments/{self.token_address}")
        # TODO error handling etc
        for payment in response.json():
            # we don't care if the user paid too much, it's their probleml
            if payment['event'] == "EventPaymentReceivedSuccess":
                if int(payment["identifier"]) == int(identifier) and int(payment["amount"]) >= int(amount):
                    log.info(f"Found payment in raiden: {identifier}")
                    return True
        log.info(f"Didn't find payment in raiden: {identifier}")
        return False

    def schedule_payment(self, amount):
        # FIXME 2**64 is within bruteforce reach! Fix raiden ids!
        payment_id = random.randint(0, 2**64 - 1)
        if payment_id in set(self._payments_awaited.keys()):
            return self.schedule_payment(amount)
        # TODO convert to absolute amount with the decimals
        log.info(f"Payment scheduled: id={payment_id}, amount={amount}")
        payment_information = PaymentInformation(
            amount=amount,
            identifier=int(payment_id),
            token=self.token_address,
            receiver=self.raiden_address,
            timeout=self._calculate_timeout()
        )
        self._payments_awaited[payment_id] = payment_information
        return payment_information

    def redeem_payment(self, payment_id):
        # if it was scheduled, it automatically is paid for
        assert type(payment_id) is int
        payment_information = self.payments_awaited.get(payment_id)
        if not payment_information:
            return False
        if self.payment_exists(payment_id, payment_information.amount):
            if payment_id in self._redeemed_payments:
                return False
            del self._payments_awaited[payment_id]
            self._redeemed_payments.add(payment_id)
            return True



def prepare_response(response, payment):
    response.headers['X-Raiden-Payment-Id'] = payment.identifier
    return response


def paywalled(raiden, amount):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # If a payment Id is present it is assumed that the requester
            # knows he is requesting 
            payment_id = request.headers.get('X-Raiden-Payment-Id')
            if payment_id:
                log.info(f"Found id in header: {payment_id}")
                payment_id = int(payment_id)
                payment_information = raiden.payments_awaited.get(payment_id)
                if payment_information:
                    log.info(f"Payment awaited: {payment_information}")
                    # this means the requester knows this is an endpoint,
                    # and tries to redeem a token!
                    if raiden.redeem_payment(payment_id) is True:
                        # If redeemable return the resource function that is decorated
                        return f(*args, **kwargs)
                    else:
                        # TODO here we could implement long polling or block for 
                        # some seconds until the transfer arrives
                        log.info(f"Payment not redeemable yet: {payment_information}")
                        return payment_information.to_json(), 401
            payment_information = raiden.schedule_payment(amount)
            if payment_id:
                return payment_information.to_json(), 401
            else:
                log.info(payment_information.to_json())
                return payment_information.to_json(), 402
        return decorated_function
    return decorator


from flask import Flask
app = Flask(__name__)
CORS(app)

raiden_api = 'http://localhost:5002'
token_address = "0xC563388e2e2fdD422166eD5E76971D11eD37A466"
amount_to_pay = 0.001
raiden = PaymentService(raiden_api, token_address)

# FIXME this relies on global state, which is not Thread/ process safe!!
# Right now this is a very hacky single thread, development solution.
# Later on, we need to either call the raiden api from every context naively (heavier processing load)
# or create a separate worker that polls the raiden api for registered payment ids and keeps them
# in a database. This would serve as a mediating layer between different contexts / threads/ processes


@app.route('/')
@paywalled(raiden, amount_to_pay)
def get_expensive_stuff():
    return f"$$$ You paid {amount_to_pay} token to see this boring message! $$$"
