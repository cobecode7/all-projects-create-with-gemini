<template>
  <div class="dashboard-container">
    <div class="dashboard-header mb-4">
      <h1 class="dashboard-title">لوحة التحكم</h1>
      <p class="dashboard-subtitle">مرحباً بك في لوحة التحكم الرئيسية</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card stat-card-primary">
        <div class="stat-card-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.users }}</h3>
            <p class="stat-label">المستخدمون</p>
          </div>
          <div class="stat-icon">
            <i class="fas fa-users"></i>
          </div>
        </div>
        <div class="stat-progress">
          <div class="progress-bar" style="width: 75%"></div>
        </div>
      </div>

      <div class="stat-card stat-card-success">
        <div class="stat-card-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.roles }}</h3>
            <p class="stat-label">الأدوار</p>
          </div>
          <div class="stat-icon">
            <i class="fas fa-shield-alt"></i>
          </div>
        </div>
        <div class="stat-progress">
          <div class="progress-bar" style="width: 50%"></div>
        </div>
      </div>

      <div class="stat-card stat-card-info">
        <div class="stat-card-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.permissions }}</h3>
            <p class="stat-label">الصلاحيات</p>
          </div>
          <div class="stat-icon">
            <i class="fas fa-key"></i>
          </div>
        </div>
        <div class="stat-progress">
          <div class="progress-bar" style="width: 30%"></div>
        </div>
      </div>

      <div class="stat-card stat-card-warning">
        <div class="stat-card-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.activeUsers }}</h3>
            <p class="stat-label">المستخدمون النشطون</p>
          </div>
          <div class="stat-icon">
            <i class="fas fa-user-check"></i>
          </div>
        </div>
        <div class="stat-progress">
          <div class="progress-bar" style="width: 85%"></div>
        </div>
      </div>
    </div>

    <div class="dashboard-content mt-4">
      <div class="row">
        <div class="col-lg-6 mb-4">
          <div class="content-card">
            <div class="content-card-header">
              <h5 class="content-card-title">المستخدمون الجدد</h5>
              <router-link to="/admin/users" class="btn btn-sm btn-outline-primary">عرض الكل</router-link>
            </div>
            <div class="content-card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">جاري التحميل...</span>
                </div>
              </div>
              <div v-else-if="newUsers.length === 0" class="empty-state py-4">
                <i class="fas fa-users-slash fa-3x text-muted mb-3"></i>
                <p class="text-muted">لا يوجد مستخدمون جدد</p>
              </div>
              <div v-else class="user-list">
                <div v-for="user in newUsers" :key="user.id" class="user-item">
                  <div class="user-avatar">
                    <img v-if="user.avatar" :src="user.avatar" :alt="user.firstName">
                    <span v-else class="avatar-placeholder">{{ user.firstName.charAt(0) }}{{ user.lastName.charAt(0) }}</span>
                  </div>
                  <div class="user-info">
                    <h6 class="user-name">{{ user.firstName }} {{ user.lastName }}</h6>
                    <p class="user-email text-muted small">{{ user.email }}</p>
                  </div>
                  <div class="user-date">
                    <small class="text-muted">{{ formatDate(user.createdAt) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6 mb-4">
          <div class="content-card">
            <div class="content-card-header">
              <h5 class="content-card-title">نشاط المستخدم</h5>
              <div class="btn-group btn-group-sm" role="group">
                <button type="button" class="btn btn-outline-primary active">يوم</button>
                <button type="button" class="btn btn-outline-primary">أسبوع</button>
                <button type="button" class="btn btn-outline-primary">شهر</button>
              </div>
            </div>
            <div class="content-card-body">
              <canvas ref="activityChart" height="200"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()
const loading = ref(true)
const stats = ref({
  users: 0,
  roles: 0,
  permissions: 0,
  activeUsers: 0
})
const newUsers = ref([])
const activityChart = ref(null)

// Mock data for demonstration
onMounted(async () => {
  try {
    // In a real application, you would fetch this data from your API
    // const response = await axios.get('/api/dashboard/stats')

    // Mock data for demonstration
    setTimeout(() => {
      stats.value = {
        users: 124,
        roles: 3,
        permissions: 12,
        activeUsers: 87
      }

      newUsers.value = [
        {
          id: 1,
          firstName: 'أحمد',
          lastName: 'محمد',
          email: 'ahmed@example.com',
          createdAt: new Date(Date.now() - 86400000 * 1).toISOString()
        },
        {
          id: 2,
          firstName: 'فاطمة',
          lastName: 'علي',
          email: 'fatima@example.com',
          createdAt: new Date(Date.now() - 86400000 * 2).toISOString()
        },
        {
          id: 3,
          firstName: 'عمر',
          lastName: 'حسن',
          email: 'omar@example.com',
          createdAt: new Date(Date.now() - 86400000 * 3).toISOString()
        }
      ]

      loading.value = false
    }, 1000)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    loading.value = false
  }
})

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ar-SA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
/* Dashboard Container */
.dashboard-container {
  padding: 1.5rem;
}

/* Dashboard Header */
.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-title {
  font-weight: var(--font-weight-bold);
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

.dashboard-subtitle {
  color: var(--text-muted);
  margin-bottom: 0;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow);
  overflow: hidden;
  transition: var(--transition-fast);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--box-shadow-lg);
}

.stat-card-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: var(--font-weight-bold);
  margin-bottom: 0.25rem;
}

.stat-label {
  color: var(--text-muted);
  margin-bottom: 0;
  font-weight: var(--font-weight-medium);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-card-primary .stat-icon {
  background-color: var(--primary-color);
}

.stat-card-success .stat-icon {
  background-color: var(--success-color);
}

.stat-card-info .stat-icon {
  background-color: var(--info-color);
}

.stat-card-warning .stat-icon {
  background-color: var(--warning-color);
}

.stat-progress {
  height: 4px;
  background-color: var(--light-color);
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--info-color));
}

.stat-card-primary .progress-bar {
  background: linear-gradient(90deg, var(--primary-color), #3a56d4);
}

.stat-card-success .progress-bar {
  background: linear-gradient(90deg, var(--success-color), #00d68f);
}

.stat-card-info .progress-bar {
  background: linear-gradient(90deg, var(--info-color), #2c7ae4);
}

.stat-card-warning .progress-bar {
  background: linear-gradient(90deg, var(--warning-color), #e6aa00);
}

/* Content Cards */
.content-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow);
  height: 100%;
  transition: var(--transition-fast);
}

.content-card:hover {
  box-shadow: var(--box-shadow-lg);
}

.content-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.content-card-title {
  font-weight: var(--font-weight-semibold);
  margin-bottom: 0;
  color: var(--text-color);
}

.content-card-body {
  padding: 1.5rem;
}

/* User List */
.user-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  transition: var(--transition-fast);
}

.user-item:hover {
  background-color: var(--light-color);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-left: 1rem;
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
  margin-bottom: 0.25rem;
}

.user-email {
  margin-bottom: 0;
}

.user-date {
  font-size: 0.85rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem 1rem;
}

/* RTL Support */
[dir="rtl"] .user-avatar {
  margin-left: 0;
  margin-right: 1rem;
}

[dir="rtl"] .stat-card-content {
  flex-direction: row-reverse;
}

[dir="rtl"] .content-card-header {
  flex-direction: row-reverse;
}

[dir="rtl"] .user-item {
  flex-direction: row-reverse;
}

[dir="rtl"] .user-info {
  text-align: right;
}

[dir="rtl"] .user-date {
  text-align: left;
}
</style>
