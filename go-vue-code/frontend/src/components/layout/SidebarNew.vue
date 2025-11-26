<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-header">
      <router-link to="/" class="sidebar-logo">
        <div class="logo-icon">
          <i class="fas fa-code"></i>
        </div>
        <span v-if="!isCollapsed" class="logo-text">Go-Vue Code</span>
      </router-link>
      <button class="sidebar-toggle" @click="toggleSidebar">
        <i class="fas" :class="isCollapsed ? 'fa-angle-left' : 'fa-angle-right'"></i>
      </button>
    </div>

    <div class="sidebar-menu">
      <template v-for="item in menuItems" :key="item.path">
        <!-- Single Menu Item -->
        <router-link v-if="!item.children" :to="item.path" class="sidebar-menu-item" :class="{ active: isActive(item.path) }">
          <div class="menu-icon">
            <i :class="item.icon"></i>
          </div>
          <span class="menu-text">{{ item.title }}</span>
          <span v-if="item.badge" class="sidebar-badge">{{ item.badge }}</span>
        </router-link>

        <!-- Menu with Sub-items -->
        <div v-else class="sidebar-submenu">
          <a href="#" class="sidebar-menu-item parent-item" :class="{ active: isSubmenuActive(item) }" @click.prevent="toggleSubmenu(item)">
            <div class="menu-icon">
              <i :class="item.icon"></i>
            </div>
            <span class="menu-text">{{ item.title }}</span>
            <i class="fas fa-chevron-down submenu-toggle" :class="{ 'rotate': item.expanded }"></i>
          </a>
          <div v-show="item.expanded" class="submenu-items">
            <router-link v-for="child in item.children" :key="child.path" :to="child.path"
                         class="sidebar-menu-item submenu-item" :class="{ active: isActive(child.path) }">
              <div class="menu-icon">
                <i :class="child.icon"></i>
              </div>
              <span class="menu-text">{{ child.title }}</span>
            </router-link>
          </div>
        </div>
      </template>
    </div>

    <div class="sidebar-footer" v-if="!isCollapsed">
      <div class="user-profile">
        <div class="user-avatar">
          <img v-if="user?.avatar" :src="user.avatar" :alt="user?.firstName">
          <span v-else class="avatar-placeholder">{{ user?.firstName?.charAt(0) }}{{ user?.lastName?.charAt(0) }}</span>
        </div>
        <div class="user-info">
          <h6 class="user-name">{{ user?.firstName }} {{ user?.lastName }}</h6>
          <p class="user-role text-muted small">{{ user?.roles?.[0]?.name || 'مستخدم' }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script>
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'SidebarNew',
  setup() {
    const route = useRoute();
    const authStore = useAuthStore();
    const isCollapsed = ref(false);

    // Initialize menu items with expanded state
    const menuItems = ref([
      {
        title: 'لوحة التحكم',
        path: '/dashboard',
        icon: 'fas fa-tachometer-alt',
        expanded: false
      },
      {
        title: 'المستخدمون',
        icon: 'fas fa-users',
        expanded: false,
        children: [
          {
            title: 'قائمة المستخدمين',
            path: '/admin/users',
            icon: 'fas fa-list',
            permission: 'users.view'
          },
          {
            title: 'إضافة مستخدم',
            path: '/admin/users/create',
            icon: 'fas fa-plus',
            permission: 'users.create'
          }
        ]
      },
      {
        title: 'الأدوار',
        icon: 'fas fa-user-shield',
        expanded: false,
        children: [
          {
            title: 'قائمة الأدوار',
            path: '/admin/roles',
            icon: 'fas fa-list',
            permission: 'roles.view'
          },
          {
            title: 'إضافة دور',
            path: '/admin/roles/create',
            icon: 'fas fa-plus',
            permission: 'roles.create'
          }
        ]
      },
      {
        title: 'الصلاحيات',
        icon: 'fas fa-key',
        expanded: false,
        children: [
          {
            title: 'قائمة الصلاحيات',
            path: '/admin/permissions',
            icon: 'fas fa-list',
            permission: 'permissions.view'
          },
          {
            title: 'إضافة صلاحية',
            path: '/admin/permissions/create',
            icon: 'fas fa-plus',
            permission: 'permissions.create'
          }
        ]
      },
      {
        title: 'التقارير',
        path: '/reports',
        icon: 'fas fa-chart-bar',
        expanded: false,
        permission: 'reports.view'
      },
      {
        title: 'الإعدادات',
        path: '/settings',
        icon: 'fas fa-cog',
        expanded: false
      }
    ]);

    // Filter menu items based on permissions
    const filteredMenuItems = computed(() => {
      return menuItems.value.filter(item => {
        // Check if the item has permission requirement
        if (item.permission && !authStore.hasPermission(item.permission)) {
          return false;
        }

        // Filter children if exist
        if (item.children) {
          item.children = item.children.filter(child => {
            return !child.permission || authStore.hasPermission(child.permission);
          });

          // Only show parent if it has children
          return item.children.length > 0;
        }

        return true;
      });
    });

    const isActive = (path) => {
      return route.path === path;
    };

    const isSubmenuActive = (item) => {
      if (!item.children) return false;
      return item.children.some(child => isActive(child.path));
    };

    const toggleSubmenu = (item) => {
      item.expanded = !item.expanded;
    };

    const toggleSidebar = () => {
      isCollapsed.value = !isCollapsed.value;
    };

    return {
      isCollapsed,
      menuItems: filteredMenuItems,
      user: authStore.user,
      isActive,
      isSubmenuActive,
      toggleSubmenu,
      toggleSidebar
    };
  }
};
</script>

<style scoped>
/* Sidebar Styles */
.sidebar {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: 260px;
  background-color: var(--card-bg);
  border-left: 1px solid var(--border-color);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  overflow-y: auto;
  overflow-x: hidden;
  box-shadow: var(--box-shadow);
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: 70px;
}

/* Sidebar Header */
.sidebar-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: rgba(67, 97, 238, 0.05);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: var(--font-weight-bold);
  font-size: 1.2rem;
  white-space: nowrap;
  transition: var(--transition-fast);
}

.sidebar-logo:hover {
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
  margin-left: 0.75rem;
}

.logo-text {
  font-weight: var(--font-weight-bold);
  color: var(--text-color);
}

.sidebar-toggle {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--border-radius);
  transition: var(--transition-fast);
}

.sidebar-toggle:hover {
  background-color: var(--light-color);
  color: var(--primary-color);
}

.sidebar.collapsed .sidebar-logo span {
  display: none;
}

.sidebar.collapsed .logo-icon {
  margin-left: 0;
}

.sidebar.collapsed .sidebar-toggle {
  transform: rotate(180deg);
}

/* Sidebar Menu */
.sidebar-menu {
  padding: 1rem 0;
  flex: 1;
  overflow-y: auto;
}

.sidebar-menu-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.25rem;
  color: var(--text-color);
  text-decoration: none;
  transition: var(--transition-fast);
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  border-radius: 0;
  margin: 0.25rem 0.75rem;
  border-radius: var(--border-radius);
}

.sidebar-menu-item:hover {
  background-color: var(--light-color);
  color: var(--primary-color);
}

.sidebar-menu-item.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
  font-weight: var(--font-weight-medium);
}

.sidebar-menu-item.active::before {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background-color: var(--primary-color);
  border-top-left-radius: var(--border-radius);
  border-bottom-left-radius: var(--border-radius);
}

.menu-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.75rem;
  font-size: 1rem;
}

.menu-text {
  flex: 1;
  font-weight: var(--font-weight-medium);
}

.sidebar.collapsed .menu-icon {
  margin-left: 0;
}

.sidebar.collapsed .menu-text {
  display: none;
}

.sidebar-badge {
  margin-left: auto;
  background-color: var(--danger-color);
  color: white;
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  border-radius: 1rem;
  font-weight: var(--font-weight-medium);
}

.sidebar.collapsed .sidebar-badge {
  display: none;
}

/* Submenu Styles */
.sidebar-submenu {
  margin-bottom: 0.25rem;
}

.parent-item {
  font-weight: var(--font-weight-medium);
}

.submenu-toggle {
  margin-left: auto;
  transition: transform 0.3s ease;
  font-size: 0.75rem;
}

.submenu-toggle.rotate {
  transform: rotate(180deg);
}

.sidebar.collapsed .submenu-toggle {
  display: none;
}

.submenu-items {
  background-color: rgba(0, 0, 0, 0.02);
  margin: 0.25rem 0;
}

.sidebar.collapsed .submenu-items {
  display: none;
}

.submenu-item {
  padding-right: 3.5rem;
  font-size: 0.9rem;
  margin: 0.125rem 0.75rem;
}

.sidebar.collapsed .submenu-item {
  padding-right: 1rem;
}

/* Sidebar Footer */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  background-color: rgba(0, 0, 0, 0.02);
}

.user-profile {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  margin-left: 0.75rem;
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

.user-info {
  flex: 1;
}

.user-name {
  font-weight: var(--font-weight-medium);
  margin-bottom: 0.125rem;
  font-size: 0.9rem;
}

.user-role {
  margin-bottom: 0;
  font-size: 0.8rem;
}

/* RTL Support */
[dir="rtl"] .sidebar {
  right: auto;
  left: 0;
  border-left: none;
  border-right: 1px solid var(--border-color);
}

[dir="rtl"] .sidebar-menu-item.active::before {
  right: auto;
  left: 0;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  border-top-right-radius: var(--border-radius);
  border-bottom-right-radius: var(--border-radius);
}

[dir="rtl"] .menu-icon {
  margin-left: 0;
  margin-right: 0.75rem;
}

[dir="rtl"] .sidebar.collapsed .menu-icon {
  margin-right: 0;
}

[dir="rtl"] .logo-icon {
  margin-left: 0;
  margin-right: 0.75rem;
}

[dir="rtl"] .sidebar.collapsed .logo-icon {
  margin-right: 0;
}

[dir="rtl"] .sidebar-badge {
  margin-left: 0;
  margin-right: auto;
}

[dir="rtl"] .submenu-toggle {
  margin-left: 0;
  margin-right: auto;
}

[dir="rtl"] .submenu-item {
  padding-right: 1rem;
  padding-left: 3.5rem;
}

[dir="rtl"] .sidebar.collapsed .submenu-item {
  padding-left: 1rem;
}

[dir="rtl"] .user-avatar {
  margin-left: 0;
  margin-right: 0.75rem;
}

[dir="rtl"] .sidebar-toggle {
  transform: rotate(180deg);
}

[dir="rtl"] .sidebar.collapsed .sidebar-toggle {
  transform: rotate(0deg);
}
</style>
