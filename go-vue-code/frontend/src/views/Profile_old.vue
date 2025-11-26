<template>
  <div class="row">
    <div class="col-md-4">
      <div class="card mb-4">
        <div class="card-body text-center">
          <div class="mb-3">
            <img 
              :src="user?.avatar || 'https://picsum.photos/seed/user123/200/200.jpg'" 
              class="rounded-circle img-fluid" 
              style="width: 150px;"
              alt="Avatar"
            >
          </div>
          <h4>{{ user?.firstName }} {{ user?.lastName }}</h4>
          <p class="text-muted">{{ user?.email }}</p>

          <div class="d-flex justify-content-center mb-2">
            <div class="px-2">
              <h6 class="mb-0">{{ userRolesCount }}</h6>
              <small class="text-muted">الأدوار</small>
            </div>
            <div class="px-2 border-start border-end">
              <h6 class="mb-0">{{ userPermissionsCount }}</h6>
              <small class="text-muted">الصلاحيات</small>
            </div>
            <div class="px-2">
              <h6 class="mb-0">{{ formatDate(user?.lastLogin) }}</h6>
              <small class="text-muted">آخر تسجيل دخول</small>
            </div>
          </div>

          <div class="d-grid mt-3">
            <button 
              class="btn btn-outline-primary"
              @click="showAvatarModal = true"
            >
              <i class="bi bi-camera-fill me-1"></i>
              تغيير الصورة الشخصية
            </button>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">الأدوار والصلاحيات</h5>
        </div>
        <div class="card-body">
          <div v-if="user?.roles && user.roles.length > 0">
            <div v-for="role in user.roles" :key="role.id" class="mb-3">
              <h6>{{ role.name }}</h6>
              <p class="text-muted small">{{ role.description }}</p>
              <div v-if="role.permissions && role.permissions.length > 0">
                <span 
                  v-for="permission in role.permissions" 
                  :key="permission.id" 
                  class="badge bg-secondary me-1 mb-1"
                >
                  {{ permission.name }}
                </span>
              </div>
            </div>
          </div>
          <div v-else class="text-center text-muted">
            لا توجد أدوار محددة
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-8">
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">معلومات الحساب</h5>
          <button 
            class="btn btn-sm btn-outline-secondary"
            @click="editMode = !editMode"
          >
            <i class="bi bi-pencil-fill me-1"></i>
            {{ editMode ? 'إلغاء' : 'تعديل' }}
          </button>
        </div>
        <div class="card-body">
          <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
          </div>

          <div v-if="errorMessage" class="alert alert-danger" role="alert">
            {{ errorMessage }}
          </div>

          <form @submit.prevent="updateProfile">
            <div class="row mb-3">
              <div class="col-md-6">
                <label for="firstName" class="form-label">الاسم الأول</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="firstName" 
                  v-model="profileForm.firstName"
                  :disabled="!editMode"
                >
              </div>
              <div class="col-md-6">
                <label for="lastName" class="form-label">الاسم الأخير</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="lastName" 
                  v-model="profileForm.lastName"
                  :disabled="!editMode"
                >
              </div>
            </div>

            <div class="mb-3">
              <label for="username" class="form-label">اسم المستخدم</label>
              <input 
                type="text" 
                class="form-control" 
                id="username" 
                v-model="profileForm.username"
                :disabled="!editMode"
              >
            </div>

            <div class="mb-3">
              <label for="email" class="form-label">البريد الإلكتروني</label>
              <input 
                type="email" 
                class="form-control" 
                id="email" 
                v-model="profileForm.email"
                :disabled="!editMode"
              >
            </div>

            <div v-if="editMode" class="d-grid">
              <button 
                type="submit" 
                class="btn btn-primary"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                حفظ التغييرات
              </button>
            </div>
          </form>
        </div>
      </div>

      <div class="card mt-4">
        <div class="card-header">
          <h5 class="card-title mb-0">تغيير كلمة المرور</h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="changePassword">
            <div v-if="passwordSuccessMessage" class="alert alert-success" role="alert">
              {{ passwordSuccessMessage }}
            </div>

            <div v-if="passwordErrorMessage" class="alert alert-danger" role="alert">
              {{ passwordErrorMessage }}
            </div>

            <div class="mb-3">
              <label for="currentPassword" class="form-label">كلمة المرور الحالية</label>
              <input 
                type="password" 
                class="form-control" 
                id="currentPassword" 
                v-model="passwordForm.currentPassword"
                required
              >
            </div>

            <div class="mb-3">
              <label for="newPassword" class="form-label">كلمة المرور الجديدة</label>
              <input 
                type="password" 
                class="form-control" 
                id="newPassword" 
                v-model="passwordForm.newPassword"
                required
              >
            </div>

            <div class="mb-3">
              <label for="confirmPassword" class="form-label">تأكيد كلمة المرور الجديدة</label>
              <input 
                type="password" 
                class="form-control" 
                id="confirmPassword" 
                v-model="passwordForm.confirmPassword"
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
                :disabled="passwordLoading || passwordMismatch"
              >
                <span v-if="passwordLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                تغيير كلمة المرور
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Avatar Modal -->
  <div class="modal fade" :class="{ show: showAvatarModal }" :style="{ display: showAvatarModal ? 'block' : 'none' }" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">تغيير الصورة الشخصية</h5>
          <button type="button" class="btn-close" @click="showAvatarModal = false"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="avatarUrl" class="form-label">رابط الصورة</label>
            <input 
              type="url" 
              class="form-control" 
              id="avatarUrl" 
              v-model="avatarForm.url"
              placeholder="https://example.com/image.jpg"
            >
          </div>
          <div class="text-center">
            <img 
              :src="avatarForm.url || user?.avatar || 'https://picsum.photos/seed/user123/200/200.jpg'" 
              class="rounded-circle img-fluid" 
              style="width: 150px;"
              alt="Avatar Preview"
            >
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showAvatarModal = false">إلغاء</button>
          <button type="button" class="btn btn-primary" @click="updateAvatar">حفظ</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const user = computed(() => authStore.user)

const editMode = ref(false)
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const profileForm = reactive({
  firstName: '',
  lastName: '',
  username: '',
  email: ''
})

const passwordLoading = ref(false)
const passwordSuccessMessage = ref('')
const passwordErrorMessage = ref('')

const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordMismatch = computed(() => {
  return passwordForm.newPassword && passwordForm.confirmPassword && 
         passwordForm.newPassword !== passwordForm.confirmPassword
})

const showAvatarModal = ref(false)
const avatarForm = reactive({
  url: ''
})

const userRolesCount = computed(() => {
  return user.value?.roles?.length || 0
})

const userPermissionsCount = computed(() => {
  if (!user.value?.roles) return 0

  const allPermissions = new Set()
  user.value.roles.forEach(role => {
    if (role.permissions) {
      role.permissions.forEach(permission => {
        allPermissions.add(permission.id)
      })
    }
  })

  return allPermissions.size
})

onMounted(() => {
  // Initialize form with user data
  if (user.value) {
    profileForm.firstName = user.value.firstName || ''
    profileForm.lastName = user.value.lastName || ''
    profileForm.username = user.value.username || ''
    profileForm.email = user.value.email || ''
    avatarForm.url = user.value.avatar || ''
  }
})

const updateProfile = async () => {
  loading.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    // In a real application, you would call your API
    // await authStore.updateProfile(profileForm)

    // Mock successful update for demonstration
    setTimeout(() => {
      successMessage.value = 'تم تحديث معلومات الحساب بنجاح!'
      editMode.value = false
      loading.value = false
    }, 1000)
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'فشل تحديث الملف الشخصي. يرجى المحاولة مرة أخرى.'
    loading.value = false
  }
}

const changePassword = async () => {
  if (passwordMismatch.value) return

  passwordLoading.value = true
  passwordSuccessMessage.value = ''
  passwordErrorMessage.value = ''

  try {
    // In a real application, you would call your API
    // await axios.post('/api/auth/change-password', passwordForm)

    // Mock successful password change for demonstration
    setTimeout(() => {
      passwordSuccessMessage.value = 'تم تغيير كلمة المرور بنجاح!'

      // Reset form
      passwordForm.currentPassword = ''
      passwordForm.newPassword = ''
      passwordForm.confirmPassword = ''

      passwordLoading.value = false
    }, 1000)
  } catch (error) {
    passwordErrorMessage.value = error.response?.data?.error || 'فشل تغيير كلمة المرور. يرجى المحاولة مرة أخرى.'
    passwordLoading.value = false
  }
}

const updateAvatar = () => {
  // In a real application, you would call your API
  // await authStore.updateProfile({ avatar: avatarForm.url })

  // Mock successful update for demonstration
  if (user.value) {
    user.value.avatar = avatarForm.url
  }

  showAvatarModal.value = false
}

const formatDate = (dateString) => {
  if (!dateString) return 'لم يسجل دخوله بعد'

  const date = new Date(dateString)
  return date.toLocaleDateString('ar-SA', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.modal.show {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
