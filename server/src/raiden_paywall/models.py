import datetime
import enum
from dataclasses import dataclass

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    PickleType,
    String,
    Text,
)
from sqlalchemy.orm import backref, relationship

from raiden_paywall.database import Base


class PaymentState(enum.Enum):
    AWAITED = 1
    PAID = 2
    TIMED_OUT = 3
    CLAIMED = 4


class NetworkId(enum.IntEnum):
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
    amount: str
    token: Token
    receiver: Participant

    identifier = Column(BigInteger, primary_key=True, unique=False, autoincrement=False)
    counter = Column(Integer, primary_key=True, unique=False)
    timeout = Column(DateTime(), nullable=False)
    amount = Column(Text, nullable=False)
    receiver_address = Column(String(42), ForeignKey("participant.address"))
    receiver = relationship("Participant", foreign_keys=[receiver_address])
    sender_address = Column(String(42), ForeignKey("participant.address"))
    sender = relationship("Participant", foreign_keys=[sender_address])
    token = relationship("Token", backref=backref("payments", lazy=True))
    token_address = Column(String(42), ForeignKey("token.address"), nullable=False)
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
        unclaimed_filter = base_filter.filter(
            Payment.timeout > current_time, Payment.claimed == False
        )
        if state == PaymentState.AWAITED:
            return unclaimed_filter.filter(Payment.payment_event == None)
        elif state == PaymentState.PAID:
            return unclaimed_filter.filter(Payment.payment_event != None)
        elif state == PaymentState.CLAIMED:
            return base_filter.filter(Payment.claimed == True)
        elif state == PaymentState.TIMED_OUT:
            # time out is valid for claiming!
            return base_filter.filter(Payment.claimed == False).filter(
                Payment.timeout <= current_time
            )
