<template>
  <div class="roles-list">
    <div class="page-header">
      <div class="d-flex justify-content-between align-items-center">
        <h2>الأدوار</h2>
        <router-link to="/admin/roles/create" class="btn btn-primary" v-permission="'roles.create'">
          <i class="fas fa-plus"></i> إضافة دور جديد
        </router-link>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div class="row">
          <div class="col-md-6">
            <div class="search-box">
              <div class="input-group">
                <input type="text" class="form-control" placeholder="البحث عن دور..." v-model="searchQuery">
                <button class="btn btn-outline-secondary" type="button" @click="searchRoles">
                  <i class="fas fa-search"></i>
                </button>
              </div>
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
                <th>اسم الدور</th>
                <th>الوصف</th>
                <th>عدد المستخدمين</th>
                <th>تاريخ الإنشاء</th>
                <th>الإجراءات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="6" class="text-center">
                  <div class="spinner-border" role="status">
                    <span class="visually-hidden">جاري التحميل...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="roles.length === 0">
                <td colspan="6" class="text-center">لا يوجد أدوار</td>
              </tr>
              <tr v-else v-for="(role, index) in roles" :key="role.id">
                <td>{{ (currentPage - 1) * perPage + index + 1 }}</td>
                <td>{{ role.name }}</td>
                <td>{{ role.description || '-' }}</td>
                <td>{{ role.users_count || 0 }}</td>
                <td>{{ formatDate(role.createdAt) }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button class="btn btn-sm btn-outline-primary" @click="viewRole(role)" v-permission="'roles.view'">
                      <i class="fas fa-eye"></i>
                    </button>
                    <router-link :to="`/admin/roles/${role.id}/edit`" class="btn btn-sm btn-outline-secondary" v-permission="'roles.update'">
                      <i class="fas fa-edit"></i>
                    </router-link>
                    <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteRole(role)" v-permission="'roles.delete'" :disabled="role.users_count > 0">
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
            عرض {{ (currentPage - 1) * perPage + 1 }} إلى {{ Math.min(currentPage * perPage, totalRoles) }} من {{ totalRoles }} دور
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

    <!-- Role Details Modal -->
    <div class="modal fade" id="roleModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">تفاصيل الدور</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedRole">
            <div class="row mb-3">
              <div class="col-4">اسم الدور:</div>
              <div class="col-8">{{ selectedRole.name }}</div>
            </div>
            <div class="row mb-3">
              <div class="col-4">الوصف:</div>
              <div class="col-8">{{ selectedRole.description || '-' }}</div>
            </div>
            <div class="row mb-3">
              <div class="col-4">عدد المستخدمين:</div>
              <div class="col-8">{{ selectedRole.users_count || 0 }}</div>
            </div>
            <div class="row mb-3">
              <div class="col-4">تاريخ الإنشاء:</div>
              <div class="col-8">{{ formatDate(selectedRole.createdAt) }}</div>
            </div>
            <div class="row">
              <div class="col-4">الصلاحيات:</div>
              <div class="col-8">
                <div class="permissions-list">
                  <span v-for="permission in selectedRole.permissions" :key="permission.id" class="badge bg-primary me-1 mb-1">
                    {{ permission.name }}
                  </span>
                  <span v-if="!selectedRole.permissions || selectedRole.permissions.length === 0" class="text-muted">
                    لا توجد صلاحيات
                  </span>
                </div>
              </div>
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
            هل أنت متأكد من أنك تريد حذف الدور "{{ roleToDelete ? roleToDelete.name : '' }}"؟
            <div v-if="roleToDelete && roleToDelete.users_count > 0" class="alert alert-warning mt-3">
              <i class="fas fa-exclamation-triangle"></i>
              لا يمكن حذف هذا الدور لأنه مرتبط بـ {{ roleToDelete.users_count }} مستخدم.
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">إلغاء</button>
            <button type="button" class="btn btn-danger" @click="deleteRole" :disabled="roleToDelete && roleToDelete.users_count > 0">حذف</button>
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
  name: 'RolesList',
  data() {
    return {
      roles: [],
      loading: false,
      currentPage: 1,
      perPage: 10,
      totalRoles: 0,
      totalPages: 0,
      searchQuery: '',
      selectedRole: null,
      roleToDelete: null,
      roleModal: null,
      deleteModal: null
    };
  },
  created() {
    this.fetchRoles();
  },
  mounted() {
    this.roleModal = new Modal(document.getElementById('roleModal'));
    this.deleteModal = new Modal(document.getElementById('deleteModal'));
  },
  methods: {
    async fetchRoles() {
      this.loading = true;
      try {
        const response = await adminService.getRoles(this.currentPage, this.perPage, this.searchQuery);
        this.roles = response.data;
        this.totalRoles = response.total;
        this.totalPages = response.last_page;
      } catch (error) {
        console.error('Failed to fetch roles:', error);
      } finally {
        this.loading = false;
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.fetchRoles();
      }
    },
    searchRoles() {
      this.currentPage = 1;
      this.fetchRoles();
    },
    async viewRole(role) {
      try {
        this.selectedRole = await adminService.getRoleById(role.id);
        this.roleModal.show();
      } catch (error) {
        console.error('Failed to fetch role details:', error);
      }
    },
    confirmDeleteRole(role) {
      this.roleToDelete = role;
      this.deleteModal.show();
    },
    async deleteRole() {
      if (!this.roleToDelete) return;

      try {
        await adminService.deleteRole(this.roleToDelete.id);
        this.deleteModal.hide();
        this.fetchRoles();
      } catch (error) {
        console.error('Failed to delete role:', error);
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

.permissions-list {
  max-height: 200px;
  overflow-y: auto;
}
</style>
