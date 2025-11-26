"""
API routes module for E-commerce API.
"""

from . import auth, users, products, orders

__all__ = [
    "auth",
    "users", 
    "products",
    "orders"
]