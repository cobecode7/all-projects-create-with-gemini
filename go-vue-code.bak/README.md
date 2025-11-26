# نظام Go Vue Auth

نظام مصادقة متكامل مبني باستخدام Go/Gin للواجهة الخلفية و Vue.js 3 للواجهة الأمامية مع SQLite كقاعدة بيانات.

## المميزات

- تسجيل المستخدمين الجدد
- تسجيل الدخول والخروج الآمن
- إدارة الأدوار والصلاحيات
- حماية المسارات المطلوبة للمصادقة
- واجهة مستخدم حديثة وسهلة الاستخدام

## التقنيات المستخدمة

### الواجهة الخلفية
- Go/Gin Framework
- SQLite
- GORM
- JWT للمصادقة

### الواجهة الأمامية
- Vue.js 3
- Pinia لإدارة الحالة
- Vue Router للتوجيه
- Bootstrap 5 للتصميم
- Axios للتعامل مع الطلبات

## المتطلبات

- Go 1.21 أو أحدث
- Node.js 16 أو أحدث

## التثبيت والتشغيل

### 1. إعداد قاعدة البيانات

سيتم إنشاء قاعدة بيانات SQLite تلقائيًا باسم `app.db` في المجلد الرئيسي للمشروع عند تشغيل التطبيق لأول مرة.

### 2. تشغيل الواجهة الخلفية

```bash
# الانتقال إلى مجلد المشروع
cd /path/to/go-vue-code

# تثبيت الاعتماديات
go mod download

# نسخ ملف المتغيرات البيئية وتعديله حسب الحاجة
cp .env.example .env

# تشغيل الخادم
go run main.go
```

### 3. تشغيل الواجهة الأمامية

```bash
# الانتقال إلى مجلد الواجهة الأمامية
cd frontend

# تثبيت الاعتماديات
npm install

# تشغيل خادم التطوير
npm run dev
```

## حساب المدير الافتراضي

عند تشغيل التطبيق لأول مرة، سيتم إنشاء حساب مدير افتراضي:

- البريد الإلكتروني: admin@example.com
- كلمة المرور: admin123

## هيكل المشروع

```
go-vue-code/
├── main.go                 # نقطة دخول التطبيق
├── go.mod                  # ملف وحدات Go
├── .env                    # متغيرات البيئة
├── config/
│   └── database.go         # إعداد قاعدة البيانات
├── controllers/
│   └── auth_controller.go  # وحدات تحكم المصادقة
├── middleware/
│   └── auth.go             # برمجيات المصادقة الوسيطة
├── models/
│   └── user.go             # نماذج البيانات
├── routes/
│   └── routes.go           # تعريف المسارات
└── frontend/
    ├── package.json        # ملف مشروع Node.js
    ├── vite.config.js      # إعدادات Vite
    ├── index.html          # ملف HTML الرئيسي
    ├── src/
    │   ├── main.js         # نقطة دخول Vue.js
    │   ├── App.vue         # المكون الرئيسي
    │   ├── router/
    │   │   └── index.js    # إعدادات التوجيه
    │   ├── stores/
    │   │   └── auth.js     # متجر المصادقة
    │   └── views/
    │       ├── Home.vue    # الصفحة الرئيسية
    │       ├── Login.vue   # صفحة تسجيل الدخول
    │       ├── Register.vue # صفحة التسجيل
    │       ├── Dashboard.vue # لوحة التحكم
    │       └── Profile.vue # صفحة الملف الشخصي
    └── public/             # ملفات عامة
```

## المساهمة

1. Fork المشروع
2. إنشاء فرع جديد (`git checkout -b feature/AmazingFeature`)
3. حفظ التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. دفع التغييرات (`git push origin feature/AmazingFeature`)
5. فتح طلب سحب (Pull Request)

## الترخيص

هذا المشروع مرخص تحت ترخيص MIT.
