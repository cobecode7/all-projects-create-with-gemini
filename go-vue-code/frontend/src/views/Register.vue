<template>
  <div class="register-page">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6 col-lg-5 col-xl-4">
          <div class="register-container">
            <div class="text-center mb-4">
              <div class="register-logo mx-auto mb-3">
                <i class="bi bi-person-plus"></i>
              </div>
              <h2 class="register-title">إنشاء حساب جديد</h2>
              <p class="register-subtitle">انضم إلينا اليوم! يرجى إدخال بياناتك</p>
            </div>

            <div class="register-card">
              <div v-if="error" class="alert alert-danger d-flex align-items-center" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                {{ error }}
              </div>

              <div v-if="successMessage" class="alert alert-success d-flex align-items-center" role="alert">
                <i class="bi bi-check-circle-fill me-2"></i>
                {{ successMessage }}
              </div>

              <form @submit.prevent="handleRegister" class="register-form">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="firstName" class="form-label">الاسم الأول</label>
                    <div class="input-group">
                      <span class="input-group-text"><i class="bi bi-person"></i></span>
                      <input
                        type="text"
                        class="form-control"
                        id="firstName"
                        v-model="form.firstName"
                        placeholder="محمد"
                        required
                      >
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="lastName" class="form-label">الاسم الأخير</label>
                    <div class="input-group">
                      <span class="input-group-text"><i class="bi bi-person"></i></span>
                      <input
                        type="text"
                        class="form-control"
                        id="lastName"
                        v-model="form.lastName"
                        placeholder="أحمد"
                        required
                      >
                    </div>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="username" class="form-label">اسم المستخدم</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-at"></i></span>
                    <input
                      type="text"
                      class="form-control"
                      id="username"
                      v-model="form.username"
                      placeholder="username"
                      required
                    >
                  </div>
                </div>

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
                  <div class="form-text text-muted mt-1">
                    يجب أن تكون كلمة المرور قوية تحتوي على 8 أحرف على الأقل
                  </div>
                </div>

                <div class="mb-3">
                  <label for="confirmPassword" class="form-label">تأكيد كلمة المرور</label>
                  <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
                    <input
                      :type="showConfirmPassword ? 'text' : 'password'"
                      class="form-control"
                      id="confirmPassword"
                      v-model="form.confirmPassword"
                      placeholder="••••••••"
                      :class="{ 'is-invalid': passwordMismatch }"
                      required
                    >
                    <button class="btn btn-outline-secondary" type="button" @click="toggleConfirmPasswordVisibility">
                      <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                  </div>
                  <div v-if="passwordMismatch" class="invalid-feedback d-block">
                    كلمات المرور غير متطابقة
                  </div>
                </div>

                <div class="mb-3 form-check">
                  <input type="checkbox" class="form-check-input" id="terms" v-model="form.agreeToTerms">
                  <label class="form-check-label" for="terms">
                    أوافق على <a href="#" class="terms-link">الشروط والأحكام</a>
                  </label>
                </div>

                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary btn-register"
                    :disabled="loading || passwordMismatch || !form.agreeToTerms"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    إنشاء حساب
                  </button>
                </div>
              </form>

              <div class="register-footer text-center mt-4">
                <p>لديك حساب بالفعل؟ <router-link to="/login" class="login-link">تسجيل الدخول</router-link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeToTerms: false
})

const loading = ref(false)
const error = ref('')
const successMessage = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const passwordMismatch = computed(() => {
  return form.password && form.confirmPassword && form.password !== form.confirmPassword
})

const handleRegister = async () => {
  if (passwordMismatch.value || !form.agreeToTerms) return

  loading.value = true
  error.value = ''
  successMessage.value = ''

  try {
    await authStore.register(form)
    successMessage.value = 'تم إنشاء حسابك بنجاح! يمكنك الآن تسجيل الدخول.'

    // Reset form
    Object.keys(form).forEach(key => {
      if (key !== 'agreeToTerms') {
        form[key] = ''
      }
    })

    // Redirect to login after a short delay
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.error || 'فشل إنشاء الحساب. يرجى المحاولة مرة أخرى.'
  } finally {
    loading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value
}
</script>

<style scoped>
/* Register Page Layout */
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--info-color) 0%, var(--primary-color) 100%);
  padding: 1.5rem;
}

.register-container {
  width: 100%;
  max-width: 500px;
}

.register-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-lg);
  padding: 2.5rem;
  border: none;
}

/* Register Header */
.register-logo {
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

.register-title {
  font-weight: var(--font-weight-bold);
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.register-subtitle {
  color: var(--text-muted);
  margin-bottom: 0;
}

/* Form Styles */
.register-form .form-label {
  font-weight: var(--font-weight-medium);
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.register-form .input-group {
  border-radius: var(--border-radius);
  overflow: hidden;
}

.register-form .input-group-text {
  background-color: var(--light-color);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
}

.register-form .form-control {
  border: 1px solid var(--border-color);
  padding: 0.75rem 1rem;
  transition: var(--transition-fast);
}

.register-form .form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.25rem rgba(67, 97, 238, 0.25);
}

.register-form .btn-outline-secondary {
  border-color: var(--border-color);
  color: var(--text-muted);
}

.register-form .btn-outline-secondary:hover {
  background-color: var(--light-color);
  color: var(--text-color);
}

.terms-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
}

.terms-link:hover {
  text-decoration: underline;
}

/* Register Button */
.btn-register {
  padding: 0.75rem 1rem;
  font-weight: var(--font-weight-medium);
  background-color: var(--primary-color);
  border: none;
  border-radius: var(--border-radius);
  transition: var(--transition-fast);
}

.btn-register:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(67, 97, 238, 0.2);
}

.btn-register:disabled {
  background-color: var(--primary-color);
  opacity: 0.7;
  transform: none;
  box-shadow: none;
}

/* Register Footer */
.register-footer p {
  color: var(--text-muted);
  margin-bottom: 0;
}

.login-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: var(--font-weight-medium);
  transition: var(--transition-fast);
}

.login-link:hover {
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

.alert-success {
  background-color: rgba(6, 255, 165, 0.1);
  color: var(--success-color);
}

/* RTL Support */
[dir="rtl"] .register-form .input-group-text {
  border-left: none;
  border-right: 1px solid var(--border-color);
}

[dir="rtl"] .register-form .btn-outline-secondary {
  border-left: 1px solid var(--border-color);
  border-right: none;
}

[dir="rtl"] .alert i {
  margin-right: 0;
  margin-left: 0.5rem;
}
</style>
