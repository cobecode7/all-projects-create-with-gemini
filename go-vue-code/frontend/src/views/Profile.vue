<template>
  <div class="profile-container">
    <div class="row">
      <div class="col-lg-4 mb-4">
        <div class="profile-card">
          <div class="profile-header text-center">
            <div class="profile-avatar-container mb-3">
              <img
                :src="user?.avatar || 'https://picsum.photos/seed/user123/200/200.jpg'"
                class="profile-avatar"
                alt="Avatar"
              >
              <button
                class="profile-avatar-edit"
                @click="showAvatarModal = true"
              >
                <i class="bi bi-camera-fill"></i>
              </button>
            </div>
            <h4 class="profile-name">{{ user?.firstName }} {{ user?.lastName }}</h4>
            <p class="profile-email text-muted">{{ user?.email }}</p>
            <div class="profile-badges mb-3">
              <span v-for="role in user?.roles" :key="role.id" class="badge bg-primary me-1">
                {{ role.name }}
              </span>
            </div>
          </div>

          <div class="profile-stats">
            <div class="row text-center">
              <div class="col-4">
                <div class="stat-item">
                  <h5 class="stat-value">{{ userRolesCount }}</h5>
                  <span class="stat-label">الأدوار</span>
                </div>
              </div>
              <div class="col-4">
                <div class="stat-item">
                  <h5 class="stat-value">{{ userPermissionsCount }}</h5>
                  <span class="stat-label">الصلاحيات</span>
                </div>
              </div>
              <div class="col-4">
                <div class="stat-item">
                  <h5 class="stat-value">{{ formatDate(user?.lastLogin) }}</h5>
                  <span class="stat-label">آخر دخول</span>
                </div>
              </div>
            </div>
          </div>

          <div class="profile-actions">
            <button
              class="btn btn-outline-primary w-100 mb-2"
              @click="showAvatarModal = true"
            >
              <i class="bi bi-camera-fill me-2"></i>
              تغيير الصورة الشخصية
            </button>
            <button
              class="btn btn-outline-danger w-100"
              @click="confirmLogout"
            >
              <i class="bi bi-box-arrow-right me-2"></i>
              تسجيل الخروج
            </button>
          </div>
        </div>

        <div class="roles-card">
          <div class="card-header">
            <h5 class="card-title mb-0">الأدوار والصلاحيات</h5>
          </div>
          <div class="card-body">
            <div v-if="user?.roles && user.roles.length > 0">
              <div v-for="role in user.roles" :key="role.id" class="role-item">
                <div class="role-header">
                  <h6 class="role-name">{{ role.name }}</h6>
                  <span class="role-count">{{ role.permissions?.length || 0 }} صلاحية</span>
                </div>
                <p class="role-description text-muted small">{{ role.description }}</p>
                <div v-if="role.permissions && role.permissions.length > 0" class="permissions-list">
                  <span
                    v-for="permission in role.permissions"
                    :key="permission.id"
                    class="permission-badge"
                  >
                    {{ permission.name }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="empty-state text-center py-3">
              <i class="bi bi-shield-slash fa-2x text-muted mb-2"></i>
              <p class="text-muted">لا توجد أدوار محددة</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-8 mb-4">
        <div class="profile-tabs">
          <ul class="nav nav-tabs" id="profileTabs" role="tablist">
            <li class="nav-item" role="presentation">
              <button class="nav-link active" id="account-tab" data-bs-toggle="tab" data-bs-target="#account" type="button" role="tab">
                <i class="bi bi-person me-2"></i>
                معلومات الحساب
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button class="nav-link" id="security-tab" data-bs-toggle="tab" data-bs-target="#security" type="button" role="tab">
                <i class="bi bi-shield-lock me-2"></i>
                الأمان
              </button>
            </li>
            <li class="nav-item" role="presentation">
              <button class="nav-link" id="activity-tab" data-bs-toggle="tab" data-bs-target="#activity" type="button" role="tab">
                <i class="bi bi-clock-history me-2"></i>
                النشاط
              </button>
            </li>
          </ul>
          <div class="tab-content" id="profileTabsContent">
            <div class="tab-pane fade show active" id="account" role="tabpanel">
              <div class="account-form">
                <div v-if="successMessage" class="alert alert-success d-flex align-items-center" role="alert">
                  <i class="bi bi-check-circle-fill me-2"></i>
                  {{ successMessage }}
                </div>

                <div v-if="errorMessage" class="alert alert-danger d-flex align-items-center" role="alert">
                  <i class="bi bi-exclamation-triangle-fill me-2"></i>
                  {{ errorMessage }}
                </div>

                <div class="d-flex justify-content-between align-items-center mb-4">
                  <h5>معلومات الحساب</h5>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    @click="editMode = !editMode"
                  >
                    <i class="bi bi-pencil-fill me-1"></i>
                    {{ editMode ? 'إلغاء' : 'تعديل' }}
                  </button>
                </div>

                <form @submit.prevent="updateProfile">
                  <div class="row mb-3">
                    <div class="col-md-6">
                      <label for="firstName" class="form-label">الاسم الأول</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-person"></i></span>
                        <input
                          type="text"
                          class="form-control"
                          id="firstName"
                          v-model="profileForm.firstName"
                          :disabled="!editMode"
                          placeholder="أحمد"
                        >
                      </div>
                    </div>
                    <div class="col-md-6">
                      <label for="lastName" class="form-label">الاسم الأخير</label>
                      <div class="input-group">
                        <span class="input-group-text"><i class="bi bi-person"></i></span>
                        <input
                          type="text"
                          class="form-control"
                          id="lastName"
                          v-model="profileForm.lastName"
                          :disabled="!editMode"
                          placeholder="محمد"
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
                        v-model="profileForm.username"
                        :disabled="!editMode"
                        placeholder="username"
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
                        v-model="profileForm.email"
                        :disabled="!editMode"
                        placeholder="example@email.com"
                      >
                    </div>
                  </div>

                  <div v-if="editMode" class="d-grid">
                    <button
                      type="submit"
                      class="btn btn-primary"
                      :disabled="loading"
                    >
                      <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      حفظ التغييرات
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <div class="tab-pane fade" id="security" role="tabpanel">
              <div class="security-form">
                <h5 class="mb-4">تغيير كلمة المرور</h5>

                <div v-if="passwordSuccessMessage" class="alert alert-success d-flex align-items-center" role="alert">
                  <i class="bi bi-check-circle-fill me-2"></i>
                  {{ passwordSuccessMessage }}
                </div>

                <div v-if="passwordErrorMessage" class="alert alert-danger d-flex align-items-center" role="alert">
                  <i class="bi bi-exclamation-triangle-fill me-2"></i>
                  {{ passwordErrorMessage }}
                </div>

                <form @submit.prevent="changePassword">
                  <div class="mb-3">
                    <label for="currentPassword" class="form-label">كلمة المرور الحالية</label>
                    <div class="input-group">
                      <span class="input-group-text"><i class="bi bi-lock"></i></span>
                      <input
                        :type="showCurrentPassword ? 'text' : 'password'"
                        class="form-control"
                        id="currentPassword"
                        v-model="passwordForm.currentPassword"
                        placeholder="••••••••"
                        required
                      >
                      <button class="btn btn-outline-secondary" type="button" @click="toggleCurrentPasswordVisibility">
                        <i :class="showCurrentPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                      </button>
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="newPassword" class="form-label">كلمة المرور الجديدة</label>
                    <div class="input-group">
                      <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
                      <input
                        :type="showNewPassword ? 'text' : 'password'"
                        class="form-control"
                        id="newPassword"
                        v-model="passwordForm.newPassword"
                        placeholder="••••••••"
                        required
                      >
                      <button class="btn btn-outline-secondary" type="button" @click="toggleNewPasswordVisibility">
                        <i :class="showNewPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                      </button>
                    </div>
                    <div class="form-text text-muted mt-1">
                      يجب أن تكون كلمة المرور قوية تحتوي على 8 أحرف على الأقل
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="confirmPassword" class="form-label">تأكيد كلمة المرور الجديدة</label>
                    <div class="input-group">
                      <span class="input-group-text"><i class="bi bi-lock-fill"></i></span>
                      <input
                        :type="showConfirmPassword ? 'text' : 'password'"
                        class="form-control"
                        id="confirmPassword"
                        v-model="passwordForm.confirmPassword"
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

                  <div class="d-grid">
                    <button
                      type="submit"
                      class="btn btn-primary"
                      :disabled="passwordLoading || passwordMismatch"
                    >
                      <span v-if="passwordLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      تغيير كلمة المرور
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <div class="tab-pane fade" id="activity" role="tabpanel">
              <div class="activity-timeline">
                <h5 class="mb-4">سجل النشاط</h5>
                <div class="timeline">
                  <div class="timeline-item" v-for="(activity, index) in userActivities" :key="index">
                    <div class="timeline-marker" :class="activity.type">
                      <i :class="activity.icon"></i>
                    </div>
                    <div class="timeline-content">
                      <h6 class="timeline-title">{{ activity.title }}</h6>
                      <p class="timeline-description">{{ activity.description }}</p>
                      <small class="timeline-date">{{ formatDate(activity.timestamp) }}</small>
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
            <div class="input-group">
              <span class="input-group-text"><i class="bi bi-image"></i></span>
              <input
                type="url"
                class="form-control"
                id="avatarUrl"
                v-model="avatarForm.url"
                placeholder="https://example.com/image.jpg"
              >
            </div>
          </div>
          <div class="text-center">
            <img
              :src="avatarForm.url || user?.avatar || 'https://picsum.photos/seed/user123/200/200.jpg'"
              class="rounded-circle img-fluid avatar-preview"
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
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
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

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

// Mock user activities
const userActivities = ref([
  {
    title: 'تسجيل الدخول',
    description: 'تم تسجيل الدخول من جهاز جديد',
    type: 'success',
    icon: 'bi bi-box-arrow-in-right',
    timestamp: new Date(Date.now() - 86400000 * 0.5).toISOString()
  },
  {
    title: 'تحديث الملف الشخصي',
    description: 'تم تحديث معلومات الحساب',
    type: 'info',
    icon: 'bi bi-person-gear',
    timestamp: new Date(Date.now() - 86400000 * 1).toISOString()
  },
  {
    title: 'تغيير كلمة المرور',
    description: 'تم تغيير كلمة المرور بنجاح',
    type: 'warning',
    icon: 'bi bi-shield-check',
    timestamp: new Date(Date.now() - 86400000 * 7).toISOString()
  },
  {
    title: 'إنشاء الحساب',
    description: 'تم إنشاء حساب جديد',
    type: 'primary',
    icon: 'bi bi-person-plus',
    timestamp: new Date(Date.now() - 86400000 * 30).toISOString()
  }
])

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

const confirmLogout = () => {
  if (confirm('هل أنت متأكد من أنك تريد تسجيل الخروج؟')) {
    authStore.logout()
    router.push('/login')
  }
}

const toggleCurrentPasswordVisibility = () => {
  showCurrentPassword.value = !showCurrentPassword.value
}

const toggleNewPasswordVisibility = () => {
  showNewPassword.value = !showNewPassword.value
}

const toggleConfirmPasswordVisibility = () => {
  showConfirmPassword.value = !showConfirmPassword.value
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
/* Profile Container */
.profile-container {
  padding: 1.5rem;
}

/* Profile Card */
.profile-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow);
  overflow: hidden;
  margin-bottom: 1.5rem;
}

.profile-header {
  padding: 2rem 1.5rem;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
  color: white;
}

.profile-avatar-container {
  position: relative;
  display: inline-block;
}

.profile-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid rgba(255, 255, 255, 0.2);
  object-fit: cover;
}

.profile-avatar-edit {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  border: 2px solid white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-fast);
}

.profile-avatar-edit:hover {
  background-color: var(--primary-hover);
}

.profile-name {
  font-weight: var(--font-weight-bold);
  margin-bottom: 0.5rem;
}

.profile-email {
  margin-bottom: 1rem;
  opacity: 0.9;
}

.profile-badges {
  margin-bottom: 1rem;
}

.profile-stats {
  padding: 1.5rem;
  background-color: rgba(0, 0, 0, 0.03);
}

.stat-item {
  padding: 0.5rem 0;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: var(--font-weight-bold);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.profile-actions {
  padding: 1.5rem;
}

/* Roles Card */
.roles-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.card-header {
  padding: 1rem 1.5rem;
  background-color: rgba(0, 0, 0, 0.03);
  border-bottom: 1px solid var(--border-color);
}

.card-title {
  font-weight: var(--font-weight-semibold);
  color: var(--text-color);
}

.card-body {
  padding: 1.5rem;
}

.role-item {
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.role-item:last-child {
  border-bottom: none;
}

.role-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.role-name {
  font-weight: var(--font-weight-medium);
  margin-bottom: 0;
}

.role-count {
  font-size: 0.85rem;
  color: var(--text-muted);
  background-color: var(--light-color);
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius);
}

.role-description {
  margin-bottom: 0.75rem;
}

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.permission-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  background-color: var(--light-color);
  color: var(--text-muted);
  border-radius: var(--border-radius);
}

/* Profile Tabs */
.profile-tabs {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.nav-tabs {
  border-bottom: 1px solid var(--border-color);
  padding: 0 1.5rem;
}

.nav-link {
  color: var(--text-muted);
  border: none;
  padding: 1rem 1.5rem;
  font-weight: var(--font-weight-medium);
  transition: var(--transition-fast);
}

.nav-link:hover {
  color: var(--primary-color);
  background-color: rgba(67, 97, 238, 0.05);
}

.nav-link.active {
  color: var(--primary-color);
  background-color: transparent;
  border-bottom: 3px solid var(--primary-color);
}

.tab-content {
  padding: 1.5rem;
}

/* Account Form */
.account-form {
  max-width: 600px;
}

/* Security Form */
.security-form {
  max-width: 500px;
}

/* Activity Timeline */
.activity-timeline {
  max-width: 600px;
}

.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0.5rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: var(--border-color);
}

.timeline-item {
  position: relative;
  padding-bottom: 1.5rem;
}

.timeline-marker {
  position: absolute;
  left: -1.5rem;
  top: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.75rem;
}

.timeline-marker.success {
  background-color: var(--success-color);
}

.timeline-marker.info {
  background-color: var(--info-color);
}

.timeline-marker.warning {
  background-color: var(--warning-color);
}

.timeline-marker.primary {
  background-color: var(--primary-color);
}

.timeline-content {
  background-color: var(--light-color);
  border-radius: var(--border-radius);
  padding: 1rem;
}

.timeline-title {
  font-weight: var(--font-weight-medium);
  margin-bottom: 0.25rem;
}

.timeline-description {
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}

.timeline-date {
  color: var(--text-muted);
  font-size: 0.85rem;
}

/* Modal Styles */
.modal.show {
  display: block;
  background-color: rgba(0, 0, 0, 0.5);
}

.avatar-preview {
  width: 120px;
  height: 120px;
  object-fit: cover;
}

/* Form Styles */
.form-label {
  font-weight: var(--font-weight-medium);
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.input-group {
  border-radius: var(--border-radius);
  overflow: hidden;
}

.input-group-text {
  background-color: var(--light-color);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
}

.form-control {
  border: 1px solid var(--border-color);
  padding: 0.75rem 1rem;
  transition: var(--transition-fast);
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.25rem rgba(67, 97, 238, 0.25);
}

.form-control:disabled {
  background-color: var(--light-color);
  opacity: 1;
}

.btn-outline-secondary {
  border-color: var(--border-color);
  color: var(--text-muted);
}

.btn-outline-secondary:hover {
  background-color: var(--light-color);
  color: var(--text-color);
}

/* Alert Styles */
.alert {
  border-radius: var(--border-radius);
  border: none;
  padding: 0.75rem 1rem;
}

.alert-success {
  background-color: rgba(6, 255, 165, 0.1);
  color: var(--success-color);
}

.alert-danger {
  background-color: rgba(255, 0, 110, 0.1);
  color: var(--danger-color);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem 1rem;
}

/* RTL Support */
[dir="rtl"] .profile-avatar-edit {
  left: 5px;
  right: auto;
}

[dir="rtl"] .timeline {
  padding-left: 0;
  padding-right: 2rem;
}

[dir="rtl"] .timeline::before {
  left: auto;
  right: 0.5rem;
}

[dir="rtl"] .timeline-marker {
  left: auto;
  right: -1.5rem;
}

[dir="rtl"] .input-group-text {
  border-left: none;
  border-right: 1px solid var(--border-color);
}

[dir="rtl"] .btn-outline-secondary {
  border-left: 1px solid var(--border-color);
  border-right: none;
}

[dir="rtl"] .alert i {
  margin-right: 0;
  margin-left: 0.5rem;
}
</style>
