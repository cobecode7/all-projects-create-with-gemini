<template>
  <header class="header">
    <div class="d-flex align-items-center">
      <button class="sidebar-toggle me-3" @click="toggleSidebar">
        <i class="fas fa-bars"></i>
      </button>
      <h5 class="header-title mb-0">{{ pageTitle }}</h5>
    </div>

    <div class="header-actions">
      <!-- Language Switcher -->
      <div class="dropdown me-3">
        <button class="header-action dropdown-toggle" type="button" data-bs-toggle="dropdown">
          <i class="fas fa-globe"></i>
          <span class="d-none d-md-inline">{{ currentLanguage }}</span>
        </button>
        <ul class="dropdown-menu">
          <li v-for="lang in availableLanguages" :key="lang.code">
            <a class="dropdown-item" href="#" @click.prevent="changeLanguage(lang.code)">
              {{ lang.name }}
            </a>
          </li>
        </ul>
      </div>

      <!-- Theme Switcher -->
      <button class="header-action me-3" @click="toggleTheme">
        <i :class="isDarkTheme ? 'fas fa-sun' : 'fas fa-moon'"></i>
      </button>

      <!-- Notifications -->
      <div class="dropdown me-3">
        <button class="header-action dropdown-toggle position-relative" type="button" data-bs-toggle="dropdown">
          <i class="fas fa-bell"></i>
          <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
        </button>
        <div class="dropdown-menu dropdown-menu-end notification-dropdown">
          <div class="dropdown-header d-flex justify-content-between align-items-center">
            <span>الإشعارات</span>
            <button class="btn btn-sm btn-link" @click="markAllAsRead" v-if="unreadCount > 0">
              تحديد الكل كمقروء
            </button>
          </div>
          <div class="dropdown-divider"></div>
          <div v-if="loading" class="text-center py-3">
            <div class="spinner-border spinner-border-sm" role="status">
              <span class="visually-hidden">جاري التحميل...</span>
            </div>
          </div>
          <div v-else-if="notifications.length === 0" class="text-center py-3">
            لا توجد إشعارات
          </div>
          <div v-else>
            <div v-for="notification in recentNotifications" :key="notification.id" 
                 class="notification-item" :class="{ 'unread': !notification.read }">
              <div class="d-flex">
                <div class="notification-icon me-3">
                  <i :class="getNotificationIcon(notification.type)"></i>
                </div>
                <div class="notification-content flex-grow-1">
                  <div class="notification-title">{{ notification.title }}</div>
                  <div class="notification-message text-muted">{{ notification.message }}</div>
                  <div class="notification-time text-muted">{{ formatTime(notification.createdAt) }}</div>
                </div>
                <button class="btn btn-sm btn-icon" @click="deleteNotification(notification.id)">
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>
            <div class="dropdown-divider"></div>
            <div class="text-center py-2">
              <router-link to="/notifications" class="btn btn-sm btn-link">عرض جميع الإشعارات</router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- User Dropdown -->
      <div class="dropdown">
        <button class="user-dropdown-toggle" type="button" data-bs-toggle="dropdown">
          <img v-if="user.avatar" :src="user.avatar" alt="User Avatar" class="user-avatar">
          <div v-else class="user-avatar bg-primary text-white d-flex align-items-center justify-content-center">
            {{ user.firstName.charAt(0) }}{{ user.lastName.charAt(0) }}
          </div>
          <span class="d-none d-md-inline me-2">{{ userName }}</span>
          <i class="fas fa-chevron-down"></i>
        </button>
        <div class="user-dropdown-menu">
          <div class="dropdown-header">
            {{ userName }}
            <div class="text-muted small">{{ user.email }}</div>
          </div>
          <div class="dropdown-divider"></div>
          <router-link to="/profile" class="user-dropdown-item">
            <i class="fas fa-user me-2"></i> الملف الشخصي
          </router-link>
          <router-link to="/settings" class="user-dropdown-item">
            <i class="fas fa-cog me-2"></i> الإعدادات
          </router-link>
          <div class="dropdown-divider"></div>
          <button class="user-dropdown-item" @click="logout">
            <i class="fas fa-sign-out-alt me-2"></i> تسجيل الخروج
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useSettingsStore } from '@/stores/settings';
import { useNotificationsStore } from '@/stores/notifications';

export default {
  name: 'Header',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();
    const settingsStore = useSettingsStore();
    const notificationsStore = useNotificationsStore();

    const pageTitle = computed(() => {
      return route.meta.title || 'لوحة التحكم';
    });

    const user = computed(() => authStore.user || {});
    const userName = computed(() => {
      return user.value ? `${user.value.firstName} ${user.value.lastName}` : '';
    });

    const isDarkTheme = computed(() => settingsStore.isDarkTheme);
    const currentLanguage = computed(() => {
      const lang = settingsStore.language;
      return lang === 'ar' ? 'العربية' : 'English';
    });

    const availableLanguages = [
      { code: 'ar', name: 'العربية' },
      { code: 'en', name: 'English' }
    ];

    const notifications = computed(() => notificationsStore.notifications);
    const unreadCount = computed(() => notificationsStore.unreadCount);
    const recentNotifications = computed(() => notificationsStore.recentNotifications);
    const loading = computed(() => notificationsStore.loading);

    const toggleSidebar = () => {
      settingsStore.toggleSidebar();
    };

    const toggleTheme = () => {
      settingsStore.toggleTheme();
    };

    const changeLanguage = (lang) => {
      settingsStore.setLanguage(lang);
    };

    const markAllAsRead = async () => {
      await notificationsStore.markAllAsRead();
    };

    const deleteNotification = async (id) => {
      await notificationsStore.deleteNotification(id);
    };

    const logout = async () => {
      await authStore.logout();
      router.push('/login');
    };

    const getNotificationIcon = (type) => {
      const icons = {
        info: 'fas fa-info-circle text-info',
        success: 'fas fa-check-circle text-success',
        warning: 'fas fa-exclamation-triangle text-warning',
        error: 'fas fa-times-circle text-danger'
      };
      return icons[type] || icons.info;
    };

    const formatTime = (dateString) => {
      const date = new Date(dateString);
      const now = new Date();
      const diff = Math.floor((now - date) / 1000); // Difference in seconds

      if (diff < 60) return 'الآن';
      if (diff < 3600) return `${Math.floor(diff / 60)} دقيقة`;
      if (diff < 86400) return `${Math.floor(diff / 3600)} ساعة`;
      if (diff < 604800) return `${Math.floor(diff / 86400)} يوم`;

      return date.toLocaleDateString('ar-SA');
    };

    return {
      pageTitle,
      user,
      userName,
      isDarkTheme,
      currentLanguage,
      availableLanguages,
      notifications,
      unreadCount,
      recentNotifications,
      loading,
      toggleSidebar,
      toggleTheme,
      changeLanguage,
      markAllAsRead,
      deleteNotification,
      logout,
      getNotificationIcon,
      formatTime
    };
  }
};
</script>

<style scoped>
.header {
  padding: 0 1.5rem;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.sidebar-toggle {
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--border-radius);
}

.sidebar-toggle:hover {
  background-color: var(--light-color);
}

.header-action {
  background: none;
  border: none;
  color: var(--text-color);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--border-radius);
  position: relative;
}

.header-action:hover {
  background-color: var(--light-color);
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: var(--danger-color);
  color: white;
  font-size: 0.7rem;
  width: 1.2rem;
  height: 1.2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-dropdown-toggle {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--border-radius);
}

.user-dropdown-toggle:hover {
  background-color: var(--light-color);
}

.user-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: cover;
}

.notification-dropdown {
  width: 350px;
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-color);
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item.unread {
  background-color: var(--light-color);
}

.notification-icon {
  font-size: 1.2rem;
}

.notification-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.notification-message {
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.notification-time {
  font-size: 0.8rem;
}

.btn-icon {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: var(--border-radius);
}

.btn-icon:hover {
  color: var(--text-color);
}
</style>
