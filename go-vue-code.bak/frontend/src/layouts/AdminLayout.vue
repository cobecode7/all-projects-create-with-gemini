<template>
  <div class="admin-layout">
    <AdminSidebar />
    <div class="admin-content">
      <AdminHeader />
      <div class="admin-main">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import AdminSidebar from '@/components/admin/AdminSidebar.vue';
import AdminHeader from '@/components/admin/AdminHeader.vue';

export default {
  name: 'AdminLayout',
  components: {
    AdminSidebar,
    AdminHeader
  }
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.admin-content {
  flex: 1;
  margin-right: 250px;
  display: flex;
  flex-direction: column;
}

.admin-main {
  flex: 1;
  padding: 20px;
  background-color: #f8f9fa;
}

@media (max-width: 768px) {
  .admin-sidebar {
    width: 70px;
  }

  .admin-content {
    margin-right: 70px;
  }

  .sidebar-header h4,
  .menu-link span {
    display: none;
  }
}
</style>
