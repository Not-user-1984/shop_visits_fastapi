from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models import Order


async def order_exists(
        db: Session,
        order_data: dict , customer_id: int
) -> bool:
    stmt = select(Order).where(
        Order.author_id == customer_id,
        Order.where_id == order_data.trade_point_id,
        Order.status == 'started'
    )
    result = await db.execute(stmt)
    existing_order = result.first()
    return existing_order is not None
