import datetime
from enum import Enum as PyEnum

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class OrderStatus(PyEnum):
    started = 'started'
    ended = 'ended'
    in_process = 'in process'
    awaiting = 'awaiting'
    canceled = 'canceled'


class TradePoint(Base):
    __tablename__ = 'trade_points'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    trade_point_id = Column(
        Integer, ForeignKey('trade_points.id'), nullable=False)
    is_blocked = Column(Boolean, default=False)
    visits = relationship("Visit", backref="executor", lazy=True)
    orders = relationship("Order", backref="author", lazy=True)

    def __str__(self):
        return str(self.name)


customer_trade_points = Table(
    'customer_trade_points', Base.metadata,
    Column('customer_id', Integer, ForeignKey('customers.id')),
    Column('trade_point_id', Integer, ForeignKey('trade_points.id'))
)


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    customer_orders = relationship("Order", backref="customer", lazy=True)
    visits = relationship("Visit", backref="customer", lazy=True)
    trade_points = relationship(
        "TradePoint",
        secondary=customer_trade_points,
        backref="customers"
    )

    def __str__(self):
        return str(self.name)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = Column(DateTime)
    where_id = Column(Integer, ForeignKey('trade_points.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    executor_id = Column(Integer, ForeignKey('workers.id'))
    visits = relationship("Visit", backref="order", uselist=False, lazy=True)

    def __str__(self):
        return str(self.created_at)


class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    executor_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    where_id = Column(Integer, ForeignKey('trade_points.id'), nullable=False)

    def __str__(self):
        return str(self.created_at)
