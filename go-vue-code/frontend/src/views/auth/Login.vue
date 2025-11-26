<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <i class="fas fa-code"></i>
          <h2>Go-Vue Code</h2>
        </div>
        <p class="login-subtitle">تسجيل الدخول إلى حسابك</p>
      </div>

      <form @submit.prevent="login" class="login-form">
        <div class="mb-3">
          <label for="email" class="form-label">البريد الإلكتروني</label>
          <div class="input-group">
            <span class="input-group-text">
              <i class="fas fa-envelope"></i>
            </span>
            <input type="email" class="form-control" id="email" v-model="credentials.email" required>
          </div>
          <div class="invalid-feedback" v-if="errors.email">
            {{ errors.email[0] }}
          </div>
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">كلمة المرور</label>
          <div class="input-group">
            <span class="input-group-text">
              <i class="fas fa-lock"></i>
            </span>
            <input :type="showPassword ? 'text' : 'password'" class="form-control" id="password" v-model="credentials.password" required>
            <button class="btn btn-outline-secondary" type="button" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <div class="invalid-feedback" v-if="errors.password">
            {{ errors.password[0] }}
          </div>
        </div>

        <div class="mb-3 form-check">
          <input type="checkbox" class="form-check-input" id="remember" v-model="credentials.remember">
          <label class="form-check-label" for="remember">تذكرني</label>
        </div>

        <div class="d-grid gap-2 mb-3">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
              <span class="visually-hidden">جاري التحميل...</span>
            </div>
            تسجيل الدخول
          </button>
        </div>

        <div class="text-center">
          <router-link to="/forgot-password" class="forgot-password-link">نسيت كلمة المرور؟</router-link>
        </div>
      </form>

      <div class="login-footer">
        <p>ليس لديك حساب؟ <router-link to="/register">إنشاء حساب جديد</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();

    const credentials = ref({
      email: '',
      password: '',
      remember: false
    });

    const showPassword = ref(false);
    const loading = ref(false);
    const errors = ref({});

    const login = async () => {
      loading.value = true;
      errors.value = {};

      try {
        await authStore.login(credentials.value);
        router.push('/dashboard');
      } catch (error) {
        if (error.response && error.response.status === 422) {
          errors.value = error.response.data.errors;
        } else {
          // Show a generic error message
          errors.value = { 
            general: [error.response?.data?.message || 'فشل تسجيل الدخول. يرجى التحقق من بياناتك والمحاولة مرة أخرى.'] 
          };
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      credentials,
      showPassword,
      loading,
      errors,
      login
    };
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background-color: var(--card-bg);
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.login-header {
  padding: 30px 20px;
  text-align: center;
  background-color: var(--primary-color);
  color: white;
}

.logo {
  margin-bottom: 10px;
}

.logo i {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.logo h2 {
  margin: 0;
  font-weight: 600;
}

.login-subtitle {
  margin: 0;
  opacity: 0.9;
}

.login-form {
  padding: 30px;
}

.input-group-text {
  background-color: transparent;
  border-right: none;
}

.form-control {
  border-left: none;
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.25rem rgba(0, 123, 255, 0.25);
}

.forgot-password-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: 0.9rem;
}

.forgot-password-link:hover {
  text-decoration: underline;
}

.login-footer {
  padding: 20px;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.02);
  border-top: 1px solid var(--border-color);
}

.login-footer p {
  margin: 0;
  font-size: 0.9rem;
}

.login-footer a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.login-footer a:hover {
  text-decoration: underline;
}

/* RTL Support */
[dir="rtl"] .input-group-text {
  border-right: 1px solid var(--border-color);
  border-left: none;
}

[dir="rtl"] .form-control {
  border-left: 1px solid var(--border-color);
  border-right: none;
}
</style>
