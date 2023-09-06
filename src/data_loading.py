import datetime
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings
from db.database import Base
from db.models import Customer, Order, OrderStatus, TradePoint, Worker


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
        ended_at=(datetime.datetime.utcnow()+ datetime.timedelta(days=random.randint(1, 30))),
        where_id=random.randint(1, 10),
        author_id=random.randint(1, 50),
        status=OrderStatus.started
    )


def main():
    engine = create_engine(settings.DATABASE_URL, echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()
    try:
        for i in range(1, 31):
            trade_point = TradePoint(name=f"TradePoint-{i}", id=i)
            session.add(trade_point)
        session.commit()
        for i in range(1, 201):
            worker = create_random_worker(i)
            session.add(worker)
            session.commit()

        for i in range(1, 201):
            customer = create_random_customer(i)
            session.add(customer)
            session.commit()

        for i in range(1, 151):
            order = create_random_order(i)
            session.add(order)
            session.commit()
        print("Записи успешно созданы!")
    except Exception as e:
        session.rollback()
        print(f"Произошла ошибка: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
