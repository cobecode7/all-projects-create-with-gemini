from sqlalchemy import Column, String, Text, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    compare_price = Column(Float)
    cost = Column(Float)
    sku = Column(String, unique=True)
    barcode = Column(String)
    track_quantity = Column(Boolean, default=True)
    quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_digital = Column(Boolean, default=False)
    
    # Foreign Keys
    vendor_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Relationships
    vendor = relationship("User", back_populates="products")
    category = relationship("Category")
    order_items = relationship("OrderItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")

class Category(BaseModel):
    __tablename__ = "categories"
    
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey("categories.id"))

class Review(BaseModel):
    __tablename__ = "reviews"
    
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    is_approved = Column(Boolean, default=False)
    
    # Foreign Keys
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    product = relationship("Product", back_populates="reviews")
    customer = relationship("User")