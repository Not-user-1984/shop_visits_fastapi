from sqladmin import ModelView
from db.models import TradePoint,  Worker, Customer, Order, Visit


class TradePointAdmin(ModelView, model=TradePoint):
    column_list = [
        TradePoint.id,
        TradePoint.name
    ]


class WorkerAdmin(ModelView, model=Worker):
    column_list = [
        Worker.id,
        Worker.name,
        Worker.phone_number,

    ]
    column_details_list = [
        Worker.orders,
        Worker.trade_point_id,
        Worker.visits,
    ]
    column_searchable_list = [Worker.name, Worker.phone_number]


class CustomerAdmin(ModelView, model=Customer):
    column_list = [
        Customer.id,
        Customer.name,
        Customer.phone_number,

    ]
    column_searchable_list = [
        Customer.name,
        Customer.phone_number,
        ]
    column_details_list = [
        Customer.customer_orders,
        Customer.visits,
        Customer.trade_points
    ]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.created_at,
        Order.ended_at,
        Order.status,
        Order.visits
    ]
    column_searchable_list = [Order.created_at]


class VisitAdmin(ModelView, model=Visit):
    column_list = [
        Visit.id,
        Visit.created_at,
        Visit.executor_id,
        Visit.order_id,
        Visit.author_id,
        Visit.where_id
    ]
