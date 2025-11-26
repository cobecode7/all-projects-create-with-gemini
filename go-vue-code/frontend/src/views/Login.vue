<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6 col-lg-5 col-xl-4">
          <div class="login-container">
            <div class="text-center mb-4">
              <div class="login-logo mx-auto mb-3">
                <i class="bi bi-shield-lock"></i>
              </div>
              <h2 class="login-title">تسجيل الدخول</h2>
              <p class="login-subtitle">أهلاً بعودتك! يرجى إدخال بياناتك</p>
            </div>

            <div class="login-card">
              <div v-if="error" class="alert alert-danger d-flex align-items-center" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                {{ error }}
              </div>

              <form @submit.prevent="handleLogin" class="login-form">
                <div class="mb-3">
                  <label for="email" class="form-label">البريد الإلكتروني</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                    <input
                      type="email"
                      class="form-control"
                      id="email"
                      v-model="form.email"
                      placeholder="example@email.com"
                      required
                    >
                  </div>
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">كلمة المرور</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-lock"></i></span>
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      id="password"
                      v-model="form.password"
                      placeholder="••••••••"
                      required
                    >
                    <button class="btn btn-outline-secondary" type="button" @click="togglePasswordVisibility">
                      <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                  </div>
                </div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                  <div class="form-check">
                    <input type="checkbox" class="form-check-input" id="remember" v-model="form.remember">
                    <label class="form-check-label" for="remember">تذكرني</label>
                  </div>
                  <a href="#" class="forgot-password-link">نسيت كلمة المرور؟</a>
                </div>
                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary btn-login"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    تسجيل الدخول
                  </button>
                </div>
              </form>

              <div class="login-footer text-center mt-4">
                <p>ليس لديك حساب؟ <router-link to="/register" class="register-link">إنشاء حساب جديد</router-link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  remember: false
})

const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await authStore.login(form)

    // Redirect to the intended page or dashboard
    const redirectPath = route.query.redirect || '/dashboard'
    router.push(redirectPath)
  } catch (err) {
    error.value = err.response?.data?.error || 'فشل تسجيل الدخول. يرجى التحقق من بياناتك والمحاولة مرة أخرى.'
  } finally {
    loading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
  const passwordInput = document.getElementById('password')
  if (passwordInput) {
    passwordInput.type = showPassword.value ? 'text' : 'password'
  }
}
</script>

<style scoped>
/* Login Page Layout */
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
  padding: 1.5rem;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-lg);
  padding: 2.5rem;
  border: none;
}

/* Login Header */
.login-logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: var(--primary-color);
}

.login-title {
  font-weight: var(--font-weight-bold);
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: var(--text-muted);
  margin-bottom: 0;
}

/* Form Styles */
.login-form .form-label {
  font-weight: var(--font-weight-medium);
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.login-form .input-group {
  border-radius: var(--border-radius);
  overflow: hidden;
}

.login-form .input-group-text {
  background-color: var(--light-color);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
}

.login-form .form-control {
  border: 1px solid var(--border-color);
  padding: 0.75rem 1rem;
  transition: var(--transition-fast);
}

.login-form .form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.25rem rgba(67, 97, 238, 0.25);
}

.login-form .btn-outline-secondary {
  border-color: var(--border-color);
  color: var(--text-muted);
}

.login-form .btn-outline-secondary:hover {
  background-color: var(--light-color);
  color: var(--text-color);
}

.forgot-password-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 0.9rem;
  transition: var(--transition-fast);
}

.forgot-password-link:hover {
  text-decoration: underline;
}

/* Login Button */
.btn-login {
  padding: 0.75rem 1rem;
  font-weight: var(--font-weight-medium);
  background-color: var(--primary-color);
  border: none;
  border-radius: var(--border-radius);
  transition: var(--transition-fast);
}

.btn-login:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(67, 97, 238, 0.2);
}

.btn-login:disabled {
  background-color: var(--primary-color);
  opacity: 0.7;
  transform: none;
  box-shadow: none;
}

/* Login Footer */
.login-footer p {
  color: var(--text-muted);
  margin-bottom: 0;
}

.register-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: var(--transition-fast);
}

.register-link:hover {
  text-decoration: underline;
}

/* Alert Styles */
.alert {
  border-radius: var(--border-radius);
  border: none;
  padding: 0.75rem 1rem;
}

.alert-danger {
  background-color: rgba(255, 0, 110, 0.1);
  color: var(--danger-color);
}

/* RTL Support */
[dir="rtl"] .login-form .input-group-text {
  border-left: none;
  border-right: 1px solid var(--border-color);
}

[dir="rtl"] .login-form .btn-outline-secondary {
  border-left: 1px solid var(--border-color);
  border-right: none;
}

[dir="rtl"] .forgot-password-link {
  margin-right: auto;
  margin-left: 0;
}

[dir="rtl"] .alert i {
  margin-right: 0;
  margin-left: 0.5rem;
}
</style>
