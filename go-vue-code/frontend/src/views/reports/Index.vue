<template>
  <div class="reports-container">
    <div class="page-header">
      <h2>التقارير</h2>
    </div>

    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="stats-icon bg-primary text-white">
                  <i class="fas fa-users"></i>
                </div>
              </div>
              <div class="flex-grow-1 ms-3">
                <div class="stats-value">{{ stats.totalUsers }}</div>
                <div class="stats-label">إجمالي المستخدمين</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="stats-icon bg-success text-white">
                  <i class="fas fa-user-check"></i>
                </div>
              </div>
              <div class="flex-grow-1 ms-3">
                <div class="stats-value">{{ stats.activeUsers }}</div>
                <div class="stats-label">المستخدمون النشطون</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="stats-icon bg-warning text-white">
                  <i class="fas fa-user-plus"></i>
                </div>
              </div>
              <div class="flex-grow-1 ms-3">
                <div class="stats-value">{{ stats.newUsers }}</div>
                <div class="stats-label">مستخدمون جدد هذا الشهر</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <div class="stats-icon bg-info text-white">
                  <i class="fas fa-chart-line"></i>
                </div>
              </div>
              <div class="flex-grow-1 ms-3">
                <div class="stats-value">{{ stats.growth }}%</div>
                <div class="stats-label">معدل النمو</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">مخطط نمو المستخدمين</h5>
            <div class="btn-group btn-group-sm">
              <button type="button" class="btn btn-outline-secondary" :class="{ active: chartPeriod === 'week' }" @click="changeChartPeriod('week')">أسبوع</button>
              <button type="button" class="btn btn-outline-secondary" :class="{ active: chartPeriod === 'month' }" @click="changeChartPeriod('month')">شهر</button>
              <button type="button" class="btn btn-outline-secondary" :class="{ active: chartPeriod === 'year' }" @click="changeChartPeriod('year')">سنة</button>
            </div>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas id="userGrowthChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">توزيع المستخدمين حسب الدور</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas id="roleDistributionChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-4">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">سجل النشاط</h5>
            <div class="d-flex">
              <select class="form-select form-select-sm me-2" style="width: auto;" v-model="activityFilter.user">
                <option value="">جميع المستخدمين</option>
                <option v-for="user in users" :key="user.id" :value="user.id">{{ user.firstName }} {{ user.lastName }}</option>
              </select>
              <select class="form-select form-select-sm" style="width: auto;" v-model="activityFilter.action">
                <option value="">جميع الإجراءات</option>
                <option value="login">تسجيل الدخول</option>
                <option value="create">إنشاء</option>
                <option value="update">تحديث</option>
                <option value="delete">حذف</option>
              </select>
            </div>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>المستخدم</th>
                    <th>الإجراء</th>
                    <th>التفاصيل</th>
                    <th>التاريخ والوقت</th>
                    <th>عنوان IP</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="loading">
                    <td colspan="5" class="text-center">
                      <div class="spinner-border" role="status">
                        <span class="visually-hidden">جاري التحميل...</span>
                      </div>
                    </td>
                  </tr>
                  <tr v-else-if="activities.length === 0">
                    <td colspan="5" class="text-center">لا توجد بيانات</td>
                  </tr>
                  <tr v-else v-for="activity in activities" :key="activity.id">
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="avatar-sm me-2">
                          <img v-if="activity.user.avatar" :src="activity.user.avatar" alt="Avatar" class="rounded-circle">
                          <div v-else class="avatar-placeholder-sm bg-primary text-white rounded-circle d-flex align-items-center justify-content-center">
                            {{ activity.user.firstName.charAt(0) }}{{ activity.user.lastName.charAt(0) }}
                          </div>
                        </div>
                        {{ activity.user.firstName }} {{ activity.user.lastName }}
                      </div>
                    </td>
                    <td>
                      <span :class="getActivityBadgeClass(activity.action)">
                        {{ getActivityText(activity.action) }}
                      </span>
                    </td>
                    <td>{{ activity.description }}</td>
                    <td>{{ formatDateTime(activity.createdAt) }}</td>
                    <td>{{ activity.ipAddress }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="d-flex justify-content-between align-items-center mt-3">
              <div class="pagination-info">
                عرض {{ (currentPage - 1) * perPage + 1 }} إلى {{ Math.min(currentPage * perPage, totalActivities) }} من {{ totalActivities }} نشاط
              </div>
              <nav>
                <ul class="pagination">
                  <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <button class="page-link" @click="changePage(currentPage - 1)">السابق</button>
                  </li>
                  <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: page === currentPage }">
                    <button class="page-link" @click="changePage(page)">{{ page }}</button>
                  </li>
                  <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                    <button class="page-link" @click="changePage(currentPage + 1)">التالي</button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import adminService from '@/services/adminService';
import Chart from 'chart.js/auto';

export default {
  name: 'Reports',
  setup() {
    const stats = ref({
      totalUsers: 0,
      activeUsers: 0,
      newUsers: 0,
      growth: 0
    });

    const users = ref([]);
    const activities = ref([]);
    const loading = ref(false);
    const currentPage = ref(1);
    const perPage = ref(10);
    const totalActivities = ref(0);
    const totalPages = ref(0);
    const chartPeriod = ref('month');
    const activityFilter = ref({
      user: '',
      action: ''
    });

    let userGrowthChart = null;
    let roleDistributionChart = null;

    // Fetch dashboard stats
    const fetchStats = async () => {
      try {
        const data = await adminService.getDashboardStats();
        stats.value = data;
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      }
    };

    // Fetch users
    const fetchUsers = async () => {
      try {
        const data = await adminService.getUsers(1, 100);
        users.value = data.data;
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    };

    // Fetch activities
    const fetchActivities = async () => {
      loading.value = true;
      try {
        const data = await adminService.getActivities(
          currentPage.value, 
          perPage.value, 
          activityFilter.value.user, 
          activityFilter.value.action
        );
        activities.value = data.data;
        totalActivities.value = data.total;
        totalPages.value = data.last_page;
      } catch (error) {
        console.error('Failed to fetch activities:', error);
      } finally {
        loading.value = false;
      }
    };

    // Initialize charts
    const initCharts = async () => {
      try {
        // Fetch chart data
        const chartData = await adminService.getChartData(chartPeriod.value);

        // User Growth Chart
        const userGrowthCtx = document.getElementById('userGrowthChart').getContext('2d');

        if (userGrowthChart) {
          userGrowthChart.destroy();
        }

        userGrowthChart = new Chart(userGrowthCtx, {
          type: 'line',
          data: {
            labels: chartData.growth.labels,
            datasets: [{
              label: 'مستخدمون جدد',
              data: chartData.growth.newUsers,
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              tension: 0.1
            }, {
              label: 'مستخدمون نشطون',
              data: chartData.growth.activeUsers,
              borderColor: 'rgb(54, 162, 235)',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              tension: 0.1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });

        // Role Distribution Chart
        const roleDistributionCtx = document.getElementById('roleDistributionChart').getContext('2d');

        if (roleDistributionChart) {
          roleDistributionChart.destroy();
        }

        roleDistributionChart = new Chart(roleDistributionCtx, {
          type: 'doughnut',
          data: {
            labels: chartData.roles.labels,
            datasets: [{
              data: chartData.roles.counts,
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
      } catch (error) {
        console.error('Failed to initialize charts:', error);
      }
    };

    // Change chart period
    const changeChartPeriod = (period) => {
      chartPeriod.value = period;
      initCharts();
    };

    // Change page
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        fetchActivities();
      }
    };

    // Get activity badge class
    const getActivityBadgeClass = (action) => {
      const classes = {
        login: 'badge bg-info',
        create: 'badge bg-success',
        update: 'badge bg-warning',
        delete: 'badge bg-danger'
      };
      return classes[action] || 'badge bg-secondary';
    };

    // Get activity text
    const getActivityText = (action) => {
      const texts = {
        login: 'تسجيل الدخول',
        create: 'إنشاء',
        update: 'تحديث',
        delete: 'حذف'
      };
      return texts[action] || action;
    };

    // Format date and time
    const formatDateTime = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleString('ar-SA');
    };

    // Watch for filter changes
    watch(activityFilter, () => {
      currentPage.value = 1;
      fetchActivities();
    }, { deep: true });

    // Initialize data
    onMounted(() => {
      fetchStats();
      fetchUsers();
      fetchActivities();
      initCharts();
    });

    return {
      stats,
      users,
      activities,
      loading,
      currentPage,
      perPage,
      totalActivities,
      totalPages,
      chartPeriod,
      activityFilter,
      changeChartPeriod,
      changePage,
      getActivityBadgeClass,
      getActivityText,
      formatDateTime
    };
  }
};
</script>

<style scoped>
.stats-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.stats-value {
  font-size: 1.5rem;
  font-weight: 600;
}

.stats-label {
  font-size: 0.875rem;
  color: var(--text-muted);
}

.chart-container {
  position: relative;
  height: 300px;
}

.avatar-sm {
  width: 32px;
  height: 32px;
}

.avatar-placeholder-sm {
  width: 32px;
  height: 32px;
  font-size: 0.75rem;
}

.pagination-info {
  color: var(--text-muted);
  font-size: 0.875rem;
}
</style>
