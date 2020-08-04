"""Models."""

from app import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, \
    ForeignKey
from typing import Any


class Client(Base):
    """Client model."""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_vip = Column(Boolean, nullable=False)

    def __init__(self, name: str, is_vip: str):
        """Initializing."""
        self.name = name
        self.is_vip = is_vip


class Driver(Base):
    """Driver model."""

    __tablename__ = 'drivers'

    id: Any = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    car = Column(String, nullable=False)

    def __init__(self, name: str, car: str):
        """Initializing."""
        self.name = name
        self.car = car


class Order(Base):
    """Order model."""

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    address_from = Column(String, nullable=False)
    address_to = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    date_created = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    def __init__(self, address_from: str, address_to: str,
                 client_id: int, driver_id: int,
                 date_created, status: str) -> None:
        """Initializing."""
        self.address_from = address_from
        self.address_to = address_to
        self.client_id = client_id
        self.driver_id = driver_id
        self.date_created = date_created
        self.status = status


Base.metadata.create_all(engine)
