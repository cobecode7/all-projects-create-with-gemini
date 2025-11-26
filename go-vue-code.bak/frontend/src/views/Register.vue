<template>
  <div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
      <div class="card shadow">
        <div class="card-body p-4">
          <h2 class="text-center mb-4">إنشاء حساب جديد</h2>

          <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
          </div>

          <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
          </div>

          <form @submit.prevent="handleRegister">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="firstName" class="form-label">الاسم الأول</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="firstName" 
                  v-model="form.firstName"
                  required
                >
              </div>
              <div class="col-md-6 mb-3">
                <label for="lastName" class="form-label">الاسم الأخير</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="lastName" 
                  v-model="form.lastName"
                  required
                >
              </div>
            </div>

            <div class="mb-3">
              <label for="username" class="form-label">اسم المستخدم</label>
              <input 
                type="text" 
                class="form-control" 
                id="username" 
                v-model="form.username"
                required
              >
            </div>

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

            <div class="mb-3">
              <label for="confirmPassword" class="form-label">تأكيد كلمة المرور</label>
              <input 
                type="password" 
                class="form-control" 
                id="confirmPassword" 
                v-model="form.confirmPassword"
                required
              >
              <div v-if="passwordMismatch" class="form-text text-danger">
                كلمات المرور غير متطابقة
              </div>
            </div>

            <div class="d-grid">
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="loading || passwordMismatch"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                إنشاء حساب
              </button>
            </div>
          </form>

          <div class="mt-3 text-center">
            <p>لديك حساب بالفعل؟ <router-link to="/login">تسجيل الدخول</router-link></p>
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
  confirmPassword: ''
})

const loading = ref(false)
const error = ref('')
const successMessage = ref('')

const passwordMismatch = computed(() => {
  return form.password && form.confirmPassword && form.password !== form.confirmPassword
})

const handleRegister = async () => {
  if (passwordMismatch.value) return

  loading.value = true
  error.value = ''
  successMessage.value = ''

  try {
    await authStore.register(form)
    successMessage.value = 'تم إنشاء حسابك بنجاح! يمكنك الآن تسجيل الدخول.'

    // Reset form
    Object.keys(form).forEach(key => {
      form[key] = ''
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
</script>
