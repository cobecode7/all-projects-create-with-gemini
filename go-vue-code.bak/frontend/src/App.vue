<template>
  <div class="container-fluid">
    <header class="py-3 mb-4 border-bottom">
      <div class="container d-flex flex-wrap justify-content-between">
        <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
          <span class="fs-4">Go Vue Auth</span>
        </a>
        <ul class="nav nav-pills">
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link">تسجيل الدخول</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link to="/register" class="nav-link">إنشاء حساب</router-link>
          </li>
          <li class="nav-item dropdown" v-if="isLoggedIn">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              {{ user?.firstName }} {{ user?.lastName }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><router-link to="/profile" class="dropdown-item">الملف الشخصي</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#" @click="logout">تسجيل الخروج</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </header>

    <main>
      <div class="container">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <footer class="py-3 my-4 border-top">
      <div class="container text-center">
        <span class="text-muted">© 2023 Go Vue Auth. جميع الحقوق محفوظة.</span>
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
.rtl {
  direction: rtl;
  text-align: right;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
