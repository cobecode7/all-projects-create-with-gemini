<template>
  <div class="users-list">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <h2>المستخدمون</h2>
        <router-link to="/admin/users/create" class="btn btn-primary" v-permission="'users.create'">
          <i class="fas fa-plus"></i> إضافة مستخدم جديد
        </router-link>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="row">
          <div class="col-md-6">
            <div class="search-box">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="البحث عن مستخدم..." v-model="searchQuery">
                <button class="btn btn-outline-secondary" type="button" @click="searchUsers">
                  <i class="fas fa-search"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="col-md-6 text-end">
            <div class="btn-group">
              <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                التصفية حسب الدور
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#" @click.prevent="filterByRole(null)">الكل</a></li>
                <li v-for="role in roles" :key="role.id">
                  <a class="dropdown-item" href="#" @click.prevent="filterByRole(role.id)">{{ role.name }}</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>#</th>
                <th>الاسم</th>
                <th>البريد الإلكتروني</th>
                <th>الدور</th>
                <th>الحالة</th>
                <th>تاريخ التسجيل</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="7" class="text-center">
                  <div class="spinner-border" role="status">
                    <span class="visually-hidden">جاري التحميل...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="users.length === 0">
                <td colspan="7" class="text-center">لا يوجد مستخدمون</td>
              </tr>
              <tr v-else v-for="(user, index) in users" :key="user.id">
                <td>{{ (currentPage - 1) * perPage + index + 1 }}</td>
                <td>{{ user.firstName }} {{ user.lastName }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span class="badge bg-primary">{{ user.role ? user.role.name : 'غير محدد' }}</span>
                </td>
                <td>
                  <span :class="user.isActive ? 'badge bg-success' : 'badge bg-danger'">
                    {{ user.isActive ? 'نشط' : 'غير نشط' }}
                  </span>
                </td>
                <td>{{ formatDate(user.createdAt) }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button class="btn btn-sm btn-outline-primary" @click="viewUser(user)" v-permission="'users.view'">
                      <i class="fas fa-eye"></i>
                    </button>
                    <router-link :to="`/admin/users/${user.id}/edit`" class="btn btn-sm btn-outline-secondary" v-permission="'users.update'">
                      <i class="fas fa-edit"></i>
                    </router-link>
                    <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteUser(user)" v-permission="'users.delete'">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="d-flex justify-content-between align-items-center mt-3">
          <div class="pagination-info">
            عرض {{ (currentPage - 1) * perPage + 1 }} إلى {{ Math.min(currentPage * perPage, totalUsers) }} من {{ totalUsers }} مستخدم
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

    <!-- User Details Modal -->
    <div class="modal fade" id="userModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">تفاصيل المستخدم</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedUser">
            <div class="row mb-3">
              <div class="col-4">الاسم:</div>
              <div class="col-8">{{ selectedUser.firstName }} {{ selectedUser.lastName }}</div>
            </div>
            <div class="row mb-3">
              <div class="col-4">البريد الإلكتروني:</div>
              <div class="col-8">{{ selectedUser.email }}</div>
            </div>
            <div class="row mb-3">
              <div class="col-4">الدور:</div>
              <div class="col-8">{{ selectedUser.role ? selectedUser.role.name : 'غير محدد' }}</div>
            </div>
            <div class="row mb-3">
              <div class="col-4">الحالة:</div>
              <div class="col-8">
                <span :class="selectedUser.isActive ? 'badge bg-success' : 'badge bg-danger'">
                  {{ selectedUser.isActive ? 'نشط' : 'غير نشط' }}
                </span>
              </div>
            </div>
            <div class="row mb-3">
              <div class="col-4">تاريخ التسجيل:</div>
              <div class="col-8">{{ formatDate(selectedUser.createdAt) }}</div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إغلاق</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">تأكيد الحذف</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            هل أنت متأكد من أنك تريد حذف المستخدم "{{ userToDelete ? userToDelete.firstName + ' ' + userToDelete.lastName : '' }}"؟
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
            <button type="button" class="btn btn-danger" @click="deleteUser">حذف</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import adminService from '@/services/adminService';

export default {
  name: 'UsersList',
  data() {
    return {
      users: [],
      roles: [],
      loading: false,
      currentPage: 1,
      perPage: 10,
      totalUsers: 0,
      totalPages: 0,
      searchQuery: '',
      selectedRole: null,
      selectedUser: null,
      userToDelete: null,
      userModal: null,
      deleteModal: null
    };
  },
  created() {
    this.fetchUsers();
    this.fetchRoles();
  },
  mounted() {
    this.userModal = new Modal(document.getElementById('userModal'));
    this.deleteModal = new Modal(document.getElementById('deleteModal'));
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      try {
        const response = await adminService.getUsers(this.currentPage, this.perPage, this.searchQuery, this.selectedRole);
        this.users = response.data;
        this.totalUsers = response.total;
        this.totalPages = response.last_page;
      } catch (error) {
        console.error('Failed to fetch users:', error);
      } finally {
        this.loading = false;
      }
    },
    async fetchRoles() {
      try {
        const response = await adminService.getRoles(1, 100);
        this.roles = response.data;
      } catch (error) {
        console.error('Failed to fetch roles:', error);
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.fetchUsers();
      }
    },
    searchUsers() {
      this.currentPage = 1;
      this.fetchUsers();
    },
    filterByRole(roleId) {
      this.selectedRole = roleId;
      this.currentPage = 1;
      this.fetchUsers();
    },
    viewUser(user) {
      this.selectedUser = user;
      this.userModal.show();
    },
    confirmDeleteUser(user) {
      this.userToDelete = user;
      this.deleteModal.show();
    },
    async deleteUser() {
      if (!this.userToDelete) return;

      try {
        await adminService.deleteUser(this.userToDelete.id);
        this.deleteModal.hide();
        this.fetchUsers();
      } catch (error) {
        console.error('Failed to delete user:', error);
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('ar-SA', options);
    }
  }
};
</script>

<style scoped>
.search-box {
  margin-bottom: 15px;
}

.pagination-info {
  color: #6c757d;
}
</style>
