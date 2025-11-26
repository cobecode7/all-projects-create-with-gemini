"""
Utilities module for the E-commerce API.
"""

from .database import get_db
from .init_db import init_db

__all__ = [
    "get_db",
    "init_db"
]