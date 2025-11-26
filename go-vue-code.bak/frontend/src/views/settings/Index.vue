<template>
  <div class="settings-container">
    <div class="page-header">
      <h2>الإعدادات</h2>
    </div>

    <div class="row">
      <div class="col-md-3">
        <div class="card">
          <div class="card-body p-0">
            <div class="list-group list-group-flush">
              <a href="#" class="list-group-item list-group-item-action" 
                 :class="{ active: activeTab === 'general' }" @click.prevent="activeTab = 'general'">
                <i class="fas fa-cog me-2"></i> عام
              </a>
              <a href="#" class="list-group-item list-group-item-action" 
                 :class="{ active: activeTab === 'appearance' }" @click.prevent="activeTab = 'appearance'">
                <i class="fas fa-palette me-2"></i> المظهر
              </a>
              <a href="#" class="list-group-item list-group-item-action" 
                 :class="{ active: activeTab === 'notifications' }" @click.prevent="activeTab = 'notifications'">
                <i class="fas fa-bell me-2"></i> الإشعارات
              </a>
              <a href="#" class="list-group-item list-group-item-action" 
                 :class="{ active: activeTab === 'security' }" @click.prevent="activeTab = 'security'">
                <i class="fas fa-shield-alt me-2"></i> الأمان
              </a>
              <a href="#" class="list-group-item list-group-item-action" 
                 :class="{ active: activeTab === 'backup' }" @click.prevent="activeTab = 'backup'">
                <i class="fas fa-database me-2"></i> النسخ الاحتياطي
              </a>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-9">
        <div class="card">
          <div class="card-body">
            <!-- General Settings -->
            <div v-if="activeTab === 'general'">
              <h4 class="mb-4">الإعدادات العامة</h4>
              <form @submit.prevent="saveGeneralSettings">
                <div class="mb-3">
                  <label for="siteName" class="form-label">اسم الموقع</label>
                  <input type="text" class="form-control" id="siteName" v-model="generalSettings.siteName">
                </div>

                <div class="mb-3">
                  <label for="siteDescription" class="form-label">وصف الموقع</label>
                  <textarea class="form-control" id="siteDescription" rows="3" v-model="generalSettings.siteDescription"></textarea>
                </div>

                <div class="mb-3">
                  <label for="adminEmail" class="form-label">بريد المدير</label>
                  <input type="email" class="form-control" id="adminEmail" v-model="generalSettings.adminEmail">
                </div>

                <div class="mb-3">
                  <label for="defaultLanguage" class="form-label">اللغة الافتراضية</label>
                  <select class="form-select" id="defaultLanguage" v-model="generalSettings.defaultLanguage">
                    <option value="ar">العربية</option>
                    <option value="en">English</option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="timezone" class="form-label">المنطقة الزمنية</label>
                  <select class="form-select" id="timezone" v-model="generalSettings.timezone">
                    <option value="Asia/Riyadh">الرياض (GMT+3)</option>
                    <option value="Asia/Dubai">دبي (GMT+4)</option>
                    <option value="Africa/Cairo">القاهرة (GMT+2)</option>
                    <option value="Europe/London">لندن (GMT+0)</option>
                    <option value="America/New_York">نيويورك (GMT-5)</option>
                  </select>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                    حفظ الإعدادات
                  </button>
                </div>
              </form>
            </div>

            <!-- Appearance Settings -->
            <div v-if="activeTab === 'appearance'">
              <h4 class="mb-4">إعدادات المظهر</h4>
              <form @submit.prevent="saveAppearanceSettings">
                <div class="mb-3">
                  <label class="form-label">السمة</label>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="theme" id="light-theme" value="light" v-model="appearanceSettings.theme">
                    <label class="form-check-label" for="light-theme">
                      فاتح
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="theme" id="dark-theme" value="dark" v-model="appearanceSettings.theme">
                    <label class="form-check-label" for="dark-theme">
                      داكن
                    </label>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="primaryColor" class="form-label">اللون الأساسي</label>
                  <div class="input-group">
                    <input type="color" class="form-control form-control-color" id="primaryColor" v-model="appearanceSettings.primaryColor">
                    <input type="text" class="form-control" v-model="appearanceSettings.primaryColor">
                  </div>
                </div>

                <div class="mb-3">
                  <label for="logo" class="form-label">شعار الموقع</label>
                  <input type="file" class="form-control" id="logo" @change="handleLogoUpload" accept="image/*">
                  <div class="mt-2" v-if="appearanceSettings.logo">
                    <img :src="appearanceSettings.logo" alt="Logo" class="img-thumbnail" style="max-height: 100px;">
                  </div>
                </div>

                <div class="mb-3">
                  <label for="favicon" class="form-label">أيقونة الموقع</label>
                  <input type="file" class="form-control" id="favicon" @change="handleFaviconUpload" accept="image/x-icon">
                  <div class="mt-2" v-if="appearanceSettings.favicon">
                    <img :src="appearanceSettings.favicon" alt="Favicon" class="img-thumbnail" style="max-height: 32px;">
                  </div>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                    حفظ الإعدادات
                  </button>
                </div>
              </form>
            </div>

            <!-- Notification Settings -->
            <div v-if="activeTab === 'notifications'">
              <h4 class="mb-4">إعدادات الإشعارات</h4>
              <form @submit.prevent="saveNotificationSettings">
                <div class="mb-3">
                  <label class="form-label">إشعارات البريد الإلكتروني</label>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="email-new-user" v-model="notificationSettings.emailNewUser">
                    <label class="form-check-label" for="email-new-user">
                      عند تسجيل مستخدم جديد
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="email-new-order" v-model="notificationSettings.emailNewOrder">
                    <label class="form-check-label" for="email-new-order">
                      عند إنشاء طلب جديد
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="email-system-update" v-model="notificationSettings.emailSystemUpdate">
                    <label class="form-check-label" for="email-system-update">
                      عند تحديث النظام
                    </label>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label">إشعارات داخل النظام</label>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="internal-new-user" v-model="notificationSettings.internalNewUser">
                    <label class="form-check-label" for="internal-new-user">
                      عند تسجيل مستخدم جديد
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="internal-new-order" v-model="notificationSettings.internalNewOrder">
                    <label class="form-check-label" for="internal-new-order">
                      عند إنشاء طلب جديد
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="internal-system-update" v-model="notificationSettings.internalSystemUpdate">
                    <label class="form-check-label" for="internal-system-update">
                      عند تحديث النظام
                    </label>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="notification-frequency" class="form-label">تكرار تلخيص الإشعارات</label>
                  <select class="form-select" id="notification-frequency" v-model="notificationSettings.summaryFrequency">
                    <option value="daily">يومي</option>
                    <option value="weekly">أسبوعي</option>
                    <option value="monthly">شهري</option>
                    <option value="never">أبداً</option>
                  </select>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                    حفظ الإعدادات
                  </button>
                </div>
              </form>
            </div>

            <!-- Security Settings -->
            <div v-if="activeTab === 'security'">
              <h4 class="mb-4">إعدادات الأمان</h4>
              <form @submit.prevent="saveSecuritySettings">
                <div class="mb-3">
                  <label for="session-timeout" class="form-label">مدة انتهاء صلاحية الجلسة (بالدقائق)</label>
                  <input type="number" class="form-control" id="session-timeout" v-model="securitySettings.sessionTimeout">
                </div>

                <div class="mb-3">
                  <label for="max-login-attempts" class="form-label">الحد الأقصى لمحاولات تسجيل الدخول</label>
                  <input type="number" class="form-control" id="max-login-attempts" v-model="securitySettings.maxLoginAttempts">
                </div>

                <div class="mb-3">
                  <label for="lockout-duration" class="form-label">مدة قفل الحساب (بالدقائق)</label>
                  <input type="number" class="form-control" id="lockout-duration" v-model="securitySettings.lockoutDuration">
                </div>

                <div class="mb-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="require-2fa" v-model="securitySettings.requireTwoFactorAuth">
                    <label class="form-check-label" for="require-2fa">
                      تفعيل المصادقة الثنائية للمسؤولين
                    </label>
                  </div>
                </div>

                <div class="mb-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="password-strength" v-model="securitySettings.requireStrongPassword">
                    <label class="form-check-label" for="password-strength">
                      فرض كلمات مرور قوية
                    </label>
                  </div>
                </div>

                <div class="mb-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="ip-whitelist" v-model="securitySettings.enableIpWhitelist">
                    <label class="form-check-label" for="ip-whitelist">
                      تفعيل القائمة البيضاء لعناوين IP
                    </label>
                  </div>

                  <div v-if="securitySettings.enableIpWhitelist" class="mt-2">
                    <label for="ip-list" class="form-label">عناوين IP المسموح بها</label>
                    <textarea class="form-control" id="ip-list" rows="3" 
                             v-model="securitySettings.ipWhitelist" 
                             placeholder="أدخل عناوين IP، كل عنوان في سطر منفصل"></textarea>
                  </div>
                </div>

                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary" :disabled="loading">
                    <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                    حفظ الإعدادات
                  </button>
                </div>
              </form>
            </div>

            <!-- Backup Settings -->
            <div v-if="activeTab === 'backup'">
              <h4 class="mb-4">إعدادات النسخ الاحتياطي</h4>

              <div class="card mb-4">
                <div class="card-header">
                  <h5>النسخ الاحتياطي التلقائي</h5>
                </div>
                <div class="card-body">
                  <form @submit.prevent="saveBackupSettings">
                    <div class="mb-3">
                      <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="enable-auto-backup" v-model="backupSettings.enableAutoBackup">
                        <label class="form-check-label" for="enable-auto-backup">
                          تفعيل النسخ الاحتياطي التلقائي
                        </label>
                      </div>
                    </div>

                    <div v-if="backupSettings.enableAutoBackup">
                      <div class="mb-3">
                        <label for="backup-frequency" class="form-label">تكرار النسخ الاحتياطي</label>
                        <select class="form-select" id="backup-frequency" v-model="backupSettings.frequency">
                          <option value="daily">يومي</option>
                          <option value="weekly">أسبوعي</option>
                          <option value="monthly">شهري</option>
                        </select>
                      </div>

                      <div class="mb-3">
                        <label for="backup-time" class="form-label">وقت النسخ الاحتياطي</label>
                        <input type="time" class="form-control" id="backup-time" v-model="backupSettings.time">
                      </div>

                      <div class="mb-3">
                        <label for="backup-retention" class="form-label">عدد النسخ الاحتياطية المحتفظ بها</label>
                        <input type="number" class="form-control" id="backup-retention" v-model="backupSettings.retention">
                      </div>
                    </div>

                    <div class="d-flex justify-content-end">
                      <button type="submit" class="btn btn-primary" :disabled="loading">
                        <div class="spinner-border spinner-border-sm me-2" role="status" v-if="loading">
                          <span class="visually-hidden">جاري التحميل...</span>
                        </div>
                        حفظ الإعدادات
                      </button>
                    </div>
                  </form>
                </div>
              </div>

              <div class="card">
                <div class="card-header">
                  <h5>النسخ الاحتياطي اليدوي</h5>
                </div>
                <div class="card-body">
                  <p>يمكنك إنشاء نسخة احتياطية يدوية من قاعدة البيانات والملفات في أي وقت.</p>
                  <button class="btn btn-primary" @click="createBackup" :disabled="creatingBackup">
                    <div class="spinner-border spinner-border-sm me-2" role="status" v-if="creatingBackup">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                    إنشاء نسخة احتياطية الآن
                  </button>
                </div>
              </div>

              <div class="card mt-4">
                <div class="card-header">
                  <h5>النسخ الاحتياطية المتاحة</h5>
                </div>
                <div class="card-body">
                  <div v-if="loadingBackups" class="text-center py-3">
                    <div class="spinner-border" role="status">
                      <span class="visually-hidden">جاري التحميل...</span>
                    </div>
                  </div>
                  <div v-else-if="backups.length === 0" class="text-center py-3">
                    لا توجد نسخ احتياطية متاحة
                  </div>
                  <div v-else>
                    <div class="table-responsive">
                      <table class="table table-hover">
                        <thead>
                          <tr>
                            <th>اسم الملف</th>
                            <th>الحجم</th>
                            <th>تاريخ الإنشاء</th>
                            <th>الإجراءات</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="backup in backups" :key="backup.id">
                            <td>{{ backup.fileName }}</td>
                            <td>{{ formatFileSize(backup.size) }}</td>
                            <td>{{ formatDate(backup.createdAt) }}</td>
                            <td>
                              <div class="btn-group">
                                <button class="btn btn-sm btn-outline-primary" @click="downloadBackup(backup)">
                                  <i class="fas fa-download"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteBackup(backup)">
                                  <i class="fas fa-trash"></i>
                                </button>
                              </div>
                            </td>
                          </tr>
                        </tbody>
                      </table>
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
</template>

<script>
import { ref, onMounted } from 'vue';
import { useSettingsStore } from '@/stores/settings';
import adminService from '@/services/adminService';

export default {
  name: 'Settings',
  setup() {
    const settingsStore = useSettingsStore();
    const activeTab = ref('general');
    const loading = ref(false);
    const creatingBackup = ref(false);
    const loadingBackups = ref(false);
    const backups = ref([]);

    // Settings data
    const generalSettings = ref({
      siteName: '',
      siteDescription: '',
      adminEmail: '',
      defaultLanguage: 'ar',
      timezone: 'Asia/Riyadh'
    });

    const appearanceSettings = ref({
      theme: 'light',
      primaryColor: '#007bff',
      logo: '',
      favicon: ''
    });

    const notificationSettings = ref({
      emailNewUser: true,
      emailNewOrder: true,
      emailSystemUpdate: true,
      internalNewUser: true,
      internalNewOrder: true,
      internalSystemUpdate: true,
      summaryFrequency: 'daily'
    });

    const securitySettings = ref({
      sessionTimeout: 30,
      maxLoginAttempts: 5,
      lockoutDuration: 15,
      requireTwoFactorAuth: false,
      requireStrongPassword: true,
      enableIpWhitelist: false,
      ipWhitelist: ''
    });

    const backupSettings = ref({
      enableAutoBackup: true,
      frequency: 'daily',
      time: '02:00',
      retention: 7
    });

    // Load settings on component mount
    onMounted(async () => {
      await fetchSettings();
      await fetchBackups();
    });

    const fetchSettings = async () => {
      loading.value = true;
      try {
        const settings = await adminService.getSettings();

        // Update settings objects with fetched data
        if (settings.general) {
          generalSettings.value = { ...generalSettings.value, ...settings.general };
        }

        if (settings.appearance) {
          appearanceSettings.value = { ...appearanceSettings.value, ...settings.appearance };
        }

        if (settings.notifications) {
          notificationSettings.value = { ...notificationSettings.value, ...settings.notifications };
        }

        if (settings.security) {
          securitySettings.value = { ...securitySettings.value, ...settings.security };
        }

        if (settings.backup) {
          backupSettings.value = { ...backupSettings.value, ...settings.backup };
        }
      } catch (error) {
        console.error('Failed to fetch settings:', error);
      } finally {
        loading.value = false;
      }
    };

    const fetchBackups = async () => {
      loadingBackups.value = true;
      try {
        // This would be an actual API call in a real app
        // const response = await adminService.getBackups();
        // backups.value = response.data;

        // Mock data for demonstration
        backups.value = [
          {
            id: 1,
            fileName: 'backup_2023_05_15_02_00.sql',
            size: 2048576,
            createdAt: '2023-05-15T02:00:00Z'
          },
          {
            id: 2,
            fileName: 'backup_2023_05_08_02_00.sql',
            size: 1984512,
            createdAt: '2023-05-08T02:00:00Z'
          }
        ];
      } catch (error) {
        console.error('Failed to fetch backups:', error);
      } finally {
        loadingBackups.value = false;
      }
    };

    const saveGeneralSettings = async () => {
      loading.value = true;
      try {
        await adminService.updateSettings({ general: generalSettings.value });
        // Show success message
      } catch (error) {
        console.error('Failed to save general settings:', error);
      } finally {
        loading.value = false;
      }
    };

    const saveAppearanceSettings = async () => {
      loading.value = true;
      try {
        await adminService.updateSettings({ appearance: appearanceSettings.value });
        // Update theme in store
        settingsStore.setTheme(appearanceSettings.value.theme);
        // Show success message
      } catch (error) {
        console.error('Failed to save appearance settings:', error);
      } finally {
        loading.value = false;
      }
    };

    const saveNotificationSettings = async () => {
      loading.value = true;
      try {
        await adminService.updateSettings({ notifications: notificationSettings.value });
        // Show success message
      } catch (error) {
        console.error('Failed to save notification settings:', error);
      } finally {
        loading.value = false;
      }
    };

    const saveSecuritySettings = async () => {
      loading.value = true;
      try {
        await adminService.updateSettings({ security: securitySettings.value });
        // Show success message
      } catch (error) {
        console.error('Failed to save security settings:', error);
      } finally {
        loading.value = false;
      }
    };

    const saveBackupSettings = async () => {
      loading.value = true;
      try {
        await adminService.updateSettings({ backup: backupSettings.value });
        // Show success message
      } catch (error) {
        console.error('Failed to save backup settings:', error);
      } finally {
        loading.value = false;
      }
    };

    const handleLogoUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          appearanceSettings.value.logo = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const handleFaviconUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          appearanceSettings.value.favicon = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const createBackup = async () => {
      creatingBackup.value = true;
      try {
        // This would be an actual API call in a real app
        // const response = await adminService.createBackup();
        // backups.value.unshift(response.data);

        // Mock for demonstration
        const newBackup = {
          id: Date.now(),
          fileName: `backup_${new Date().toISOString().replace(/[:.]/g, '_')}.sql`,
          size: 2100000 + Math.floor(Math.random() * 100000),
          createdAt: new Date().toISOString()
        };

        backups.value.unshift(newBackup);
      } catch (error) {
        console.error('Failed to create backup:', error);
      } finally {
        creatingBackup.value = false;
      }
    };

    const downloadBackup = (backup) => {
      // This would be an actual API call in a real app
      // window.location.href = `/api/admin/backups/${backup.id}/download`;

      // Mock for demonstration
      const link = document.createElement('a');
      link.href = '#';
      link.download = backup.fileName;
      link.click();
    };

    const confirmDeleteBackup = (backup) => {
      if (confirm(`هل أنت متأكد من أنك تريد حذف النسخة الاحتياطية "${backup.fileName}"؟`)) {
        deleteBackup(backup.id);
      }
    };

    const deleteBackup = async (backupId) => {
      try {
        // This would be an actual API call in a real app
        // await adminService.deleteBackup(backupId);

        // Mock for demonstration
        const index = backups.value.findIndex(b => b.id === backupId);
        if (index !== -1) {
          backups.value.splice(index, 1);
        }
      } catch (error) {
        console.error('Failed to delete backup:', error);
      }
    };

    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString('ar-SA', options);
    };

    return {
      activeTab,
      loading,
      creatingBackup,
      loadingBackups,
      backups,
      generalSettings,
      appearanceSettings,
      notificationSettings,
      securitySettings,
      backupSettings,
      saveGeneralSettings,
      saveAppearanceSettings,
      saveNotificationSettings,
      saveSecuritySettings,
      saveBackupSettings,
      handleLogoUpload,
      handleFaviconUpload,
      createBackup,
      downloadBackup,
      confirmDeleteBackup,
      formatFileSize,
      formatDate
    };
  }
};
</script>

<style scoped>
.settings-container {
  padding: 1.5rem;
}

.list-group-item {
  border-radius: 0;
  border-left: none;
  border-right: none;
}

.list-group-item:first-child {
  border-top: none;
}

.list-group-item:last-child {
  border-bottom: none;
}

.list-group-item.active {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.form-control-color {
  width: 50px;
  height: 38px;
  padding: 0.375rem;
}

.img-thumbnail {
  max-width: 100%;
  height: auto;
}

[dir="rtl"] .list-group-item {
  border-left: 1px solid rgba(0, 0, 0, 0.125);
  border-right: none;
}
</style>
