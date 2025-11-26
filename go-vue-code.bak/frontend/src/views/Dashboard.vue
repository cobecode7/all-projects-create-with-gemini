<template>
  <div>
    <h1 class="mb-4">لوحة التحكم</h1>

    <div class="row">
      <div class="col-md-3">
        <div class="card text-white bg-primary mb-3">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h4 class="card-title">{{ stats.users }}</h4>
                <p class="card-text">المستخدمون</p>
              </div>
              <div class="align-self-center">
                <i class="bi bi-people-fill fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-success mb-3">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h4 class="card-title">{{ stats.roles }}</h4>
                <p class="card-text">الأدوار</p>
              </div>
              <div class="align-self-center">
                <i class="bi bi-shield-fill-check fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-info mb-3">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h4 class="card-title">{{ stats.permissions }}</h4>
                <p class="card-text">الصلاحيات</p>
              </div>
              <div class="align-self-center">
                <i class="bi bi-key-fill fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-warning mb-3">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h4 class="card-title">{{ stats.activeUsers }}</h4>
                <p class="card-text">المستخدمون النشطون</p>
              </div>
              <div class="align-self-center">
                <i class="bi bi-person-check-fill fs-1"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">المستخدمون الجدد</h5>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-3">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">جاري التحميل...</span>
              </div>
            </div>
            <div v-else-if="newUsers.length === 0" class="text-center py-3">
              لا يوجد مستخدمون جدد
            </div>
            <ul v-else class="list-group list-group-flush">
              <li v-for="user in newUsers" :key="user.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ user.firstName }} {{ user.lastName }}</strong>
                  <div class="text-muted small">{{ user.email }}</div>
                </div>
                <small>{{ formatDate(user.createdAt) }}</small>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">نشاط المستخدم</h5>
          </div>
          <div class="card-body">
            <canvas ref="activityChart"></canvas>
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
