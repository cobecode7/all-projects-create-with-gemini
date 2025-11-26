<template>
  <div class="admin-dashboard">
    <div class="page-header">
      <h1>لوحة تحكم المشرفين</h1>
    </div>

    <div class="dashboard-stats">
      <div class="row">
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-users"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.totalUsers }}</h3>
              <p>إجمالي المستخدمين</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-user-shield"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.totalRoles }}</h3>
              <p>إجمالي الأدوار</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="stat-card">
            <div class="stat-icon">
              <i class="fas fa-key"></i>
            </div>
            <div class="stat-content">
              <h3>{{ stats.totalPermissions }}</h3>
              <p>إجمالي الصلاحيات</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5>المستخدمون النشطون حديثاً</h5>
            </div>
            <div class="card-body">
              <div class="user-list">
                <div v-for="user in recentUsers" :key="user.id" class="user-item">
                  <div class="user-avatar">
                    <img :src="user.avatar || '/default-avatar.png'" :alt="user.firstName">
                  </div>
                  <div class="user-info">
                    <h6>{{ user.firstName }} {{ user.lastName }}</h6>
                    <p>{{ user.email }}</p>
                  </div>
                  <div class="user-status">
                    <span :class="['badge', user.active ? 'badge-success' : 'badge-danger']">
                      {{ user.active ? 'نشط' : 'غير نشط' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5>الأدوار والصلاحيات</h5>
            </div>
            <div class="card-body">
              <div class="role-list">
                <div v-for="role in rolesWithPermissions" :key="role.id" class="role-item">
                  <h6>{{ role.name }}</h6>
                  <p class="role-description">{{ role.description }}</p>
                  <div class="permission-count">
                    <span>{{ role.permissions.length }} صلاحية</span>
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
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        totalUsers: 0,
        totalRoles: 0,
        totalPermissions: 0
      },
      recentUsers: [],
      rolesWithPermissions: []
    };
  },
  created() {
    this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
      try {
        // Get stats
        const [usersResponse, rolesResponse, permissionsResponse] = await Promise.all([
          axios.get('/api/admin/users?limit=5'),
          axios.get('/api/admin/roles?limit=10'),
          axios.get('/api/admin/permissions?limit=1')
        ]);

        this.stats.totalUsers = usersResponse.data.total;
        this.stats.totalRoles = rolesResponse.data.total;
        this.stats.totalPermissions = permissionsResponse.data.total;

        // Get recent users
        this.recentUsers = usersResponse.data.users;

        // Get roles with permissions
        this.rolesWithPermissions = rolesResponse.data.roles;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        this.$toast.error('فشل في جلب بيانات لوحة التحكم');
      }
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.dashboard-stats {
  margin-bottom: 30px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 15px;
}

.stat-icon i {
  font-size: 24px;
  color: #007bff;
}

.stat-content h3 {
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 5px;
}

.stat-content p {
  margin: 0;
  color: #6c757d;
}

.card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.card-header {
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h5 {
  margin: 0;
  font-weight: 600;
}

.card-body {
  padding: 20px;
}

.user-list {
  max-height: 300px;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.user-item:last-child {
  border-bottom: none;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-left: 15px;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-info h6 {
  margin: 0 0 3px;
  font-weight: 600;
}

.user-info p {
  margin: 0;
  font-size: 14px;
  color: #6c757d;
}

.badge {
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 12px;
}

.badge-success {
  background-color: #28a745;
  color: white;
}

.badge-danger {
  background-color: #dc3545;
  color: white;
}

.role-list {
  max-height: 300px;
  overflow-y: auto;
}

.role-item {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.role-item:last-child {
  border-bottom: none;
}

.role-item h6 {
  margin: 0 0 5px;
  font-weight: 600;
}

.role-description {
  margin: 0 0 5px;
  font-size: 14px;
  color: #6c757d;
}

.permission-count {
  font-size: 14px;
  color: #007bff;
}
</style>
