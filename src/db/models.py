import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Энумерация для статусов заказа
class OrderStatus(PyEnum):
    started = 'started'
    ended = 'ended'
    in_process = 'in process'
    awaiting = 'awaiting'
    canceled = 'canceled'


class RoleEnum(PyEnum):
    worker = "Worker"
    customer = "Customer"


class TradePoint(Base):
    __tablename__ = 'trade_points'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    users = relationship("User", backref="trade_point", lazy=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    role = Column(Enum('Worker',
                       'Customer',
                       name='user_roles'), nullable=False)

    # Добавьте другие связи, например, с таблицами Order, Visit и т. д.
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
