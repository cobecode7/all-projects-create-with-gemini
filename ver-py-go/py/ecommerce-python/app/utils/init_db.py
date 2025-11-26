
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db as create_tables
from app.models.user import User, UserRole
from app.models.product import Product, Category
from app.core.security import get_password_hash

def init_db():
    """
    تهيئة قاعدة البيانات مع بعض البيانات النموذجية
    """
    # إنشاء الجداول أولاً
    create_tables()

    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                email="admin@example.com",
                password_hash=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("تم إنشاء المستخدم المدير")

        # Check if vendor user already exists
        vendor_user = db.query(User).filter(User.email == "vendor@example.com").first()
        if not vendor_user:
            # Create vendor user
            vendor_user = User(
                email="vendor@example.com",
                password_hash=get_password_hash("vendor123"),
                first_name="Vendor",
                last_name="User",
                role=UserRole.VENDOR,
                is_active=True
            )
            db.add(vendor_user)
            db.commit()
            db.refresh(vendor_user)
            print("تم إنشاء المستخدم البائع")

        # Check if customer user already exists
        customer_user = db.query(User).filter(User.email == "customer@example.com").first()
        if not customer_user:
            # Create customer user
            customer_user = User(
                email="customer@example.com",
                password_hash=get_password_hash("customer123"),
                first_name="Customer",
                last_name="User",
                role=UserRole.CUSTOMER,
                is_active=True
            )
            db.add(customer_user)
            db.commit()
            db.refresh(customer_user)
            print("تم إنشاء المستخدم العميل")

        # Check if categories already exist
        electronics_category = db.query(Category).filter(Category.name == "Electronics").first()
        if not electronics_category:
            # Create electronics category
            electronics_category = Category(
                name="Electronics",
                description="Electronic devices and accessories"
            )
            db.add(electronics_category)
            db.commit()
            db.refresh(electronics_category)
            print("تم إنشاء فئة الإلكترونيات")

        clothing_category = db.query(Category).filter(Category.name == "Clothing").first()
        if not clothing_category:
            # Create clothing category
            clothing_category = Category(
                name="Clothing",
                description="Apparel and accessories"
            )
            db.add(clothing_category)
            db.commit()
            db.refresh(clothing_category)
            print("تم إنشاء فئة الملابس")

        # Check if products already exist
        laptop_product = db.query(Product).filter(Product.name == "Laptop").first()
        if not laptop_product:
            # Create laptop product
            laptop_product = Product(
                name="Laptop",
                description="High-performance laptop with 16GB RAM and 512GB SSD",
                price=999.99,
                sku="LAPTOP-001",
                track_quantity=True,
                quantity=10,
                vendor_id=vendor_user.id,
                category_id=electronics_category.id
            )
            db.add(laptop_product)
            db.commit()
            db.refresh(laptop_product)
            print("تم إنشاء منتج الكمبيوتر المحمول")

        tshirt_product = db.query(Product).filter(Product.name == "T-Shirt").first()
        if not tshirt_product:
            # Create t-shirt product
            tshirt_product = Product(
                name="T-Shirt",
                description="Cotton t-shirt in various colors and sizes",
                price=19.99,
                sku="TSHIRT-001",
                track_quantity=True,
                quantity=50,
                vendor_id=vendor_user.id,
                category_id=clothing_category.id
            )
            db.add(tshirt_product)
            db.commit()
            db.refresh(tshirt_product)
            print("تم إنشاء منتج القميص")

        print("تم تهيئة قاعدة البيانات بنجاح")
    except Exception as e:
        print(f"خطأ في تهيئة قاعدة البيانات: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
