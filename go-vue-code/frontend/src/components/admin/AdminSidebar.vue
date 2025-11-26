<template>
  <div class="admin-sidebar">
    <div class="sidebar-header">
      <h4>لوحة تحكم المشرفين</h4>
    </div>
    <ul class="sidebar-menu">
      <li class="menu-item">
        <router-link to="/admin/dashboard" class="menu-link">
          <i class="fas fa-tachometer-alt"></i>
          <span>لوحة التحكم</span>
        </router-link>
      </li>
      <li class="menu-item">
        <router-link to="/admin/users" class="menu-link">
          <i class="fas fa-users"></i>
          <span>المستخدمون</span>
        </router-link>
      </li>
      <li class="menu-item">
        <router-link to="/admin/roles" class="menu-link">
          <i class="fas fa-user-shield"></i>
          <span>الأدوار</span>
        </router-link>
      </li>
      <li class="menu-item">
        <router-link to="/admin/permissions" class="menu-link">
          <i class="fas fa-key"></i>
          <span>الصلاحيات</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'AdminSidebar'
};
</script>

<style scoped>
.admin-sidebar {
  background-color: #343a40;
  color: #fff;
  height: 100vh;
  position: fixed;
  width: 250px;
  overflow-y: auto;
  z-index: 1000;
  transition: all 0.3s;
}

.sidebar-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #454d55;
}

.sidebar-header h4 {
  margin: 0;
  font-size: 18px;
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  border-bottom: 1px solid #454d55;
}

.menu-link {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: #adb5bd;
  text-decoration: none;
  transition: all 0.3s;
}

.menu-link:hover {
  background-color: #454d55;
  color: #fff;
}

.menu-link.router-link-active {
  background-color: #007bff;
  color: #fff;
}

.menu-link i {
  width: 20px;
  margin-left: 10px;
  text-align: center;
}

.menu-link span {
  font-size: 16px;
}
</style>
