<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-4">
      <div class="card shadow">
        <div class="card-body p-4">
          <h2 class="text-center mb-4">تسجيل الدخول</h2>

          <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
          </div>

          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="email" class="form-label">البريد الإلكتروني</label>
              <input 
                type="email" 
                class="form-control" 
                id="email" 
                v-model="form.email"
                required
              >
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">كلمة المرور</label>
              <input 
                type="password" 
                class="form-control" 
                id="password" 
                v-model="form.password"
                required
              >
            </div>
            <div class="mb-3 form-check">
              <input type="checkbox" class="form-check-input" id="remember">
              <label class="form-check-label" for="remember">تذكرني</label>
            </div>
            <div class="d-grid">
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                تسجيل الدخول
              </button>
            </div>
          </form>

          <div class="mt-3 text-center">
            <p>ليس لديك حساب؟ <router-link to="/register">إنشاء حساب جديد</router-link></p>
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
  password: ''
})

const loading = ref(false)
const error = ref('')

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
</script>
