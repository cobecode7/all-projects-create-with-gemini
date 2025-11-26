"""
Services module for the E-commerce API.
"""

from .auth import register_user, authenticate_user
from .user import get_users, get_user_by_id, get_user_by_email, create_user, update_user, delete_user
from .product import get_products, get_product_by_id, create_product, update_product, delete_product, get_categories, get_category_by_id
from .order import get_orders, get_order_by_id, create_order, update_order_status, cancel_order

__all__ = [
    "register_user",
    "authenticate_user",
    "get_users",
    "get_user_by_id",
    "get_user_by_email",
    "create_user",
    "update_user",
    "delete_user",
    "get_products",
    "get_product_by_id",
    "create_product",
    "update_product",
    "delete_product",
    "get_categories",
    "get_category_by_id",
    "get_orders",
    "get_order_by_id",
    "create_order",
    "update_order_status",
    "cancel_order"
]