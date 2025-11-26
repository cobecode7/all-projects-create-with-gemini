# 🛍️ برومبت متجر إلكتروني متكامل - Ecommerce Platform

## 🎯 نظرة عامة
مطلوب إنشاء متجر إلكتروني متكامل باستخدام أحدث التقنيات، جاهز للنشر والبيع فوراً مع التركيز على:
- **الأداء العالي** والكفاءة
- **تجربة مستخدم** استثنائية
- **أمان** متكامل
- **قابلية التوسع** والصيانة

## 🛠 المكدس التقني

### Backend (اختر واحد)
**الخيار 1 - Django:**
```python
Django 5.0+ | Django REST Framework | Djangorestframework-simplejwt
Django-CORS-headers | Django-storages | Django-filter

الخيار 2 - FastAPI:
python

FastAPI 0.100+ | SQLAlchemy 2.0+ | Alembic | Pydantic V2
Uvicorn | Gunicorn | Python-multipart

الأدوات المشتركة:
python

uv | ruff | pytest | python-decouple | celery | redis
postgresql | pydantic | pytest | mypy

Frontend:
javascript

Next.js 14+ (App Router) | React 18+ | TypeScript 5+ 
Tailwind CSS 3+ | shadcn/ui | Zustand | TanStack Query
React Hook Form | Zod | Framer Motion

البنية التحتية:
yaml

Docker | Docker Compose | PostgreSQL | Redis
Nginx | GitHub Actions | AWS S3 | CloudFront

📋 المتطلبات الوظيفية
🏪 نظام المنتجات

    عرض المنتجات مع التصنيفات والعلامات

    بحث وتصفية متقدم

    إدارة المخزون

    تقييمات ومراجعات العملاء

    نظام الخصومات والعروض

👥 نظام المستخدمين

    تسجيل الدخول/التسجيل (Email + OAuth)

    إدارة الملفات الشخصية

    نظام الصلاحيات (Admin, Vendor, Customer)

    إعادة تعيين كلمة المرور

🛒 نظام الطلبات

    سلة التسوق

    عملية دفع متعددة البوابات

    تتبع الطلبات

    إشعارات البريد الإلكتروني

    إدارة الشحن والتوصيل

📊 لوحة التحكم

    إحصائيات وتحليلات المبيعات

    إدارة العملاء والطلبات

    تقارير الأداء

    إدارة المحتوى

🏗 هيكل المشروع
text

ecommerce-platform/
├── backend/
│   ├── apps/
│   │   ├── users/         # إدارة المستخدمين
│   │   ├── products/      # المنتجات والفئات
│   │   ├── orders/        # الطلبات والمبيعات
│   │   ├── payments/      # أنظمة الدفع
│   │   └── analytics/     # التحليلات والتقارير
│   ├── core/              # الإعدادات الأساسية
│   ├── utils/             # الأدوات المساعدة
│   └── tests/             # الاختبارات
├── frontend/
│   ├── app/               # Next.js App Router
│   │   ├── (auth)/        # صفحات المصادقة
│   │   ├── (dashboard)/   # لوحة التحكم
│   │   ├── products/      # صفحات المنتجات
│   │   └── api/           # API Routes
│   ├── components/        # مكونات قابلة لإعادة الاستخدام
│   ├── lib/               # التكوينات والأدوات
│   ├── stores/            # إدارة الحالة (Zustand)
│   └── types/             # تعريفات TypeScript
├── infrastructure/
│   ├── docker/            # ملفات Docker
│   ├── nginx/             # إعدادات Nginx
│   └── ci-cd/             # سيرفرات CI/CD
└── docs/                  # التوثيق

⚙️ إعدادات الجودة
Backend Configuration (pyproject.toml):
toml

[tool.ruff]
select = ["E", "F", "W", "I", "N", "UP", "YTT", "S", "BLE", "FBT", "B", "A", "COM", "C4", "DTZ", "T10", "EM", "EXE", "ISC", "ICN", "G", "INP", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SLF", "SIM", "TID", "TCH", "INT", "ARG", "PTH", "PL", "TRY", "FLY", "NPY", "AIR", "PERF", "FIX", "RUF"]
ignore = ["ANN101", "ANN102", "S101", "D100", "D104"]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101", "INP001"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

Frontend Configuration (tailwind.config.js):
javascript

module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}

🔒 إعدادات الأمان
إعدادات Django:
python

# settings.py
CORS_ALLOWED_ORIGINS = []  # تحديد النطاقات المسموحة
CSRF_TRUSTED_ORIGINS = []   # لنطاقات الإنتاج
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# إعدادات JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

إعدادات FastAPI:
python

# security.py
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# CORS settings
origins = [
    "http://localhost:3000",
    "https://yourdomain.com",
]

🚀 خطوات التنفيذ
المرحلة 1: الإعداد الأساسي ✅

    تهيئة المشروع باستخدام uv

    تكوين Docker للبيئة التنموية

    إعداد PostgreSQL وRedis

    تكوين Ruff وPytest للجودة

المرحلة 2: النماذج الأساسية ✅

    نماذج المستخدمين والصلاحيات

    نماذج المنتجات والفئات

    نماذج الطلبات والمبيعات

    نماذج الدفع والشحن

المرحلة 3: واجهات برمجة التطبيقات ✅

    واجهات المستخدمين والمصادقة

    واجهات إدارة المنتجات

    واجهات الطلبات والمبيعات

    واجهات الدفع والإشعارات

المرحلة 4: الواجهة الأمامية ✅

    إعداد Next.js مع TypeScript

    تكوين Tailwind CSS وshadcn/ui

    صفحات المنتجات والتصنيفات

    سلة التسويل وعملية الشراء

المرحلة 5: التكامل والاختبار ✅

    تكامل واجهات برمجة التطبيقات

    اختبارات شاملة (Unit, Integration, E2E)

    تحسين الأداء والتحميل

    إعداد CI/CD

📊 مقاييس الأداء المستهدفة

    وقت تحميل الصفحة: < 2 ثانية

    Lighthouse Score: > 90

    Coverage: > 90%

    TypeScript: لا أخطاء

    Security: فحوصات أمان سليمة

🔧 أوامر التشغيل
bash

# Backend Development
uv sync
uv run python manage.py runserver  # Django
uv run uvicorn app.main:app --reload  # FastAPI

# Frontend Development
npm install
npm run dev
npm run build

# Testing & Quality
uv run pytest
npm run test
uv run ruff check .
uv run ruff format .
npm run lint
npm run type-check

# Production
docker-compose up -d
docker-compose exec backend uv run python manage.py migrate

🎯 المخرجات النهائية المتوقعة
📁 ملفات المشروع

    مشروع كامل جاهز للتشغيل

    توثيق شامل للكود

    إعدادات Docker للتطوير والإنتاج

    سكريبتات النشر والتوزيع

    إعدادات CI/CD جاهزة

📚 التوثيق

    دليل الإعداد والتنصيب

    دليل المستخدم والإدارة

    دليل المطورين والمساهمين


