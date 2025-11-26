
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate

def get_orders(db: Session, customer_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).filter(Order.customer_id == customer_id).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: int, customer_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id, Order.customer_id == customer_id).first()

def create_order(db: Session, order: OrderCreate, customer_id: int) -> Order:
    # Create order with initial values
    db_order = Order(
        customer_id=customer_id,
        status=OrderStatus.PENDING,
        payment_status=PaymentStatus.PENDING,
        total=0,
        subtotal=0
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    subtotal = 0
    for item in order.items:
        # Check if product exists and is active
        product = db.query(Product).filter(Product.id == item.product_id, Product.is_active == True).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )

        # Check if enough quantity is available
        if product.track_quantity and product.quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough quantity for product {product.name}. Available: {product.quantity}, Requested: {item.quantity}"
            )

        # Calculate item total
        item_total = product.price * item.quantity
        subtotal += item_total

        # Create order item
        db_order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price,
            total=item_total
        )
        db.add(db_order_item)

        # Update product quantity if tracking is enabled
        if product.track_quantity:
            product.quantity -= item.quantity
            db.add(product)

    # Update order totals
    tax = subtotal * 0.1  # 10% tax
    shipping = 10 if subtotal < 100 else 0  # Free shipping for orders over 100
    total = subtotal + tax + shipping

    db_order.subtotal = subtotal
    db_order.tax = tax
    db_order.shipping = shipping
    db_order.total = total

    db.commit()
    db.refresh(db_order)
    return db_order

def update_order_status(db: Session, order_id: int, status: OrderStatus, customer_id: int) -> Order:
    db_order = get_order_by_id(db, order_id, customer_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def cancel_order(db: Session, order_id: int, customer_id: int) -> Order:
    db_order = get_order_by_id(db, order_id, customer_id)
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Only allow cancellation if order is in pending or confirmed status
    if db_order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel order in current status"
        )

    # Restore product quantities
    for item in db_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product and product.track_quantity:
            product.quantity += item.quantity
            db.add(product)

    db_order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(db_order)
    return db_order
