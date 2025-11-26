from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# إضافة echo=True لعرض استعلامات SQL في الطرفية (مفيد للتصحيح)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    تهيئة قاعدة البيانات بإنشاء جميع الجداول
    """
    from app.models import user, product, order
    Base.metadata.create_all(bind=engine)