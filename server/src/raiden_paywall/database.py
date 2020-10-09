from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import _app_ctx_stack


SQLALCHEMY_DATABASE_URI = 'sqlite:///paywall.db'
# TODO necessary?
SQLALCHEMY_TRACK_MODIFICATIONS = False


engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine),
                            scopefunc=_app_ctx_stack.__ident_func__)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import raiden_paywall.models
    Base.metadata.create_all(bind=engine)


import requests
from threading import Timer
from .models import Payment, PaymentState
import time


from raiden.api.v1.encoding import EventPaymentReceivedSuccessSchema

PaymentReceivedSchema = EventPaymentReceivedSuccessSchema()



from typing import Union
import decimal
from decimal import localcontext


def to_absolute_amount(number: Union[float, str], decimals: int) -> int:
    if isinstance(number, str):
        d_number = decimal.Decimal(value=number)
    elif isinstance(number, float):
        d_number = decimal.Decimal(value=str(number))
    else:
        raise TypeError("Unsupported type.  Must be one of integer, float, or string")

    s_number = str(number)
    unit_value = decimal.Decimal(10 ** decimals)


    if d_number == decimal.Decimal(0):
        return 0

    if d_number < 1 and "." in s_number:
        with localcontext() as ctx:
            # '0.000001'
            # 8 - 1 - 1 = 6
            multiplier = len(s_number) - s_number.index(".") - 1

            ctx.prec = multiplier
            d_number = decimal.Decimal(value=number, context=ctx) * 10 ** multiplier
        unit_value /= 10 ** multiplier

    with localcontext() as ctx:
        ctx.prec = 999
        result_value = decimal.Decimal(value=d_number, context=ctx) * unit_value

    if result_value < 0 or result_value > 2** 256 - 1:
        raise ValueError("Resulting token value must be between 1 and 2**256 - 1")

    return int(result_value)


def database_update_payments(raiden):
    # Data cannot be passed as a param because it will be prefetched
    # by the thread and reused.
    session = db_session()
    try:
        awaited = Payment.create_filter(identifier=None, state=PaymentState.AWAITED).with_for_update(of=Payment)
        if awaited.first():
            id_payment_map = {payment.identifier: payment for payment in awaited}
            for raiden_payment in raiden.iter_payments():
                    payment = id_payment_map.get(int(raiden_payment["identifier"]))
                    if payment:
                        if int(raiden_payment['amount']) >= to_absolute_amount(payment.amount, payment.token.decimals):
                            # TODO with lock payment row
                            # TODO parse and create object, or directly save the json string in db?
                            print("Found payment:", raiden_payment)
                            payment_received_event = PaymentReceivedSchema.make_object(raiden_payment)
                            payment.payment_event = payment_received_event
            session.commit()

    except Exception as e :
        print(f"There was an Error: {e}")


def start_raiden_db_thread(raiden):
    class RepeatTimer(Timer):
        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)

    thread = RepeatTimer(0.5, database_update_payments, [raiden])
    # FIXME this will not shutdown the database connection gracefully:
    #   see: https://docs.python.org/3/library/threading.html#thread-objects
    # Also close db connection in the end
    thread.daemon = True
    thread.start()
    return thread
