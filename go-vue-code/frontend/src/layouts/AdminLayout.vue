<template>
  <div class="admin-layout">
    <AdminSidebar />
    <div class="admin-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <AdminHeader />
      <div class="admin-main">
        <div class="content-container">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import AdminSidebar from '@/components/admin/AdminSidebar.vue';
import AdminHeader from '@/components/admin/AdminHeader.vue';

export default {
  name: 'AdminLayout',
  components: {
    AdminSidebar,
    AdminHeader
  },
  setup() {
    const isSidebarCollapsed = ref(false);

    return {
      isSidebarCollapsed
    };
  }
};
</script>

<style scoped>
/* Admin Layout */
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--body-bg);
}

.admin-content {
  flex: 1;
  margin-right: 260px;
  display: flex;
  flex-direction: column;
  transition: margin-right 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.admin-content.sidebar-collapsed {
  margin-right: 70px;
}

.admin-main {
  flex: 1;
  padding: 0;
  background-color: var(--body-bg);
  position: relative;
  overflow-y: auto;
}

.content-container {
  padding: 1.5rem;
  min-height: calc(100vh - var(--header-height));
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

/* Responsive Design */
@media (max-width: 992px) {
  .admin-content {
    margin-right: 70px;
  }
  
  .content-container {
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .admin-layout {
    flex-direction: column;
  }
  
  .admin-content {
    margin-right: 0;
    margin-top: 60px;
  }
  
  .content-container {
    padding: 1rem 0.75rem;
  }
}

/* RTL Support */
[dir="rtl"] .admin-content {
  margin-right: 0;
  margin-left: 260px;
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

[dir="rtl"] .admin-content.sidebar-collapsed {
  margin-left: 70px;
  margin-right: 0;
}

@media (max-width: 992px) {
  [dir="rtl"] .admin-content {
    margin-left: 70px;
    margin-right: 0;
  }
}

@media (max-width: 768px) {
  [dir="rtl"] .admin-content {
    margin-left: 0;
    margin-top: 60px;
  }
}
</style>
