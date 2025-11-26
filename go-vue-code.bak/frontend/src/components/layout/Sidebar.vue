<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-header">
      <router-link to="/" class="sidebar-logo">
        <i class="fas fa-code"></i>
        <span v-if="!isCollapsed">Go-Vue Code</span>
      </router-link>
    </div>

    <div class="sidebar-menu">
      <template v-for="item in menuItems" :key="item.path">
        <!-- Single Menu Item -->
        <router-link v-if="!item.children" :to="item.path" class="sidebar-menu-item" :class="{ active: isActive(item.path) }">
          <i :class="item.icon"></i>
          <span>{{ item.title }}</span>
          <span v-if="item.badge" class="sidebar-badge">{{ item.badge }}</span>
        </router-link>

        <!-- Menu with Sub-items -->
        <div v-else class="sidebar-submenu">
          <a href="#" class="sidebar-menu-item" :class="{ active: isSubmenuActive(item) }" @click.prevent="toggleSubmenu(item)">
            <i :class="item.icon"></i>
            <span>{{ item.title }}</span>
            <i class="fas fa-chevron-down submenu-toggle" :class="{ 'rotate': item.expanded }"></i>
          </a>
          <div v-show="item.expanded" class="submenu-items">
            <router-link v-for="child in item.children" :key="child.path" :to="child.path" 
                         class="sidebar-menu-item submenu-item" :class="{ active: isActive(child.path) }">
              <i :class="child.icon"></i>
              <span>{{ child.title }}</span>
            </router-link>
          </div>
        </div>
      </template>
    </div>
  </aside>
</template>

<script>
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'Sidebar',
  setup() {
    const route = useRoute();
    const authStore = useAuthStore();
    const isCollapsed = computed(() => false); // This will be managed by the settings store

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

    return {
      isCollapsed,
      menuItems: filteredMenuItems,
      isActive,
      isSubmenuActive,
      toggleSubmenu
    };
  }
};
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: 250px;
  background-color: var(--card-bg);
  border-left: 1px solid var(--border-color);
  transition: width 0.3s ease;
  z-index: 1000;
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  color: var(--primary-color);
  text-decoration: none;
  font-weight: bold;
  font-size: 1.2rem;
  white-space: nowrap;
}

.sidebar-logo i {
  margin-left: 0.5rem;
  font-size: 1.5rem;
}

.sidebar.collapsed .sidebar-logo span {
  display: none;
}

.sidebar-menu {
  padding: 1rem 0;
}

.sidebar-menu-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: var(--text-color);
  text-decoration: none;
  transition: background-color 0.3s ease;
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-menu-item:hover {
  background-color: var(--light-color);
}

.sidebar-menu-item.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
}

.sidebar-menu-item.active::before {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background-color: var(--primary-color);
}

.sidebar-menu-item i {
  width: 1.5rem;
  text-align: center;
  margin-left: 0.75rem;
  font-size: 1rem;
}

.sidebar.collapsed .sidebar-menu-item i {
  margin-left: 0;
}

.sidebar.collapsed .sidebar-menu-item span {
  display: none;
}

.sidebar-badge {
  margin-left: auto;
  background-color: var(--danger-color);
  color: white;
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  border-radius: 1rem;
}

.sidebar.collapsed .sidebar-badge {
  display: none;
}

.sidebar-submenu {
  margin-bottom: 0.5rem;
}

.submenu-toggle {
  margin-left: auto;
  transition: transform 0.3s ease;
}

.submenu-toggle.rotate {
  transform: rotate(180deg);
}

.sidebar.collapsed .submenu-toggle {
  display: none;
}

.submenu-items {
  background-color: rgba(0, 0, 0, 0.05);
}

.sidebar.collapsed .submenu-items {
  display: none;
}

.submenu-item {
  padding-right: 3.5rem;
  font-size: 0.9rem;
}

.sidebar.collapsed .submenu-item {
  padding-right: 1rem;
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
}

[dir="rtl"] .sidebar-menu-item i {
  margin-left: 0;
  margin-right: 0.75rem;
}

[dir="rtl"] .sidebar.collapsed .sidebar-menu-item i {
  margin-right: 0;
}

[dir="rtl"] .sidebar-logo i {
  margin-left: 0;
  margin-right: 0.5rem;
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
</style>
