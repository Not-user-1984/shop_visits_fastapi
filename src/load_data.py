import random
import datetime
from enum import Enum as PyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from db.models import TradePoint, Worker, Customer, Order, Visit , OrderStatus


from config import settings

from db.database import Base



def create_random_worker(i):
    return Worker(
        id=i,
        name=f"Worker-{random.randint(1, 1000)}",
        phone_number=f"+7{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        trade_point_id=random.randint(1, 10),
        is_blocked=random.choice([True, False])
    )


def create_random_customer(i):
    return Customer(
        id=i,
        name=f"Customer-{random.randint(1, 1000)}",
        phone_number=f"+7{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    )

def create_random_order(i):
    return Order(
        id=i,
        created_at=datetime.datetime.utcnow(),
        ended_at=datetime.datetime.utcnow() + datetime.timedelta(days=random.randint(1, 30)),
        where_id=random.randint(1, 10),
        author_id=random.randint(1, 50),
        status=random.choice([OrderStatus.started, OrderStatus.ended, OrderStatus.in_process])
    )

def create_random_visit(i):
    return Visit(
        id=i,
        created_at=datetime.datetime.utcnow(),
        executor_id=random.randint(1, 50),
        order_id=random.randint(1, 50),
        author_id=random.randint(1, 50),
        where_id=random.randint(1, 10)
    )

def main():
    engine = create_engine(settings.DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    
    session = Session()
    try:
        for i in range(1, 11):
            trade_point = TradePoint(name=f"TradePoint-{i}",
                                    id=i)
            session.add(trade_point)
        session.commit()

        for i in range(random.randint(50)):
            worker = create_random_worker(i)
            session.add(worker)
            session.commit()

        for i in range(random.randint(50)):
            customer = create_random_customer(i)
            session.add(customer)
            session.commit()

        for i in range(random.randint(50)):
            order = create_random_order(i)
            session.add(order)
            session.commit()

        for i in range(random.randint(15)):
            visit = create_random_visit(i)
            session.add(visit)
            session.commit()
        print("Записи успешно созданы!")
    except Exception as e:
        session.rollback()
        print(f"Произошла ошибка: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
