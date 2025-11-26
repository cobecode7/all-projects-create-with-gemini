<template>
  <header class="admin-header">
    <div class="header-left">
      <button class="btn btn-link toggle-sidebar" @click="toggleSidebar">
        <i class="fas fa-bars"></i>
      </button>
      <h4 class="page-title">{{ pageTitle }}</h4>
    </div>
    <div class="header-right">
      <div class="user-menu dropdown">
        <button class="btn btn-link dropdown-toggle" type="button" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
          <div class="user-avatar">
            <img :src="user.avatar || '/default-avatar.png'" :alt="user.firstName">
          </div>
          <span class="user-name">{{ user.firstName }} {{ user.lastName }}</span>
        </button>
        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
          <li><a class="dropdown-item" href="#" @click.prevent="goToProfile">
            <i class="fas fa-user"></i> الملف الشخصي
          </a></li>
          <li><a class="dropdown-item" href="#" @click.prevent="goToSettings">
            <i class="fas fa-cog"></i> الإعدادات
          </a></li>
          <li><hr class="dropdown-divider"></li>
          <li><a class="dropdown-item" href="#" @click.prevent="logout">
            <i class="fas fa-sign-out-alt"></i> تسجيل الخروج
          </a></li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'AdminHeader',
  computed: {
    ...mapGetters(['user']),
    pageTitle() {
      return this.$route.meta.title || 'لوحة تحكم المشرفين';
    }
  },
  methods: {
    toggleSidebar() {
      document.querySelector('.admin-sidebar').classList.toggle('collapsed');
      document.querySelector('.admin-content').classList.toggle('expanded');
    },
    goToProfile() {
      this.$router.push('/profile');
    },
    goToSettings() {
      this.$router.push('/settings');
    },
    logout() {
      this.$store.dispatch('logout').then(() => {
        this.$router.push('/login');
      });
    }
  }
};
</script>

<style scoped>
.admin-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 999;
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-sidebar {
  margin-left: 15px;
  color: #343a40;
}

.page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #343a40;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-menu {
  position: relative;
}

.user-menu .btn {
  display: flex;
  align-items: center;
  color: #343a40;
  padding: 0;
}

.user-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  overflow: hidden;
  margin-left: 10px;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-weight: 500;
}

.dropdown-menu {
  min-width: 200px;
}

.dropdown-item {
  display: flex;
  align-items: center;
}

.dropdown-item i {
  width: 20px;
  margin-left: 10px;
}
</style>
