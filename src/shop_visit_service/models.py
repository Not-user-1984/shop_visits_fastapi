from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


# Энумерация для статусов заказа
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
    workers = relationship("Worker", backref="trade_point", lazy=True)
    customers = relationship("Customer", backref="trade_point", lazy=True)


class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    trade_point_id = Column(
        Integer, ForeignKey('trade_points.id'),
        nullable=False)
    visits = relationship("Visit", backref="executor", lazy=True)


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    trade_point_id = Column(
        Integer, ForeignKey('trade_points.id'), nullable=False)
    orders = relationship("Order", backref="author", lazy=True)
    visits = relationship("Visit", backref="author", lazy=True)


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


class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    executor_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    where_id = Column(Integer, ForeignKey('trade_points.id'), nullable=False)
