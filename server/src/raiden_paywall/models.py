import enum
from dataclasses import dataclass
import datetime
from sqlalchemy import Column, String, Boolean, Float, DateTime, PickleType, BigInteger, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from raiden_paywall.database import Base


class PaymentState(enum.Enum):
    """
    A Payment's lifecycle:
    1) AWAITED:
        A payment will be created when the payment's identifier is created upon a request
    2) PAID: 
        If a successful transfer is received before the timeout, the transfer is associated with 
        that identifier, and the identifier can be claimed in a request
    3) CLAIMED:
        If a identifier has been paid for, and the timeout is not exceeded,
        a request with the X-Raiden-Payment-Id set to the identifier will unlock the paywall,
        set the identifier to claimed and will invalidate the identifier for successive requests.
        The identifier can be re-used again in it's AWAITED state.
    4) TIMED_OUT:
        If the timeout is reached before an identifier reaches it's CLAIMED state,
        it will be set to the TIMED_OUT state and will be invalidated for requests.
        The identifier can be re-used again in it's AWAITED state.
    """
    AWAITED = 1
    PAID = 2
    TIMED_OUT = 3
    CLAIMED = 4

class NetworkId(enum.IntEnum):
    # TODO other networks
    GOERLI = 5


@dataclass
class Token(Base):
    __tablename__ = "token"

    address: str
    network_id: NetworkId
    decimals: int

    address = Column(String(42), unique=True, primary_key=True)
    network_id = Column(Enum(NetworkId))
    decimals = Column(Integer())


@dataclass
class Participant(Base):
    __tablename__ = "participant"

    address: str
    network_id: NetworkId

    address = Column(String(42), unique=True, primary_key=True)
    network_id = Column(Enum(NetworkId))


@dataclass
class Payment(Base):
    __tablename__ = "payment"

    id: str
    timeout: DateTime
    amount: float
    token: Token
    receiver: Participant

    # FIXME BigInteger is a SIGNED INT64!
    identifier = Column(BigInteger, primary_key=True, unique=False, autoincrement=False)
    counter = Column(Integer, primary_key=True, unique=False)
    timeout = Column(DateTime(), nullable=False)
    amount = Column(Float(), nullable=False)
    receiver_address = Column(String(42), ForeignKey('participant.address'))
    receiver =relationship("Participant", foreign_keys=[receiver_address])
    sender_address = Column(String(42), ForeignKey('participant.address'))
    sender = relationship("Participant", foreign_keys=[sender_address])
    token = relationship('Token', backref=backref('payments', lazy=True))
    token_address = Column(String(42), ForeignKey('token.address'), nullable=False)
    payment_event = Column(PickleType)
    claimed = Column(Boolean(), unique=False, default=False)

    @property
    def id(self):
        return str(self.identifier)

    @staticmethod
    def create_filter(identifier: int = None, state: PaymentState = None):
        base_filter = Payment.query
        if identifier:
            base_filter = base_filter.filter_by(identifier=identifier)
        if not state:
            return base_filter

        current_time = datetime.datetime.now()
        unclaimed_filter = base_filter.filter(Payment.timeout > current_time, Payment.claimed == False)
        if state == PaymentState.AWAITED:
            return unclaimed_filter.filter(Payment.payment_event == None)
        elif state == PaymentState.PAID:
            return unclaimed_filter.filter(Payment.payment_event != None)
        elif state == PaymentState.CLAIMED:
            return base_filter.filter(Payment.claimed == True)
        elif state == PaymentState.TIMED_OUT:
            # time out is valid for claiming!
            return base_filter.filter(Payment.claimed == False).filter(Payment.timeout <= current_time)

