
from app.core.database import engine, SessionLocal
from app.core.config import settings
from sqlalchemy import text
import os

print(f"قاعدة البيانات المستخدمة: {settings.DATABASE_URL}")

# التحقق من متغيرات البيئة
print("متغيرات البيئة المتعلقة بقاعدة البيانات:")
print(f"POSTGRES_USER: {os.environ.get('POSTGRES_USER', 'غير محدد')}")
print(f"POSTGRES_PASSWORD: {'***' if os.environ.get('POSTGRES_PASSWORD') else 'غير محدد'}")
print(f"POSTGRES_DB: {os.environ.get('POSTGRES_DB', 'غير محدد')}")

# التحقق من الاتصال بقاعدة البيانات
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"اتصال ناجح بقاعدة البيانات PostgreSQL:")
        print(f"الإصدار: {version}")

        # التحقق من المخططات المتاحة
        result = conn.execute(text("SELECT schema_name FROM information_schema.schemata"))
        schemas = [row[0] for row in result]
        print(f"المخططات المتاحة: {schemas}")

        # التحقق من الجداول في المخطط العام
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print(f"الجداول في المخطط العام: {tables}")

except Exception as e:
    print(f"فشل الاتصال بقاعدة البيانات: {e}")
