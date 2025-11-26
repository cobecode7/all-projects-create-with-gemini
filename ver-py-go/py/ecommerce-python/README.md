# متجر إلكتروني API

هذا متجر إلكتروني متكامل تم بناؤه باستخدام FastAPI.

## المميزات

- مصادقة المستخدمين (التسجيل وتسجيل الدخول)
- إدارة المنتجات
- إدارة الطلبات
- إدارة الفئات
- تقييمات المنتجات
- أدوار المستخدمين (مدير، بائع، عميل)
- معالجة الدفع
- تتبع المخزون

## البدء

1. استنساخ المستودع:

```bash
git clone https://github.com/your-username/ecommerce-python.git
cd ecommerce-python
```

2. إنشاء بيئة افتراضية وتثبيت الاعتماديات:

```bash
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scriptsctivate
pip install -r requirements.txt
```

3. إعداد متغيرات البيئة:

```bash
cp .env.example .env
# قم بتعديل ملف .env حسب الحاجة
```

4. تهيئة قاعدة البيانات:

```bash
python -m app.utils.init_db
```

5. تشغيل التطبيق:

```bash
uvicorn app.main:app --reload
```

سيكون API متاحًا على `http://localhost:8000`.

## واجهة المستخدم التفاعلية

يمكنك الوصول إلى واجهة المستخدم التفاعلية لـ Swagger على `http://localhost:8000/docs` أو ReDoc على `http://localhost:8000/redoc`.

## Docker

لتشغيل التطبيق باستخدام Docker، استخدم الأمر التالي:

```bash
docker-compose up -d
```

## هيكل المشروع

```
ecommerce-python/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── products.py
│   │       └── orders.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   └── utils/
│       ├── __init__.py
│       ├── database.py
│       └── init_db.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

## نقاط النهاية الرئيسية

- `/api/auth/register` - تسجيل مستخدم جديد
- `/api/auth/login` - تسجيل الدخول
- `/api/auth/refresh` - تجديد رمز المصادقة
- `/api/users/` - إدارة المستخدمين
- `/api/products/` - إدارة المنتجات
- `/api/orders/` - إدارة الطلبات

## المساهمون

- [اسمك](https://github.com/your-username)

## الترخيص

هذا المشروع مرخص تحت ترخيص MIT. راجع ملف LICENSE لمزيد من التفاصيل.