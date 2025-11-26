<template>
  <div class="profile-container">
    <div class="page-header">
      <h2>الملف الشخصي</h2>
    </div>

    <div class="row">
      <div class="col-md-4">
        <div class="card">
          <div class="card-body text-center">
            <div class="profile-avatar">
              <img v-if="user.avatar" :src="user.avatar" alt="User Avatar" class="avatar-img">
              <div v-else class="avatar-placeholder">
                <i class="fas fa-user"></i>
              </div>
              <div class="avatar-upload">
                <input type="file" id="avatar-upload" @change="handleAvatarUpload" accept="image/*" class="d-none">
                <label for="avatar-upload" class="btn btn-sm btn-primary">
                  <i class="fas fa-camera"></i> تغيير الصورة
                </label>
              </div>
            </div>
            <h4 class="mt-3">{{ user.firstName }} {{ user.lastName }}</h4>
            <p class="text-muted">{{ user.email }}</p>
            <div class="profile-stats">
              <div class="stat-item">
                <span class="stat-value">{{ user.role ? user.role.name : 'N/A' }}</span>
                <span class="stat-label">الدور</span>
              </div>
              <div class="stat-item">
                <span class="stat-value">{{ formatDate(user.createdAt) }}</span>
                <span class="stat-label">تاريخ الانضمام</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeTab === 'info' }" href="#" @click.prevent="activeTab = 'info'">
                  معلومات شخصية
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeTab === 'password' }" href="#" @click.prevent="activeTab = 'password'">
                  تغيير كلمة المرور
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" :class="{ active: activeTab === 'preferences' }" href="#" @click.prevent="activeTab = 'preferences'">
                  التفضيلات
                </a>
              </li>
            </ul>
          </div>
          <div class="card-body">
            <!-- Personal Info Tab -->
            <div v-if="activeTab === 'info'">
              <form @submit.prevent="updateProfile">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="firstName" class="form-label">الاسم الأول</label>
                    <input type="text" class="form-control" id="firstName" v-model="profileData.firstName" required>
                    <div class="invalid-feedback" v-if="errors.firstName">
                      {{ errors.firstName[0] }}
                    </div>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="lastName" class="form-label">الاسم الأخير</label>
                    <input type="text" class="form-control" id="lastName" v-model="profileData.lastName" required>
                    <div class="invalid-feedback" v-if="errors.lastName">
                      {{ errors.lastName[0] }}
                    </div>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="email" class="form-label">البريد الإلكتروني</label>
                  <input type="email" class="form-control" id="email" v-model="profileData.email" required>
                  <div class="invalid-feedback" v-if="errors.email">
                    {{ errors.email[0] }}
                  </div>
                </div>

                <div class="mb-3">
                  <label for="phone" class="form-label">رقم الهاتف</label>
                  <input type="tel" class="form-control" id="phone" v-model="profileData.phone">
                  <div class="invalid-feedback" v-if="errors.phone">
                    {{ errors.phone[0] }}
                  </div>
                </div>

                <div class="mb-3">
                  <label for="address" class="form-label">العنوان</label>
                  <textarea class="form-control" id="address" rows="3" v-model="profileData.address"></textarea>
                  <div class="invalid-feedback" v-if="errors.address">
                    {{ errors.address[0] }}
                  </div>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                    حفظ التغييرات
                  </button>
                </div>
              </form>
            </div>

            <!-- Password Tab -->
            <div v-if="activeTab === 'password'">
              <form @submit.prevent="changePassword">
                <div class="mb-3">
                  <label for="currentPassword" class="form-label">كلمة المرور الحالية</label>
                  <div class="input-group">
                    <input :type="showCurrentPassword ? 'text' : 'password'" class="form-control" id="currentPassword" v-model="passwordData.currentPassword" required>
                    <button class="btn btn-outline-secondary" type="button" @click="showCurrentPassword = !showCurrentPassword">
                      <i :class="showCurrentPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                  <div class="invalid-feedback" v-if="errors.currentPassword">
                    {{ errors.currentPassword[0] }}
                  </div>
                </div>

                <div class="mb-3">
                  <label for="newPassword" class="form-label">كلمة المرور الجديدة</label>
                  <div class="input-group">
                    <input :type="showNewPassword ? 'text' : 'password'" class="form-control" id="newPassword" v-model="passwordData.newPassword" required>
                    <button class="btn btn-outline-secondary" type="button" @click="showNewPassword = !showNewPassword">
                      <i :class="showNewPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                  <div class="invalid-feedback" v-if="errors.newPassword">
                    {{ errors.newPassword[0] }}
                  </div>
                </div>

                <div class="mb-3">
                  <label for="passwordConfirmation" class="form-label">تأكيد كلمة المرور الجديدة</label>
                  <div class="input-group">
                    <input :type="showPasswordConfirmation ? 'text' : 'password'" class="form-control" id="passwordConfirmation" v-model="passwordData.passwordConfirmation" required>
                    <button class="btn btn-outline-secondary" type="button" @click="showPasswordConfirmation = !showPasswordConfirmation">
                      <i :class="showPasswordConfirmation ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                  </div>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                    تغيير كلمة المرور
                  </button>
                </div>
              </form>
            </div>

            <!-- Preferences Tab -->
            <div v-if="activeTab === 'preferences'">
              <form @submit.prevent="updatePreferences">
                <div class="mb-3">
                  <label class="form-label">اللغة</label>
                  <select class="form-select" v-model="preferences.language">
                    <option value="ar">العربية</option>
                    <option value="en">English</option>
                  </select>
                </div>

                <div class="mb-3">
                  <label class="form-label">المظهر</label>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="theme" id="light-theme" value="light" v-model="preferences.theme">
                    <label class="form-check-label" for="light-theme">
                      فاتح
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="theme" id="dark-theme" value="dark" v-model="preferences.theme">
                    <label class="form-check-label" for="dark-theme">
                      داكن
                    </label>
                  </div>
                </div>

                <div class="mb-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="email-notifications" v-model="preferences.emailNotifications">
                    <label class="form-check-label" for="email-notifications">
                      تلقي إشعارات عبر البريد الإلكتروني
                    </label>
                  </div>
                </div>

                <div class="mb-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="push-notifications" v-model="preferences.pushNotifications">
                    <label class="form-check-label" for="push-notifications">
                      تلقي إشعارات فورية
                    </label>
                  </div>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                    حفظ التفضيلات
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useSettingsStore } from '@/stores/settings';

export default {
  name: 'Profile',
  setup() {
    const authStore = useAuthStore();
    const settingsStore = useSettingsStore();

    const user = computed(() => authStore.user);
    const activeTab = ref('info');
    const loading = ref(false);
    const errors = ref({});

    // Profile data
    const profileData = ref({
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      address: ''
    });

    // Password data
    const passwordData = ref({
      currentPassword: '',
      newPassword: '',
      passwordConfirmation: ''
    });

    // Password visibility
    const showCurrentPassword = ref(false);
    const showNewPassword = ref(false);
    const showPasswordConfirmation = ref(false);

    // Preferences
    const preferences = ref({
      language: settingsStore.language,
      theme: settingsStore.theme,
      emailNotifications: true,
      pushNotifications: true
    });

    // Initialize form data
    onMounted(() => {
      if (user.value) {
        profileData.value = {
          firstName: user.value.firstName || '',
          lastName: user.value.lastName || '',
          email: user.value.email || '',
          phone: user.value.phone || '',
          address: user.value.address || ''
        };
      }
    });

    const updateProfile = async () => {
      loading.value = true;
      errors.value = {};

      try {
        await authStore.updateProfile(profileData.value);
        // Show success message
      } catch (error) {
        if (error.response && error.response.status === 422) {
          errors.value = error.response.data.errors;
        }
      } finally {
        loading.value = false;
      }
    };

    const changePassword = async () => {
      loading.value = true;
      errors.value = {};

      try {
        await authStore.changePassword(passwordData.value);
        // Reset form
        passwordData.value = {
          currentPassword: '',
          newPassword: '',
          passwordConfirmation: ''
        };
        // Show success message
      } catch (error) {
        if (error.response && error.response.status === 422) {
          errors.value = error.response.data.errors;
        }
      } finally {
        loading.value = false;
      }
    };

    const updatePreferences = async () => {
      loading.value = true;

      try {
        // Update language
        settingsStore.setLanguage(preferences.value.language);

        // Update theme
        settingsStore.setTheme(preferences.value.theme);

        // Save other preferences (in a real app, this would be saved to the server)

        // Show success message
      } catch (error) {
        console.error('Failed to update preferences:', error);
      } finally {
        loading.value = false;
      }
    };

    const handleAvatarUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        // In a real app, this would upload the file to the server
        console.log('Avatar upload:', file);
      }
    };

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('ar-SA', options);
    };

    return {
      user,
      activeTab,
      loading,
      errors,
      profileData,
      passwordData,
      showCurrentPassword,
      showNewPassword,
      showPasswordConfirmation,
      preferences,
      updateProfile,
      changePassword,
      updatePreferences,
      handleAvatarUpload,
      formatDate
    };
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
}

.profile-avatar {
  position: relative;
  margin-bottom: 20px;
}

.avatar-img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--primary-color);
}

.avatar-placeholder {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: var(--light-color);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  border: 4px solid var(--primary-color);
}

.avatar-placeholder i {
  font-size: 3rem;
  color: var(--text-muted);
}

.avatar-upload {
  position: absolute;
  bottom: 10px;
  right: 50%;
  transform: translateX(50%);
}

.profile-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-color);
}

.stat-label {
  display: block;
  font-size: 0.8rem;
  color: var(--text-muted);
}

.nav-tabs .nav-link {
  color: var(--text-muted);
}

.nav-tabs .nav-link.active {
  color: var(--primary-color);
  font-weight: 500;
}
</style>
