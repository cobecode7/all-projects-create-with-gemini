from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.product import Product, Category
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate, CategoryResponse
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.services.product import get_products, get_product_by_id, create_product, update_product, delete_product, get_categories, get_category_by_id

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def read_products(
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search term"),
    db: Session = Depends(get_db)
):
    query = db.query(Product).filter(Product.is_active == True)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if search:
        query = query.filter(Product.name.contains(search))

    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product_endpoint(
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if user is a vendor or admin
    if current_user.role not in ["vendor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors or admins can create products"
        )

    return create_product(db, product, current_user.id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(
    product_id: int, 
    product_update: ProductUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if product exists
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Check if user is the vendor of this product or an admin
    if current_user.role != "admin" and db_product.vendor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own products"
        )

    return update_product(db, product_id, product_update)

@router.delete("/{product_id}")
def delete_product_endpoint(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    # Check if product exists
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Check if user is the vendor of this product or an admin
    if current_user.role != "admin" and db_product.vendor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own products"
        )

    delete_product(db, product_id)
    return {"message": "Product deleted successfully"}

@router.get("/categories/", response_model=List[CategoryResponse])
def read_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    categories = get_categories(db, skip, limit)
    return categories

@router.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category