<template>
  <div class="dashboard-container">
    <div class="dashboard-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-6">
          <h1 class="dashboard-title">لوحة التحكم</h1>
          <p class="dashboard-subtitle">مرحباً بك في لوحة التحكم الرئيسية</p>
        </div>
        <div class="col-md-6 text-md-end">
          <div class="d-flex gap-2 justify-content-md-end">
            <button class="btn btn-outline-primary">
              <i class="bi bi-download me-2"></i>
              تصدير التقرير
            </button>
            <button class="btn btn-primary">
              <i class="bi bi-plus-circle me-2"></i>
              إضافة مستخدم جديد
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card stat-card-primary">
        <div class="stat-card-content">
          <div class="stat-info">
            <h3 class="stat-value">{{ stats.users }}</h3>
            <p class="stat-label">المستخدمون</p>
            <div class="stat-change positive">
              <i class="bi bi-arrow-up"></i>
              <span>12% من الشهر الماضي</span>
            </div>
          </div>
          <div class="stat-icon">
            <i class="bi bi-people"></i>
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
            <div class="stat-change positive">
              <i class="bi bi-arrow-up"></i>
              <span>5% من الشهر الماضي</span>
            </div>
          </div>
          <div class="stat-icon">
            <i class="bi bi-shield-check"></i>
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
            <div class="stat-change positive">
              <i class="bi bi-arrow-up"></i>
              <span>8% من الشهر الماضي</span>
            </div>
          </div>
          <div class="stat-icon">
            <i class="bi bi-key"></i>
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
            <div class="stat-change positive">
              <i class="bi bi-arrow-up"></i>
              <span>15% من الشهر الماضي</span>
            </div>
          </div>
          <div class="stat-icon">
            <i class="bi bi-person-check"></i>
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
                <i class="bi bi-people-slash fa-3x text-muted mb-3"></i>
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
                  <div class="user-actions">
                    <button class="btn btn-sm btn-outline-primary me-1">
                      <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary">
                      <i class="bi bi-three-dots-vertical"></i>
                    </button>
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
              <div class="activity-chart-container">
                <canvas ref="activityChart" height="200"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-lg-8 mb-4">
          <div class="content-card">
            <div class="content-card-header">
              <h5 class="content-card-title">آخر الأنشطة</h5>
              <router-link to="/admin/activities" class="btn btn-sm btn-outline-primary">عرض الكل</router-link>
            </div>
            <div class="content-card-body">
              <div class="activity-timeline">
                <div class="timeline-item" v-for="(activity, index) in recentActivities" :key="index">
                  <div class="timeline-marker" :class="activity.type">
                    <i :class="activity.icon"></i>
                  </div>
                  <div class="timeline-content">
                    <h6 class="timeline-title">{{ activity.title }}</h6>
                    <p class="timeline-description">{{ activity.description }}</p>
                    <small class="timeline-date">{{ formatDate(activity.timestamp) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4 mb-4">
          <div class="content-card">
            <div class="content-card-header">
              <h5 class="content-card-title">مستخدمو النظام</h5>
              <button class="btn btn-sm btn-outline-primary">
                <i class="bi bi-arrow-clockwise"></i>
              </button>
            </div>
            <div class="content-card-body">
              <div class="system-users">
                <div class="user-status-item" v-for="(userStatus, index) in systemUsers" :key="index">
                  <div class="user-status-avatar">
                    <img v-if="userStatus.avatar" :src="userStatus.avatar" :alt="userStatus.name">
                    <span v-else class="avatar-placeholder">{{ userStatus.name.charAt(0) }}</span>
                  </div>
                  <div class="user-status-info">
                    <h6 class="user-status-name">{{ userStatus.name }}</h6>
                    <p class="user-status-role text-muted small">{{ userStatus.role }}</p>
                  </div>
                  <div class="user-status-indicator" :class="userStatus.status">
                    <span class="visually-hidden">{{ userStatus.status }}</span>
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
const recentActivities = ref([])
const systemUsers = ref([])

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

      recentActivities.value = [
        {
          title: 'تم إنشاء مستخدم جديد',
          description: 'قام أحمد محمد بإنشاء حساب جديد',
          type: 'success',
          icon: 'bi bi-person-plus',
          timestamp: new Date(Date.now() - 86400000 * 0.5).toISOString()
        },
        {
          title: 'تحديث صلاحيات',
          description: 'تم تحديث صلاحيات دور المشرف',
          type: 'info',
          icon: 'bi bi-shield-check',
          timestamp: new Date(Date.now() - 86400000 * 1).toISOString()
        },
        {
          title: 'حذف مستخدم',
          description: 'تم حذف مستخدم غير نشط',
          type: 'danger',
          icon: 'bi bi-person-dash',
          timestamp: new Date(Date.now() - 86400000 * 2).toISOString()
        },
        {
          title: 'تسجيل دخول',
          description: 'قام فاطمة علي بتسجيل الدخول',
          type: 'primary',
          icon: 'bi bi-box-arrow-in-right',
          timestamp: new Date(Date.now() - 86400000 * 3).toISOString()
        }
      ]

      systemUsers.value = [
        {
          name: 'أحمد محمد',
          role: 'مدير النظام',
          status: 'online',
          avatar: null
        },
        {
          name: 'فاطمة علي',
          role: 'مشرف',
          status: 'online',
          avatar: null
        },
        {
          name: 'عمر حسن',
          role: 'مستخدم',
          status: 'away',
          avatar: null
        },
        {
          name: 'سارة أحمد',
          role: 'مستخدم',
          status: 'offline',
          avatar: null
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
  position: relative;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--box-shadow-lg);
}

.stat-card-content {
  display: flex;
  align-items: flex-start;
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
  margin-bottom: 0.5rem;
  font-weight: var(--font-weight-medium);
}

.stat-change {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  font-weight: var(--font-weight-medium);
}

.stat-change.positive {
  color: var(--success-color);
}

.stat-change.negative {
  color: var(--danger-color);
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
  flex-shrink: 0;
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
  min-width: 0;
}

.user-name {
  font-weight: var(--font-weight-medium);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  margin-bottom: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-date {
  font-size: 0.85rem;
  white-space: nowrap;
}

.user-actions {
  display: flex;
  gap: 0.25rem;
}

/* Activity Timeline */
.activity-timeline {
  position: relative;
  padding-left: 1.5rem;
}

.timeline-item {
  position: relative;
  padding-bottom: 1.5rem;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 2rem;
  left: -0.75rem;
  height: calc(100% - 2rem);
  width: 2px;
  background-color: var(--border-color);
}

.timeline-marker {
  position: absolute;
  top: 0;
  left: -1.5rem;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.8rem;
}

.timeline-marker.primary {
  background-color: var(--primary-color);
}

.timeline-marker.success {
  background-color: var(--success-color);
}

.timeline-marker.info {
  background-color: var(--info-color);
}

.timeline-marker.warning {
  background-color: var(--warning-color);
}

.timeline-marker.danger {
  background-color: var(--danger-color);
}

.timeline-content {
  padding-left: 0.5rem;
}

.timeline-title {
  font-weight: var(--font-weight-medium);
  margin-bottom: 0.25rem;
}

.timeline-description {
  color: var(--text-muted);
  margin-bottom: 0.25rem;
  font-size: 0.9rem;
}

.timeline-date {
  color: var(--text-muted);
  font-size: 0.8rem;
}

/* System Users */
.system-users {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-status-item {
  display: flex;
  align-items: center;
}

.user-status-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  margin-left: 0.75rem;
  flex-shrink: 0;
}

.user-status-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-status-info {
  flex: 1;
  min-width: 0;
}

.user-status-name {
  font-weight: var(--font-weight-medium);
  margin-bottom: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-status-role {
  margin-bottom: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.user-status-indicator.online {
  background-color: var(--success-color);
}

.user-status-indicator.away {
  background-color: var(--warning-color);
}

.user-status-indicator.offline {
  background-color: var(--text-muted);
}

/* Activity Chart */
.activity-chart-container {
  position: relative;
  height: 200px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem 1rem;
}

/* RTL Support */
[dir="rtl"] .user-avatar,
[dir="rtl"] .user-status-avatar {
  margin-left: 0;
  margin-right: 1rem;
}

[dir="rtl"] .stat-card-content {
  flex-direction: row-reverse;
}

[dir="rtl"] .content-card-header {
  flex-direction: row-reverse;
}

[dir="rtl"] .user-item,
[dir="rtl"] .user-status-item {
  flex-direction: row-reverse;
}

[dir="rtl"] .user-info,
[dir="rtl"] .user-status-info {
  text-align: right;
}

[dir="rtl"] .user-date {
  text-align: left;
}

[dir="rtl"] .activity-timeline {
  padding-left: 0;
  padding-right: 1.5rem;
}

[dir="rtl"] .timeline-item:not(:last-child)::after {
  left: auto;
  right: -0.75rem;
}

[dir="rtl"] .timeline-marker {
  left: auto;
  right: -1.5rem;
}

[dir="rtl"] .timeline-content {
  padding-left: 0;
  padding-right: 0.5rem;
}
</style>
