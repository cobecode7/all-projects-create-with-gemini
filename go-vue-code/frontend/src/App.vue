<template>
  <div class="app-wrapper">
    <header class="app-header">
      <div class="app-container d-flex flex-wrap justify-content-between align-items-center">
        <router-link to="/" class="app-logo d-flex align-items-center text-decoration-none">
          <div class="logo-icon me-2">
            <i class="fas fa-code"></i>
          </div>
          <span class="logo-text">Go Vue Auth</span>
        </router-link>
        
        <nav class="app-nav">
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link">تسجيل الدخول</router-link>
            <router-link to="/register" class="nav-link nav-link-accent">إنشاء حساب</router-link>
          </template>
          <div class="nav-dropdown dropdown" v-else>
            <button class="nav-link dropdown-toggle d-flex align-items-center" type="button" data-bs-toggle="dropdown">
              <div class="user-avatar me-2">
                <img v-if="user?.avatar" :src="user.avatar" :alt="user?.firstName">
                <span v-else class="avatar-placeholder">{{ user?.firstName?.charAt(0) }}{{ user?.lastName?.charAt(0) }}</span>
              </div>
              <span class="user-name d-none d-md-inline">{{ user?.firstName }} {{ user?.lastName }}</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><router-link to="/profile" class="dropdown-item"><i class="fas fa-user ms-2"></i> الملف الشخصي</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#" @click="logout"><i class="fas fa-sign-out-alt ms-2"></i> تسجيل الخروج</a></li>
            </ul>
          </div>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <div class="app-container">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <footer class="app-footer">
      <div class="app-container text-center">
        <span class="text-muted">© {{ new Date().getFullYear() }} Go Vue Auth. جميع الحقوق محفوظة.</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)

onMounted(() => {
  // Check if user is already logged in
  authStore.checkAuth()
})

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style>
/* App Layout Styles */
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--body-bg);
  font-family: var(--font-family);
  color: var(--text-color);
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Header Styles */
.app-header {
  padding: 1rem 0;
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--box-shadow);
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-logo {
  display: flex;
  align-items: center;
  font-weight: var(--font-weight-bold);
  font-size: 1.5rem;
  color: var(--primary-color);
  transition: var(--transition-fast);
}

.app-logo:hover {
  opacity: 0.8;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background-color: var(--primary-color);
  color: white;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.logo-text {
  font-weight: var(--font-weight-bold);
  color: var(--text-color);
}

/* Navigation Styles */
.app-nav {
  display: flex;
  align-items: center;
}

.nav-link {
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  color: var(--text-color);
  text-decoration: none;
  border-radius: var(--border-radius);
  transition: var(--transition-fast);
  font-weight: var(--font-weight-medium);
}

.nav-link:hover {
  background-color: var(--light-color);
  color: var(--primary-color);
}

.nav-link-accent {
  background-color: var(--primary-color);
  color: white;
}

.nav-link-accent:hover {
  background-color: var(--primary-hover);
  color: white;
}

.nav-dropdown .dropdown-toggle::after {
  margin-right: 0.5rem;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid var(--border-color);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: var(--primary-color);
  color: white;
  font-weight: var(--font-weight-medium);
}

.user-name {
  font-weight: var(--font-weight-medium);
}

/* Main Content Styles */
.app-main {
  flex: 1;
  padding: 2rem 0;
}

/* Footer Styles */
.app-footer {
  padding: 1.5rem 0;
  border-top: 1px solid var(--border-color);
  background-color: var(--card-bg);
  margin-top: auto;
}

/* Transition Effects */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* RTL Support */
[dir="rtl"] .app-logo {
  flex-direction: row-reverse;
}

[dir="rtl"] .logo-icon {
  margin-right: 0;
  margin-left: 0.5rem;
}

[dir="rtl"] .nav-link {
  margin-right: 0;
  margin-left: 0.5rem;
}

[dir="rtl"] .user-avatar {
  margin-right: 0;
  margin-left: 0.5rem;
}

[dir="rtl"] .nav-dropdown .dropdown-toggle::after {
  margin-right: 0;
  margin-left: 0.5rem;
}

[dir="rtl"] .dropdown-menu.dropdown-menu-end {
  right: auto;
  left: 0;
}

[dir="rtl"] .dropdown-item i {
  margin-right: 0;
  margin-left: 0.5rem;
}
</style>
