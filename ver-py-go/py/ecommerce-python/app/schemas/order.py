from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.product import ProductResponse
from app.models.order import OrderStatus, PaymentStatus

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    price: float
    total: float
    product: ProductResponse

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    order_number: Optional[str] = None
    total: Optional[float] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = 0
    shipping: Optional[float] = 0
    discount: Optional[float] = 0
    status: Optional[OrderStatus] = OrderStatus.PENDING
    payment_status: Optional[PaymentStatus] = PaymentStatus.PENDING
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class PaymentRequest(BaseModel):
    order_id: int
    payment_method: str
    amount: float

class PaymentResponse(BaseModel):
    id: int
    order_id: int
    payment_method: str
    amount: float
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True