from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.order import Order, OrderItem, OrderStatus, PaymentStatus
from app.schemas.order import OrderResponse, OrderCreate, OrderUpdate
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.product import Product
from app.services.order import get_orders, get_order_by_id, create_order, update_order_status, cancel_order

router = APIRouter()

@router.get("/", response_model=List[OrderResponse])
def read_orders(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[OrderStatus] = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Order).filter(Order.customer_id == current_user.id)

    if status:
        query = query.filter(Order.status == status)

    orders = query.offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(
    order_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    order = get_order_by_id(db, order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.post("/", response_model=OrderResponse)
def create_order_endpoint(
    order: OrderCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    return create_order(db, order, current_user.id)

@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status_endpoint(
    order_id: int, 
    order_status: OrderStatus, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if order exists
    order = get_order_by_id(db, order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Only allow status updates for admins or vendors
    if current_user.role not in ["admin", "vendor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins or vendors can update order status"
        )

    return update_order_status(db, order_id, order_status, current_user.id)

@router.put("/{order_id}/payment-status")
def update_payment_status(
    order_id: int, 
    payment_status: PaymentStatus, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if order exists
    order = get_order_by_id(db, order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Only allow payment status updates for admins
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update payment status"
        )

    order.payment_status = payment_status
    db.commit()
    db.refresh(order)

    return {"message": f"Payment status updated to {payment_status}"}

@router.put("/{order_id}")
def update_order(
    order_id: int, 
    order_update: OrderUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if order exists
    order = get_order_by_id(db, order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Only allow updating shipping and billing addresses for customers
    if current_user.role == "customer":
        update_data = order_update.dict(exclude_unset=True, exclude={"status", "payment_status"})
        for key, value in update_data.items():
            setattr(order, key, value)

        db.commit()
        db.refresh(order)
        return order

    # For admins and vendors, allow all updates
    update_data = order_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}")
def cancel_order_endpoint(
    order_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    order = cancel_order(db, order_id, current_user.id)
    return {"message": "Order cancelled successfully"}