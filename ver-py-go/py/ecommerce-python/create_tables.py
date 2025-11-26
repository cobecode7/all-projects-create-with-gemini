
from app.core.database import engine, Base
from app.models import user, product, order

try:
    print("بدء إنشاء الجداول...")
    Base.metadata.create_all(bind=engine)
    print("تم إنشاء الجداول بنجاح!")

    # التحقق من الجداول بعد الإنشاء
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print("الجداول الموجودة في قاعدة البيانات:")
        for table in tables:
            print(f"- {table}")
except Exception as e:
    print(f"حدث خطأ: {e}")
