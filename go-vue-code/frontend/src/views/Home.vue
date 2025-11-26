<template>
  <div class="hero-section">
    <div class="container">
      <div class="row align-items-center min-vh-100">
        <div class="col-lg-6">
          <div class="hero-content">
            <h1 class="display-4 fw-bold mb-4">مرحباً بك في نظام Go Vue Auth</h1>
            <p class="lead mb-4">
              نظام مصادقة متكامل مبني باستخدام Go/Gin للواجهة الخلفية و Vue.js 3 للواجهة الأمامية.
              يوفر النظام تسجيل المستخدمين، تسجيل الدخول، إدارة الأدوار والصلاحيات.
            </p>
            <div class="d-flex gap-3 flex-wrap">
              <router-link v-if="!isAuthenticated" to="/register" class="btn btn-primary btn-lg px-4">
                <i class="bi bi-person-plus ms-2"></i>
                إنشاء حساب جديد
              </router-link>
              <router-link v-if="!isAuthenticated" to="/login" class="btn btn-outline-primary btn-lg px-4">
                <i class="bi bi-box-arrow-in-right ms-2"></i>
                تسجيل الدخول
              </router-link>
              <router-link v-if="isAuthenticated" to="/dashboard" class="btn btn-primary btn-lg px-4">
                <i class="bi bi-speedometer2 ms-2"></i>
                لوحة التحكم
              </router-link>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="hero-image text-center">
            <div class="floating-card">
              <div class="card shadow-lg border-0">
                <div class="card-body p-4">
                  <div class="d-flex align-items-center mb-3">
                    <div class="avatar bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
                      <i class="bi bi-shield-lock fs-4"></i>
                    </div>
                    <div>
                      <h6 class="mb-0 fw-bold">نظام آمن</h6>
                      <small class="text-muted">حماية عالية للبيانات</small>
                    </div>
                  </div>
                  <div class="d-flex align-items-center mb-3">
                    <div class="avatar bg-success text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
                      <i class="bi bi-people fs-4"></i>
                    </div>
                    <div>
                      <h6 class="mb-0 fw-bold">إدارة المستخدمين</h6>
                      <small class="text-muted">تحكم كامل بالصلاحيات</small>
                    </div>
                  </div>
                  <div class="d-flex align-items-center">
                    <div class="avatar bg-info text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 50px; height: 50px;">
                      <i class="bi bi-lightning fs-4"></i>
                    </div>
                    <div>
                      <h6 class="mb-0 fw-bold">أداء عالي</h6>
                      <small class="text-muted">سرعة استجابة فائقة</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <section class="features-section py-5 bg-light">
    <div class="container py-5">
      <div class="row justify-content-center text-center mb-5">
        <div class="col-lg-8">
          <h2 class="fw-bold mb-3">مميزات النظام</h2>
          <p class="lead text-muted">نظام مصادقة متكامل يوفر جميع المميزات التي تحتاجها لإدارة المستخدمين والصلاحيات</p>
        </div>
      </div>
      <div class="row g-4">
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm border-0 feature-card">
            <div class="card-body p-4 text-center">
              <div class="feature-icon bg-primary bg-opacity-10 text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                <i class="bi bi-person-plus fs-2"></i>
              </div>
              <h5 class="card-title fw-bold">تسجيل المستخدمين</h5>
              <p class="card-text text-muted">تسجيل سهل للمستخدمين الجدد مع تأكيد البريد الإلكتروني</p>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm border-0 feature-card">
            <div class="card-body p-4 text-center">
              <div class="feature-icon bg-success bg-opacity-10 text-success rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                <i class="bi bi-shield-check fs-2"></i>
              </div>
              <h5 class="card-title fw-bold">مصادقة آمنة</h5>
              <p class="card-text text-muted">تسجيل الدخول والخروج الآمن باستخدام تقنيات التشفير الحديثة</p>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm border-0 feature-card">
            <div class="card-body p-4 text-center">
              <div class="feature-icon bg-info bg-opacity-10 text-info rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                <i class="bi bi-person-badge fs-2"></i>
              </div>
              <h5 class="card-title fw-bold">الأدوار والصلاحيات</h5>
              <p class="card-text text-muted">إدارة كاملة للأدور والصلاحيات للتحكم في وصول المستخدمين</p>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm border-0 feature-card">
            <div class="card-body p-4 text-center">
              <div class="feature-icon bg-warning bg-opacity-10 text-warning rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                <i class="bi bi-shield-lock fs-2"></i>
              </div>
              <h5 class="card-title fw-bold">حماية المسارات</h5>
              <p class="card-text text-muted">حماية المسارات المطلوبة للمصادقة ومنع الوصول غير المصرح به</p>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm border-0 feature-card">
            <div class="card-body p-4 text-center">
              <div class="feature-icon bg-danger bg-opacity-10 text-danger rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                <i class="bi bi-palette fs-2"></i>
              </div>
              <h5 class="card-title fw-bold">واجهة حديثة</h5>
              <p class="card-text text-muted">واجهة مستخدم حديثة وسهلة الاستخدام مع تصميم متجاوب</p>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-lg-4">
          <div class="card h-100 shadow-sm border-0 feature-card">
            <div class="card-body p-4 text-center">
              <div class="feature-icon bg-secondary bg-opacity-10 text-secondary rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 70px; height: 70px;">
                <i class="bi bi-graph-up fs-2"></i>
              </div>
              <h5 class="card-title fw-bold">تقارير وإحصائيات</h5>
              <p class="card-text text-muted">تقارير مفصلة وإحصائيات حول نشاط المستخدمين والنظام</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="tech-section py-5">
    <div class="container py-5">
      <div class="row justify-content-center text-center mb-5">
        <div class="col-lg-8">
          <h2 class="fw-bold mb-3">التقنيات المستخدمة</h2>
          <p class="lead text-muted">تم بناء النظام باستخدام أحدث التقنيات والأدوات لضمان الأداء العالي والموثوقية</p>
        </div>
      </div>
      <div class="row g-4 align-items-center">
        <div class="col-md-6 order-md-2">
          <div class="tech-image text-center">
            <div class="tech-stack">
              <div class="d-flex flex-wrap justify-content-center gap-3">
                <div class="tech-item">
                  <div class="card shadow-sm border-0">
                    <div class="card-body p-3 text-center">
                      <div class="tech-icon bg-primary bg-opacity-10 text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-2" style="width: 60px; height: 60px;">
                        <i class="bi bi-code-slash fs-3"></i>
                      </div>
                      <h6 class="mb-0 fw-bold">Go</h6>
                    </div>
                  </div>
                </div>
                <div class="tech-item">
                  <div class="card shadow-sm border-0">
                    <div class="card-body p-3 text-center">
                      <div class="tech-icon bg-success bg-opacity-10 text-success rounded-circle d-inline-flex align-items-center justify-content-center mb-2" style="width: 60px; height: 60px;">
                        <i class="bi bi-database fs-3"></i>
                      </div>
                      <h6 class="mb-0 fw-bold">PostgreSQL</h6>
                    </div>
                  </div>
                </div>
                <div class="tech-item">
                  <div class="card shadow-sm border-0">
                    <div class="card-body p-3 text-center">
                      <div class="tech-icon bg-info bg-opacity-10 text-info rounded-circle d-inline-flex align-items-center justify-content-center mb-2" style="width: 60px; height: 60px;">
                        <i class="bi bi-layers fs-3"></i>
                      </div>
                      <h6 class="mb-0 fw-bold">GORM</h6>
                    </div>
                  </div>
                </div>
                <div class="tech-item">
                  <div class="card shadow-sm border-0">
                    <div class="card-body p-3 text-center">
                      <div class="tech-icon bg-warning bg-opacity-10 text-warning rounded-circle d-inline-flex align-items-center justify-content-center mb-2" style="width: 60px; height: 60px;">
                        <i class="bi bi-filetype-js fs-3"></i>
                      </div>
                      <h6 class="mb-0 fw-bold">Vue.js 3</h6>
                    </div>
                  </div>
                </div>
                <div class="tech-item">
                  <div class="card shadow-sm border-0">
                    <div class="card-body p-3 text-center">
                      <div class="tech-icon bg-danger bg-opacity-10 text-danger rounded-circle d-inline-flex align-items-center justify-content-center mb-2" style="width: 60px; height: 60px;">
                        <i class="bi bi-key fs-3"></i>
                      </div>
                      <h6 class="mb-0 fw-bold">JWT</h6>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 order-md-1">
          <div class="tech-content">
            <div class="accordion" id="techAccordion">
              <div class="accordion-item border-0 shadow-sm mb-3">
                <h2 class="accordion-header">
                  <button class="accordion-button fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne">
                    Go/Gin Framework للواجهة الخلفية
                  </button>
                </h2>
                <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#techAccordion">
                  <div class="accordion-body">
                    إطار عمل Go/Gin يوفر أداءً عالياً وموثوقية للواجهة الخلفية، مع معالجة سريعة للطلبات وقدرة على التعامل مع آلاف الاتصالات المتزامنة.
                  </div>
                </div>
              </div>
              <div class="accordion-item border-0 shadow-sm mb-3">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo">
                    PostgreSQL كقاعدة بيانات
                  </button>
                </h2>
                <div id="collapseTwo" class="accordion-collapse collapse" data-bs-parent="#techAccordion">
                  <div class="accordion-body">
                    قاعدة بيانات PostgreSQL قوية وموثوقة تدعم المعاملات المعقدة وتوفر أداءً عالياً مع ضمان سلامة البيانات وأمانها.
                  </div>
                </div>
              </div>
              <div class="accordion-item border-0 shadow-sm mb-3">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree">
                    GORM للتعامل مع قاعدة البيانات
                  </button>
                </h2>
                <div id="collapseThree" class="accordion-collapse collapse" data-bs-parent="#techAccordion">
                  <div class="accordion-body">
                    مكتبة GORM تتيح التعامل السهل مع قاعدة البيانات من خلال ORM (Object-Relational Mapping)، مما يسهل كتابة الاستعلامات وتعديل البيانات.
                  </div>
                </div>
              </div>
              <div class="accordion-item border-0 shadow-sm mb-3">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFour">
                    Vue.js 3 للواجهة الأمامية
                  </button>
                </h2>
                <div id="collapseFour" class="accordion-collapse collapse" data-bs-parent="#techAccordion">
                  <div class="accordion-body">
                    إطار عمل Vue.js 3 يوفر بنية قابلة للتطوير وأداءً عالياً مع نظام تفاعلي يجعل تطوير الواجهات الأمامية سهلاً وممتعاً.
                  </div>
                </div>
              </div>
              <div class="accordion-item border-0 shadow-sm">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#collapseFive">
                    JWT للمصادقة
                  </button>
                </h2>
                <div id="collapseFive" class="accordion-collapse collapse" data-bs-parent="#techAccordion">
                  <div class="accordion-body">
                    تقنية JSON Web Tokens (JWT) توفر طريقة آمنة وفعالة للمصادقة والتحقق من هوية المستخدمين بدون الحاجة لتخزين معلومات الجلسة على الخادم.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<style scoped>
/* Hero Section Styles */
.hero-section {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="0.1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,133.3C672,139,768,181,864,181.3C960,181,1056,139,1152,122.7C1248,107,1344,117,1392,122.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') no-repeat bottom;
  background-size: cover;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.floating-card {
  animation: float 6s ease-in-out infinite;
  max-width: 400px;
  margin: 0 auto;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
}

/* Features Section Styles */
.features-section {
  background-color: var(--light-color);
}

.feature-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

/* Tech Section Styles */
.tech-item {
  transition: transform 0.3s ease;
}

.tech-item:hover {
  transform: translateY(-5px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-section {
    padding-top: 2rem;
    padding-bottom: 4rem;
  }
  
  .hero-content h1 {
    font-size: 2rem;
  }
}

/* RTL Support */
[dir="rtl"] .ms-2 {
  margin-right: 0;
  margin-left: 0.5rem;
}

[dir="rtl"] .me-3 {
  margin-left: 0;
  margin-right: 1rem;
}
</style>
