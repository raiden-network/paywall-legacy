import datetime
import json
import logging
import random
from dataclasses import dataclass
from decimal import ROUND_UP, Decimal, getcontext
from functools import wraps
from typing import Any, Optional

import requests
from flask import (
    Flask,
    _app_ctx_stack,
    abort,
    current_app,
    g,
    jsonify,
    make_response,
    redirect,
    request,
    url_for,
)
from flask.globals import _app_ctx_err_msg
from flask.logging import default_handler
from pytimeparse import parse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func

from raiden_paywall.database import db_session, init_db
from raiden_paywall.models import NetworkId, Participant, Payment, PaymentState, Token
from raiden_paywall.raiden import RaidenNode

root = logging.getLogger()
root.addHandler(default_handler)

log = logging.getLogger("werkzeug")


def get_or_create(model, **kwargs):
    instance = db_session().query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db_session().add(instance)
        return instance


def prepare_response(response, payment):
    response.headers["X-Raiden-Payment-Id"] = payment.identifier
    return response


def register_ctx_proxy(name, init_value):
    def getter(obj):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, name):
                setattr(ctx, name, init_value)
            return getattr(ctx, name)
        else:
            raise RuntimeError(_app_ctx_err_msg)

    def setter(obj, value):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            setattr(ctx, name, value)
        else:
            raise RuntimeError(_app_ctx_err_msg)

    return property(getter, setter)


@dataclass
class PaymentConfig:

    receiver_address: str
    token_address: str
    token_decimals: int
    network_id: NetworkId
    default_timeout: datetime.timedelta = datetime.timedelta(minutes=10)
    default_amount: float = 0.0001

    @property
    def token(self):
        return Token.query.get(self.token_address)

    @property
    def receiver(self):
        return Participant.query.get(self.receiver_address)

    def init_database(self):
        token = get_or_create(
            Token,
            address=self.token_address,
            decimals=self.token_decimals,
            network_id=self.network_id,
        )
        receiver = get_or_create(
            Participant, address=self.receiver_address, network_id=self.network_id
        )
        db_session().commit()

    @classmethod
    def from_config(cls, config):
        if not (token_address := config.get("RD_TOKEN_ADDRESS")):
            raise KeyError("Config necessary!")

        if not (token_decimals := config.get("RD_TOKEN_DECIMALS")):
            raise KeyError("Config necessary!")

        if not (receiver_address := config.get("RD_RECEIVER_ADDRESS")):
            raise KeyError("Config necessary!")

        if not (network_id := config.get("RD_NETWORK_ID")):
            raise KeyError("Config necessary!")

        if (default_timeout := config.get("RD_DEFAULT_TIMEOUT")) :
            default_timeout = parse_to_timedelta(default_timeout)

        default_amount = config.get("RD_DEFAULT_AMOUNT")
        return cls(
            receiver_address=receiver_address,
            token_address=token_address,
            token_decimals=int(token_decimals),
            default_timeout=default_timeout,
            default_amount=Decimal(default_amount),
            network_id=NetworkId(int(network_id)),
        )


def parse_to_timedelta(input_str):
    try:
        if input_str:
            seconds = parse(input_str)
            return datetime.timedelta(seconds=seconds)
    except Exception:
        return None
    return None


class RaidenPaywall(object):
    """
    Expects the following flask config arguments, exemplary:

            RD_TOKEN_ADDRESS="0xC563388e2e2fdD422166eD5E76971D11eD37A466"
            RD_TOKEN_DECIMALS='18'
            RD_NETWORK_ID='5'
            RD_DEFAULT_TIMEOUT="10mins"
            RD_DEFAULT_AMOUNT='0.001'
            RD_API_ENDPOINT='http://localhost:5002'

    This should be exposed in a config file,
    and the path of the file is set as environment variable:

    e.g.:

    export RAIDEN_PAYWALL_SETTINGS=/path/to/settings.cfg;
    """

    amount = register_ctx_proxy("raiden_paywall_amount", Decimal("0."))
    _claimed_payment = register_ctx_proxy("raiden_paywall_claimed_paymed", False)
    _preview = register_ctx_proxy("raiden_paywall_preview", None)

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        init_db()

        app.config.from_envvar("RAIDEN_PAYWALL_SETTINGS")
        # TODO handling of when receiver address is specified in config
        # (e.g. consistency checking with DB and raiden node)
        raiden = RaidenNode.from_config(app.config)
        app.config["RD_RECEIVER_ADDRESS"] = raiden.address

        self.config = PaymentConfig.from_config(app.config)
        self.config.init_database()

        app.teardown_appcontext(self.teardown)
        app.after_request(self._modify_response)

    def teardown(self, exception):
        db_session.remove()

    def _modify_response(self, response):
        if self.amount:
            if not self._claimed_payment or self._preview:
                return self.make_payment_response(preview=self._preview)
        return response

    def preview(self, preview: Any) -> Any:
        self._preview = preview
        return preview

    def check_payment(self) -> bool:
        """
        Returns:
            A buffered writable file descriptor
        """
        if self.amount == Decimal("0."):
            return True
        payment_id = request.headers.get("X-Raiden-Payment-Id")
        if payment_id:
            payment = (
                Payment.create_filter(
                    identifier=int(payment_id), state=PaymentState.PAID
                )
                .with_for_update(of=Payment)
                .one_or_none()
            )
            if payment:
                payment.claimed = True
                db_session().commit()
                # This signals that the payment was checked and successfully claimed in this request
                self._claimed_payment = True
                return True
        return False

    def make_payment_response(self, preview=None):
        return make_response(self._make_payment_response(preview=preview))

    def _make_payment_response(self, preview=None):
        payment_id = request.headers.get("X-Raiden-Payment-Id")
        if payment_id:
            log.info(f"Found id in header: {payment_id}")
            payment_id = int(payment_id)
            payment = Payment.create_filter(
                identifier=payment_id, state=PaymentState.PAID
            ).one_or_none()
            if payment:
                assert False, "The payment should have been claimed in this request"
            payment = Payment.create_filter(
                identifier=payment_id, state=PaymentState.AWAITED
            ).one_or_none()
            if payment:
                log.info(f"Payment not redeemable yet: {payment}")
                return jsonify(payment=payment, preview=preview), 401
            else:
                return "Specified X-Raiden-Payment-Id is not awaited.", 404
        payment = await_payment(
            self.config.receiver,
            self.config.token,
            self.amount,
            self.config.default_timeout,
        )
        if payment_id:
            return jsonify(payment=payment, preview=preview), 401
        else:
            log.info(jsonify(payment))
            return jsonify(payment=payment, preview=preview), 402


def await_payment(
    receiver: Participant, token: Token, amount: Decimal, timeout: datetime.timedelta
) -> "Payment":
    try:
        tries = 0
        while tries <= 5:
            one_awaited = True
            while one_awaited:
                # FIXME 2**64 is within bruteforce reach! Fix raiden ids!
                # FIXME SQL BigInt is a signed int64! for now, we constrain
                # the ids to be smaller in the positive range, but this
                # decreases collision resistance significantly even further
                payment_id = random.randint(0, 2 ** 63 - 1)
                filter_ = Payment.create_filter(payment_id, PaymentState.AWAITED)
                one_awaited = filter_.one_or_none()
                # FIXME if all possible payment_id's are in state AWAITED,
                # this blocks/ queries until it finds a free id again.
                # Probably this is what we want though ...?

            session = db_session()
            subqry = session.query(func.max(Payment.counter)).filter(
                Payment.identifier == payment_id
            )
            qry = (
                session.query(Payment)
                .filter(Payment.identifier == payment_id, Payment.counter == subqry)
                .one_or_none()
            )

            if qry:
                counter = qry.counter + 1
            else:
                counter = 0

            rounded_amount = amount.quantize(
                Decimal(f"10e-{str(token.decimals)}"), rounding=ROUND_UP
            )
            payment = Payment(
                identifier=int(payment_id),
                counter=counter,
                amount=str(rounded_amount),
                timeout=datetime.datetime.now() + timeout,
                receiver=receiver,
                token=token,
            )

            session.add(payment)
            session.commit()
            return payment
    except IntegrityError as e:
        tries += 1
        if tries == 5:
            raise e
